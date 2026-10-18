"""Full family u0 = (a sin y, b sin z, c cos x - d cos(x+y+phi)) under 3D periodic NS,
pseudo-spectral (strict 2/3 dealiasing, 3K < N; Leray projection, Lawson RK4), for several b.

At each saved time the phi-harmonics of E, Z, D, S over an 8-point phi grid are
printed: A (constant), B1 (cos phi), B2 (cos 2phi), B3; sine parts are reported
as a check (they should vanish by the reflection symmetry).

Short-time prediction from wavevector counting (see the message): the cos 2phi
part of Z is  -6487/1555200 a^2 b^2 c^2 d^2 t^6 + 207269/7257600 nu a^2 b^2 c^2 d^2 t^7 + O(t^8).
Run: python3 full_family_dns.py N nu T dt b1 b2 ...
"""
import sys, json, time, os
import numpy as np

Z62 = -6487 / 1555200
Z72 = 207269 / 7257600


def make_solver(N, nu, dt):
    k1 = np.fft.fftfreq(N) * N
    kx, ky, kz = np.meshgrid(k1, k1, k1, indexing="ij")
    K = np.array([kx, ky, kz])
    k2 = kx ** 2 + ky ** 2 + kz ** 2
    kmax = (N - 1) // 3          # strict 2/3 rule, 3*kmax < N: no aliasing into the retained shell, and the cubic product's grid average is exact
    mask = (np.abs(kx) <= kmax) & (np.abs(ky) <= kmax) & (np.abs(kz) <= kmax)
    inv = np.where(k2 == 0, 0.0, 1.0 / np.where(k2 == 0, 1.0, k2))

    def project(vh):
        vh = vh * mask
        div = (kx * vh[0] + ky * vh[1] + kz * vh[2]) * inv
        vh = vh - K * div
        vh[:, 0, 0, 0] = 0
        return vh

    def curl(vh):
        return 1j * np.array([ky * vh[2] - kz * vh[1], kz * vh[0] - kx * vh[2], kx * vh[1] - ky * vh[0]])

    def phys(vh):
        return np.array([np.fft.ifftn(c).real for c in vh])

    def rhs(vh):
        u, w = phys(vh), phys(curl(vh))
        n = np.cross(u, w, axis=0)
        return project(np.array([np.fft.fftn(c) for c in n]))

    def diag(vh):
        wh = curl(vh)
        E = 0.5 * float(np.sum(np.abs(vh) ** 2)) / N ** 6
        Z = 0.5 * float(np.sum(np.abs(wh) ** 2)) / N ** 6
        D = float(np.sum(k2 * np.abs(wh) ** 2)) / N ** 6
        # S = <w_i w_j d_j u_i> on the grid (cubic product: modes are low, aliasing negligible at this N)
        w = phys(wh)
        S = 0.0
        for i in range(3):
            for j in range(3):
                dju_i = np.fft.ifftn(1j * K[j] * vh[i]).real
                S += float(np.mean(w[i] * w[j] * dju_i))
        return E, Z, D, S

    Ef, Eh = np.exp(-nu * k2 * dt), np.exp(-nu * k2 * dt / 2)

    def step(uh):
        r1 = rhs(uh)
        r2 = rhs(Eh * (uh + 0.5 * dt * r1))
        r3 = rhs(Eh * uh + 0.5 * dt * r2)
        r4 = rhs(Ef * uh + dt * Eh * r3)
        return (Ef * uh + dt / 6 * (Ef * r1 + 2 * Eh * (r2 + r3) + r4)) * mask

    return project, step, diag


def family(N, a, b, c, d, phi):
    x = 2 * np.pi * np.arange(N) / N
    X, Y, Zg = np.meshgrid(x, x, x, indexing="ij")
    return np.array([a * np.sin(Y), b * np.sin(Zg), c * np.cos(X) - d * np.cos(X + Y + phi)])


def harm(vals, phis, j):
    return (np.mean(vals * np.cos(j * phis)) * (1 if j == 0 else 2), np.mean(vals * np.sin(j * phis)) * 2)


if __name__ == "__main__":
    N, nu, T, dt = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    bs = [float(v) for v in sys.argv[5:]] or [1.0]
    a = c = d = 1.0
    nph = 8
    phis = 2 * np.pi * np.arange(nph) / nph
    project, step, diag = make_solver(N, nu, dt)
    nsteps = int(round(T / dt))
    save_every = max(1, int(round(float(os.environ.get('SAVE', '0.1')) / dt)))
    out = {}
    t0 = time.time()
    for b in bs:
        states = [project(np.array([np.fft.fftn(ci) for ci in family(N, a, b, c, d, p)])) for p in phis]
        rec = []
        for n in range(nsteps + 1):
            if n % save_every == 0:
                t = n * dt
                vals = np.array([diag(s) for s in states])          # (nph, 4): E Z D S
                row = dict(t=t)
                for name, col in (("E", 0), ("Z", 1), ("D", 2), ("S", 3)):
                    row[name] = dict(A=harm(vals[:, col], phis, 0)[0], B1=harm(vals[:, col], phis, 1)[0],
                                     B2=harm(vals[:, col], phis, 2)[0], B3=harm(vals[:, col], phis, 3)[0],
                                     sin1=harm(vals[:, col], phis, 1)[1], sin2=harm(vals[:, col], phis, 2)[1])
                rec.append(row)
            if n < nsteps:
                states = [step(s) for s in states]
        out[str(b)] = rec
        print(f"b={b}: {time.time()-t0:.0f} s so far")
        for row in rec:
            t = row["t"]
            pred = (a*b*c*d) ** 2 * (Z62 * t ** 6 + Z72 * nu * t ** 7)
            print(f"  t={t:.2f}  Z: A={row['Z']['A']:.8f} B1={row['Z']['B1']:+.8f} B2={row['Z']['B2']:+.3e} (t^6,t^7 prediction {pred:+.3e}) B3={row['Z']['B3']:+.2e} sin1={row['Z']['sin1']:+.1e}"
                  f"   S: A={row['S']['A']:+.6f} B1={row['S']['B1']:+.6f} B2={row['S']['B2']:+.2e}   E: B1={row['E']['B1']:+.3e} B2={row['E']['B2']:+.2e}")
    json.dump(out, open(os.environ.get("OUT", "full_family_dns.json"), "w"), indent=0)
