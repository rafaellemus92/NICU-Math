"""The φ-family of divergence-free 2π-periodic velocity fields.

For each φ ∈ [0, 2π) define

    u^φ(x, y, z) = ( sin y,
                     sin z,
                     cos x − cos(x + y + φ) ).

The family is a single-parameter deformation of one divergence-free
field. Its Fourier content lives on a handful of low wavenumbers; the
dependence on φ is carried by **phases** at the (±1, ±1, 0) modes, not
by magnitudes. The claim this module encodes:

    • ∇ · u^φ = 0 identically for every φ.
    • The volume-mean energy  E = ½ ⟨|u|²⟩              is φ-independent.
    • The volume-mean helicity H = ⟨u · (∇×u)⟩           is 0 for every φ.
    • The volume-mean vortex stretching
          S = ⟨ω_i S_ij ω_j⟩ = ⟨ω_i (∂_j u_i) ω_j⟩
      satisfies  S(φ) = ¼ cos φ.

Reading the claim: two members of the family — say u^0 and u^π —
share identical Fourier magnitudes, identical energy, identical total
helicity (both zero), identical dissipation measure (same |∇u| norms
mod sign, verified numerically), yet have stretching +¼ and −¼
respectively. The reduced state (E, H) therefore does not determine
even the sign of current stretching.

This is a self-contained demonstration of the convergence thesis in
`RESEARCH.md`:

    > The summary doesn't determine the dynamics; the phase and
    > distribution do.

The script runs a φ-sweep on a 32³ spectral grid and prints a table.
The pytest in `tests/fluids/test_phi_family.py` asserts each
quantitative claim.

Dependencies: numpy only.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "grid_and_wavenumbers",
    "velocity",
    "spectral_gradient",
    "velocity_gradient",
    "vorticity",
    "mean_energy",
    "mean_helicity",
    "mean_stretching",
    "sweep_phi",
]


# ─── Grid and spectral utilities ────────────────────────────────────────

def grid_and_wavenumbers(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                           np.ndarray, np.ndarray, np.ndarray]:
    """Return (X, Y, Z, kx, ky, kz) for an n³ grid on [0, 2π)³.

    The spatial arrays have shape (n, n, n). The wavenumber arrays
    have shape (n, 1, 1), (1, n, 1), (1, 1, n) ready for broadcasting
    against FFT output.
    """
    xs = 2 * np.pi * np.arange(n) / n
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    k = np.fft.fftfreq(n, d=1.0 / n).astype(np.float64)  # 0, 1, ..., n/2-1, -n/2, ..., -1
    kx = k.reshape(n, 1, 1)
    ky = k.reshape(1, n, 1)
    kz = k.reshape(1, 1, n)
    return X, Y, Z, kx, ky, kz


def velocity(phi: float, n: int = 32) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate u^φ at every point of the n³ grid.

    Returns (u1, u2, u3), each of shape (n, n, n).
    """
    X, Y, Z, *_ = grid_and_wavenumbers(n)
    u1 = np.sin(Y)
    u2 = np.sin(Z)
    u3 = np.cos(X) - np.cos(X + Y + phi)
    return u1, u2, u3


def spectral_gradient(f: np.ndarray, axis: int) -> np.ndarray:
    """Compute ∂f/∂x_axis on a periodic grid by multiplying by i·k_axis in Fourier space.

    `axis` is 0 for x, 1 for y, 2 for z.
    """
    n = f.shape[axis]
    k = np.fft.fftfreq(n, d=1.0 / n).astype(np.float64)
    shape = [1, 1, 1]
    shape[axis] = n
    k = 1j * k.reshape(shape)
    F = np.fft.fftn(f)
    return np.real(np.fft.ifftn(F * k))


def velocity_gradient(u: tuple[np.ndarray, np.ndarray, np.ndarray]
                      ) -> np.ndarray:
    """Compute the velocity-gradient tensor ∂_j u_i.

    Returns an array of shape (3, 3, n, n, n) where entry [i, j]
    equals ∂_j u_i. (Index i = component of u; index j = direction of
    the derivative — standard convention for ∇u in fluid mechanics.)
    """
    n = u[0].shape[0]
    G = np.empty((3, 3, n, n, n))
    for i in range(3):
        for j in range(3):
            G[i, j] = spectral_gradient(u[i], j)
    return G


def vorticity(u: tuple[np.ndarray, np.ndarray, np.ndarray],
              G: np.ndarray | None = None
              ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """ω = ∇ × u. Pass a precomputed velocity-gradient to save work."""
    if G is None:
        G = velocity_gradient(u)
    w1 = G[2, 1] - G[1, 2]
    w2 = G[0, 2] - G[2, 0]
    w3 = G[1, 0] - G[0, 1]
    return w1, w2, w3


# ─── Mean quantities ────────────────────────────────────────────────────

def mean_energy(u: tuple[np.ndarray, np.ndarray, np.ndarray]) -> float:
    """E = ½ ⟨|u|²⟩, where ⟨·⟩ is the volume mean over [0, 2π)³."""
    u1, u2, u3 = u
    return 0.5 * float(np.mean(u1 * u1 + u2 * u2 + u3 * u3))


def mean_helicity(u: tuple[np.ndarray, np.ndarray, np.ndarray],
                  w: tuple[np.ndarray, np.ndarray, np.ndarray]) -> float:
    """H = ⟨u · ω⟩."""
    u1, u2, u3 = u
    w1, w2, w3 = w
    return float(np.mean(u1 * w1 + u2 * w2 + u3 * w3))


def mean_stretching(w: tuple[np.ndarray, np.ndarray, np.ndarray],
                    G: np.ndarray) -> float:
    """S = ⟨ω_i (∂_j u_i) ω_j⟩.

    The antisymmetric part of ∂_j u_i vanishes when contracted with
    the symmetric tensor ω_i ω_j, so this equals ⟨ω_i S_ij ω_j⟩ with
    S_ij the strain-rate tensor.
    """
    w_arr = np.stack(w)  # (3, n, n, n)
    # Full contraction ω_i G_ij ω_j via einsum.
    integrand = np.einsum("ixyz,ijxyz,jxyz->xyz", w_arr, G, w_arr)
    return float(np.mean(integrand))


# ─── Divergence check ───────────────────────────────────────────────────

def mean_abs_divergence(u: tuple[np.ndarray, np.ndarray, np.ndarray]) -> float:
    """⟨|∇·u|⟩ — a residual check; should be ~ machine precision."""
    div = (spectral_gradient(u[0], 0)
           + spectral_gradient(u[1], 1)
           + spectral_gradient(u[2], 2))
    return float(np.mean(np.abs(div)))


# ─── Sweep ──────────────────────────────────────────────────────────────

def sweep_phi(phis: np.ndarray, n: int = 32) -> dict[str, np.ndarray]:
    """For each φ in `phis`, compute (E, H, S) and the divergence residual.

    Returns a dict with keys "phi", "E", "H", "S", "div_residual".
    """
    E = np.empty_like(phis, dtype=np.float64)
    H = np.empty_like(phis, dtype=np.float64)
    S = np.empty_like(phis, dtype=np.float64)
    D = np.empty_like(phis, dtype=np.float64)
    for i, phi in enumerate(phis):
        u = velocity(float(phi), n=n)
        G = velocity_gradient(u)
        w = vorticity(u, G=G)
        E[i] = mean_energy(u)
        H[i] = mean_helicity(u, w)
        S[i] = mean_stretching(w, G)
        D[i] = mean_abs_divergence(u)
    return {"phi": np.asarray(phis, dtype=np.float64),
            "E": E, "H": H, "S": S, "div_residual": D}


# ─── Script entrypoint ──────────────────────────────────────────────────

def _print_table(data: dict[str, np.ndarray]) -> None:
    print(f"{'phi/π':>8} {'E':>12} {'H':>14} {'S':>14} "
          f"{'¼cos(phi)':>14} {'|div u|':>12}")
    print("-" * 80)
    for phi, E, H, S, D in zip(data["phi"], data["E"], data["H"],
                               data["S"], data["div_residual"]):
        print(f"{phi / np.pi:>8.3f} {E:>12.6f} {H:>14.3e} "
              f"{S:>14.6f} {0.25 * np.cos(phi):>14.6f} {D:>12.3e}")


def main(n: int = 32, n_phi: int = 13) -> None:
    """Sweep φ ∈ [0, 2π] on an n³ grid; print the table."""
    phis = np.linspace(0.0, 2 * np.pi, n_phi)
    data = sweep_phi(phis, n=n)
    print(f"φ-family sweep · {n}³ spectral grid · {n_phi} values\n")
    _print_table(data)
    print()
    print(f"max |E − E(0)|             = {np.max(np.abs(data['E'] - data['E'][0])):.3e}")
    print(f"max |H|                    = {np.max(np.abs(data['H'])):.3e}")
    print(f"max |S − ¼ cos φ|          = "
          f"{np.max(np.abs(data['S'] - 0.25 * np.cos(data['phi']))):.3e}")
    print(f"max |∇·u| (residual)       = {np.max(data['div_residual']):.3e}")


if __name__ == "__main__":
    main()
