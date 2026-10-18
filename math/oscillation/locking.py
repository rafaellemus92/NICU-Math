"""Phase locking: the Adler equation and the sine circle map.

Exact results used as tests (see test_locking.py):

Adler equation for the relative phase of two rhythms,
    dphi/dt = dw - K sin(phi),
dw = difference of natural frequencies, K = coupling strength (both in rad/s):
  * stable lock iff |dw| < K, at phi* = asin(dw/K);
  * small disturbances of a lock decay at rate lam = sqrt(K^2 - dw^2);
  * outside the lock the phase slips once every T_slip = 2*pi/sqrt(dw^2 - K^2)
    (the mean drift rate is sqrt(dw^2 - K^2)); just below threshold the slips
    are rare and each slip is one anomalous cycle, which is why cycle-to-cycle
    variability rises before locking is reached.

Sine circle map (one rhythm pushed once per cycle of another),
    theta_{n+1} = theta_n + Omega - (K/2pi) sin(2 pi theta_n),
Omega = bare frequency ratio, K = coupling.  Winding number W = lim theta_n/n.
Mode locking W = p/q on intervals of Omega (Arnold tongues):
  * the 0:1 tongue is exactly |Omega| <= K/(2 pi) (fixed point exists iff
    |2 pi Omega / K| <= 1), likewise 1:1 around Omega = 1;
  * the p/q tongue's width scales like K^q for small K (simple ratios lock
    widest; a prime denominator barely locks);
  * the golden mean W = (sqrt5-1)/2 has continued fraction [0;1,1,1,...] and is
    the last quasi-periodic orbit to survive as K -> 1;
  * for K <= 1 the map is a homeomorphism (no positive Lyapunov exponent);
    above K = 1 chaos appears.
"""
from __future__ import annotations
import math

TWO_PI = 2.0 * math.pi
GOLDEN = (math.sqrt(5.0) - 1.0) / 2.0


# ----------------------------------------------------------------- Adler ---
def adler_lock(dw: float, K: float) -> bool:
    return abs(dw) < K


def adler_fixed_phase(dw: float, K: float) -> float:
    if not adler_lock(dw, K):
        raise ValueError("no lock: |dw| >= K")
    return math.asin(dw / K)


def adler_recovery_rate(dw: float, K: float) -> float:
    """Decay rate of a small disturbance of the locked phase."""
    if not adler_lock(dw, K):
        raise ValueError("no lock: |dw| >= K")
    return math.sqrt(K * K - dw * dw)


def adler_slip_period(dw: float, K: float) -> float:
    """Time between phase slips outside the lock (infinite at threshold)."""
    if abs(dw) <= K:          # locked, or exactly at threshold (the slip period diverges there)
        return math.inf
    return TWO_PI / math.sqrt(dw * dw - K * K)


def adler_integrate(dw: float, K: float, phi0: float, t_end: float, dt: float = 1e-3):
    """RK4 integration of the Adler equation; returns (times, phases) unwrapped."""
    f = lambda p: dw - K * math.sin(p)
    n = int(round(t_end / dt))
    ts, ps = [0.0], [phi0]
    p = phi0
    for i in range(n):
        k1 = f(p); k2 = f(p + 0.5 * dt * k1); k3 = f(p + 0.5 * dt * k2); k4 = f(p + dt * k3)
        p += dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        ts.append((i + 1) * dt); ps.append(p)
    return ts, ps


# ------------------------------------------------------------ circle map ---
def circle_step(theta: float, omega: float, K: float) -> float:
    return theta + omega - (K / TWO_PI) * math.sin(TWO_PI * theta)


def circle_analyze(omega: float, K: float, transient: int = 2000, n: int = 3000, qmax: int = 60, tol: float = 1e-7):
    """Winding number, Lyapunov exponent and lock (p, q) of the settled orbit."""
    th = 0.1
    for _ in range(transient):
        th = circle_step(th, omega, K)
    th0, lyap = th, 0.0
    for _ in range(n):
        lyap += math.log(abs(1.0 - K * math.cos(TWO_PI * th)))
        th = circle_step(th, omega, K)
    W, lyap = (th - th0) / n, lyap / n
    base, p, q = th, -1, -1
    for i in range(1, qmax + 1):
        th = circle_step(th, omega, K)
        d = th - base
        if abs(d - round(d)) < tol:
            p, q = int(round(d)), i
            break
    if q > 0:
        g = math.gcd(abs(p), q) or 1
        p, q = p // g, q // g
        W = p / q
    return dict(W=W, locked=q > 0, p=p, q=q, lyap=lyap)


def circle_omega_for(W_target: float, K: float, **kw) -> float:
    """Bisection on the monotone W(Omega) (K <= 1): the LOWER edge of a plateau if W_target is rational."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if circle_analyze(mid, K, **kw)["W"] < W_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def circle_tongue(p: int, q: int, K: float, **kw):
    """Edges, width and centre of the p/q plateau at coupling K (bisection on W from both sides)."""
    target = p / q
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if circle_analyze(mid, K, **kw)["W"] < target:
            lo = mid
        else:
            hi = mid
    edge_lo = hi
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if circle_analyze(mid, K, **kw)["W"] <= target:
            lo = mid
        else:
            hi = mid
    edge_hi = lo
    centre = 0.5 * (edge_lo + edge_hi)
    a = circle_analyze(centre, K, **kw)
    ok = a["locked"] and a["p"] == p and a["q"] == q
    return dict(p=p, q=q, lo=edge_lo, hi=edge_hi, width=(edge_hi - edge_lo) if ok else 0.0, centre=centre, confirmed=ok)


def continued_fraction(x: float, terms: int = 8):
    out, v = [], x
    for _ in range(terms):
        a = math.floor(v)
        out.append(int(a))
        f = v - a
        if f < 1e-9:
            break
        v = 1.0 / f
    return out


if __name__ == "__main__":
    # the neonatal example of the research brief: caregiver 12/min, infant 51.6/min, 4:1 target
    dw = (4 * 12 - 51.6) / 60 * TWO_PI
    print(f"detuning for a 4:1 lock: {dw:.3f} rad/s (the brief's threshold 0.377)")
    for K in (0.28, 0.65):
        if adler_lock(dw, K):
            print(f"  K={K}: locked at phi*={adler_fixed_phase(dw, K):.3f}, disturbances decay at {adler_recovery_rate(dw, K):.3f}/s")
        else:
            print(f"  K={K}: not locked, a phase slip every {adler_slip_period(dw, K):.1f} s")
