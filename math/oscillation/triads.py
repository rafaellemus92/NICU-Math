"""Vortex stretching as a sum over Fourier triads, and its phase coherence.

For a periodic velocity field u(x) = sum_k u^(k) e^{ik.x} with vorticity
w^(k) = i k x u^(k), the spatial average of vortex stretching is
    S = <w_i w_j d_j u_i> = sum_{k+p+q=0} (w^(k) . i p) (w^(q) . u^(p)).
Every term c(k,p) (q = -k-p) is a complex number; the field is real so the
terms pair into conjugates and the sum is real.  Write c = |c| e^{i phi}: S is
the Kuramoto-type sum sum |c| cos(phi) over the triads, so
    R = |S| / sum |c|   in [0, 1]
is the order parameter of the triad phases - 1 when every term has the same
sign, 0 when they cancel completely.  Random independent mode phases make the
triad phases nearly uniform at t = 0; organization is what the dynamics do to
them.

Convention: the (3, N, N, N//2+1) arrays are the Fourier COEFFICIENTS u^(k)
of the rfft half-space, u = sum_k u^(k) e^{ik.x}, i.e. rfftn(u) / N^3.  This
is the Helical Lab ensemble's convention (its diagnostics give E = 1 for every
case); test_triads.py pins it on an exactly known field.

This script computes S, sum|c| and R, checks E, Z, D, S against the
ensemble's own diagnostics where the archive part has them, and tabulates R
at t=0 and t=T.  The triad sum is O(N^6) per field (about 13 s at N = 24);
cases run in parallel.

Run:  python3 -I triads.py <ensemble_dir> [out.json] [workers]
"""
from __future__ import annotations
import csv, glob, json, os, sys, time
from multiprocessing import Pool
import numpy as np


def full_spectrum(uh_half: np.ndarray):
    """rfft coefficient array -> ((3,N,N,N) full coefficient array, physical field u on the N^3 grid)."""
    N = uh_half.shape[1]
    u = np.fft.irfftn(uh_half * N ** 3, s=(N, N, N), axes=(1, 2, 3))   # numpy's irfftn undoes an unnormalised rfftn
    return np.fft.fftn(u, axes=(1, 2, 3)) / N ** 3, u


def wavevectors(N: int):
    """Integer wavenumbers in numpy fftfreq order, exact (fftfreq(N)*N is off by an ulp for some N)."""
    k = np.rint(np.fft.fftfreq(N) * N)
    return np.meshgrid(k, k, k, indexing="ij")


def diagnostics(uh_half: np.ndarray):
    """E, Z, D by exact spectral sums; S, sum|c| and R by the triad sum."""
    uc, _ = full_spectrum(uh_half)
    N = uc.shape[1]
    kx, ky, kz = wavevectors(N)
    kvec = np.stack([kx, ky, kz])
    k2 = kx ** 2 + ky ** 2 + kz ** 2
    wc = 1j * np.cross(kvec, uc, axisa=0, axisb=0, axisc=0)         # vorticity coefficients
    E = 0.5 * float(np.sum(np.abs(uc) ** 2))
    Z = 0.5 * float(np.sum(np.abs(wc) ** 2))
    D = float(np.sum(k2 * np.abs(wc) ** 2))
    S, sum_abs, R = stretching_triads(uc, wc, kvec)
    return dict(E=E, Z=Z, D=D, S=S, sum_abs=sum_abs, R=R)


def stretching_triads(uc: np.ndarray, wc: np.ndarray, kvec: np.ndarray):
    """S = sum_{k,p} (w^(k).ip)(w^(-k-p).u^(p)) over all retained modes; returns (S, sum|c|, R).

    Grid index a of a wavenumber satisfies a = k mod N (numpy fftfreq order), so the
    coefficient of k+p sits at grid index (a_k + a_p) mod N: one gather per k.
    """
    N = uc.shape[1]
    M = N ** 3
    ucf, wcf = uc.reshape(3, M), wc.reshape(3, M)
    ip = (1j * kvec).reshape(3, M)                                    # i p over p
    g = np.arange(N)
    gx, gy, gz = (a.ravel() for a in np.meshgrid(g, g, g, indexing="ij"))
    active = np.flatnonzero(np.any(np.abs(wcf) > 0, axis=0))         # modes with vorticity
    total, total_abs = 0.0 + 0.0j, 0.0
    for m in active:
        a, b, c = m // (N * N), (m // N) % N, m % N
        idx = ((gx + a) % N) * (N * N) + ((gy + b) % N) * N + (gz + c) % N
        wkp = np.take(wcf, idx, axis=1)                              # w^(k+p) over p
        B = np.einsum("jp,jp->p", np.conj(wkp), ucf)                 # (w^(-k-p) . u^(p)), real field: w^(-k) = conj w^(k)
        wk = wcf[:, m]
        A = wk[0] * ip[0] + wk[1] * ip[1] + wk[2] * ip[2]            # (w^(k) . i p) over p
        cc = A * B
        total += cc.sum()
        total_abs += np.abs(cc).sum()
    S = float(total.real)
    return S, float(total_abs), (abs(S) / total_abs if total_abs > 0 else 0.0)


def _case(cdir: str):
    """One case: diagnostics at t=0 and t=T, compared with the ensemble's own files where present."""
    snap = os.path.join(cdir, "snapshots.npz")
    if not os.path.exists(snap):
        return None
    z = np.load(snap)
    uh, times = z["uh"], z["times"]
    d0, dT = diagnostics(uh[0]), diagnostics(uh[-1])
    name = os.path.basename(cdir)
    profile, split, delta_Z = name.split("_")[0], None, dT["Z"] - d0["Z"]
    worst, ncmp = {}, 0
    dpath, cpath, rpath = (os.path.join(cdir, f) for f in ("diagnostics.csv", "checks.json", "result.json"))
    if os.path.exists(dpath):
        rows = list(csv.DictReader(open(dpath)))
        ref0 = {k: float(v) for k, v in rows[0].items()}
        refT = {k: float(v) for k, v in rows[-1].items()}
        for k in ("E", "Z", "D", "S"):
            worst[k + "0"] = abs(d0[k] - ref0[k])
            worst[k + "T"] = abs(dT[k] - refT[k])
        ncmp += 1
    if os.path.exists(cpath):
        worst["ST_checks"] = abs(dT["S"] - json.load(open(cpath))["final"]["S"])
    if os.path.exists(rpath):
        res = json.load(open(rpath)); split = res["split"]
        worst["dZ_result"] = abs(res["delta_Z"] - delta_Z)
    return dict(case=name, profile=profile, split=split, T=float(times[-1]),
                E0=d0["E"], Z0=d0["Z"], D0=d0["D"], S0=d0["S"], sumabs0=d0["sum_abs"], R0=d0["R"],
                ET=dT["E"], ZT=dT["Z"], DT=dT["D"], ST=dT["S"], sumabsT=dT["sum_abs"], RT=dT["R"],
                delta_Z=delta_Z, compared=ncmp), worst


def analyze_ensemble(root: str, out_json: str | None = None, workers: int | None = None):
    t0 = time.time()
    cases = sorted(glob.glob(os.path.join(root, "main", "*")))
    with Pool(workers) as pool:
        out = [r for r in pool.map(_case, cases, chunksize=1) if r is not None]
    rows, worst = [r for r, _ in out], {}
    for _, w in out:
        for k, v in w.items():
            worst[k] = max(worst.get(k, 0.0), v)
    print(f"{len(rows)} cases with snapshots, {sum(r['compared'] for r in rows)} with the ensemble's own diagnostics.csv; worst |mine - ensemble|: " + ", ".join(f"{k} {v:.1e}" for k, v in sorted(worst.items())))
    R0, RT = np.array([r["R0"] for r in rows]), np.array([r["RT"] for r in rows])
    S0, ST = np.array([r["S0"] for r in rows]), np.array([r["ST"] for r in rows])
    dZ = np.array([r["delta_Z"] for r in rows])
    print(f"E at t=0: {min(r['E0'] for r in rows):.6f}..{max(r['E0'] for r in rows):.6f}  (the ensemble normalises every case to E = 1)")
    print(f"triad-phase order parameter R = |S| / sum|c|:   t=0: mean {R0.mean():.4f} (min {R0.min():.4f}, max {R0.max():.4f})   t=T: mean {RT.mean():.4f} (min {RT.min():.4f}, max {RT.max():.4f})")
    print(f"cases with R(T) > R(0): {int((RT > R0).sum())}/{len(rows)};  S mean t=0 {S0.mean():+.4f} (|S| {np.abs(S0).mean():.4f}) -> t=T {ST.mean():+.4f} (|S| {np.abs(ST).mean():.4f});  sum|c| mean t=0 {np.mean([r['sumabs0'] for r in rows]):.3f} -> t=T {np.mean([r['sumabsT'] for r in rows]):.3f}")
    print(f"cases with S(T) > 0: {int((ST > 0).sum())}/{len(rows)};  S(0) > 0: {int((S0 > 0).sum())}/{len(rows)}")
    corr = lambda a, b: float(np.corrcoef(a, b)[0, 1])
    print(f"correlations: R(T) vs S(T) {corr(RT, ST):+.3f};  R(0) vs delta_Z {corr(R0, dZ):+.3f};  S(0) vs delta_Z {corr(S0, dZ):+.3f};  R(T) vs delta_Z {corr(RT, dZ):+.3f};  R(0) vs R(T) {corr(R0, RT):+.3f}")
    for prof in sorted(set(r["profile"] for r in rows)):
        m = np.array([r["profile"] == prof for r in rows])
        print(f"  {prof}: n={int(m.sum())}  R0 {R0[m].mean():.4f} -> RT {RT[m].mean():.4f};  S0 {S0[m].mean():+.4f} -> ST {ST[m].mean():+.4f};  delta_Z {dZ[m].mean():+.4f}")
    elapsed = time.time() - t0
    print(f"elapsed {elapsed:.0f} s with {workers or os.cpu_count()} workers")
    if out_json:
        json.dump(dict(convention="uh = rfftn(u)/N^3 (Fourier coefficients); E, Z, D exact spectral sums; S and sum|c| by the full triad sum",
                       worst_abs_diff_vs_ensemble=worst, elapsed_s=elapsed, cases=rows), open(out_json, "w"), indent=1)
        print("wrote", out_json)
    return rows


if __name__ == "__main__":
    analyze_ensemble(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, int(sys.argv[3]) if len(sys.argv) > 3 else None)
