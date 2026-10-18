"""Fast checks of the exact enstrophy series (run from enstrophy-jet/:  python3 -m pytest -q tests).

Laurent convention: Z = sum_n sum_m c[n,m](nu) t^n e^{i m phi}; c[n,m] is stored in
results/series.json as a list of rationals [a0, a1, ...] with a_d the coefficient of nu^d.
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SERIES = json.load(open(os.path.join(ROOT, 'results', 'series.json')))


def poly(n, m, key='orders'):
    return [Fr(a) for a in SERIES[key].get(str(n), {}).get(str(m), [])]


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def harmonics(n):
    return [int(m) for m, p in SERIES['orders'][str(n)].items() if any(Fr(a) != 0 for a in p)]


def test_series_is_complete_to_order_14():
    assert SERIES['complete'] is True
    assert sorted(int(n) for n in SERIES['orders']) == list(range(15))
    assert poly(0, 0) == [Fr(5, 4)]                      # Z(0) = 5/4 for every phi
    assert poly(0, 0, 'energy_orders') == [Fr(1)]        # E(0) = 1


def test_c6_pm2_is_the_same_constant_for_every_nu():
    for m in (2, -2):
        assert poly(6, m) == [Fr(-6487, 3110400)]
    assert 2 * poly(6, 2)[0] == Fr(-6487, 1555200)       # the cos(2 phi) coefficient


def test_c7_2_is_exactly_linear_in_nu():
    for m in (2, -2):
        assert trim(poly(7, m)) == [Fr(0), Fr(207269, 14515200)]


def test_c8_2_is_beta_plus_gamma_nu_squared():
    assert trim(poly(8, 2)) == [Fr(7035947189629, 6708369507840000), Fr(0), Fr(-7261, 241920)]


def test_no_harmonic_3_or_higher_below_t9():
    for n in range(9):
        assert max(abs(m) for m in harmonics(n)) <= 2, n
    for n in range(6):
        assert max(abs(m) for m in harmonics(n)) <= 1, n
    assert 3 in harmonics(9) and 4 in harmonics(12) and 4 not in harmonics(11)


def test_time_reversal_parity_up_to_n10():
    """c[n,m](-nu) = (-1)^(n+m) c[n,m](nu): only powers nu^d with d = n+m (mod 2)."""
    for n in range(11):
        for m in harmonics(n):
            p = poly(n, m)
            assert all(a == 0 for d, a in enumerate(p) if (d - n - m) % 2), (n, m)
            for nu in (Fr(1, 7), Fr(3, 2)):
                plus = sum(a * nu ** d for d, a in enumerate(p))
                minus = sum(a * (-nu) ** d for d, a in enumerate(p))
                assert minus == (-1) ** (n + m) * plus, (n, m)


def test_degree_bounds_up_to_n10():
    """deg c[n,0] <= n, deg c[n,+-1] <= n-1, deg c[n,m] <= n - 3|m| for |m| >= 2."""
    for n in range(11):
        for m in harmonics(n):
            deg = len(trim(poly(n, m))) - 1
            bound = n if m == 0 else (n - 1 if abs(m) == 1 else n - 3 * abs(m))
            assert deg <= bound, (n, m, deg, bound)
    # consequences: c[3M,M] is nu-free and c[3M+1,M] is a multiple of nu, M = 2, 3
    for M in (2, 3):
        assert len(trim(poly(3 * M, M))) == 1
        p = trim(poly(3 * M + 1, M))
        assert len(p) == 2 and p[0] == 0


def test_energy_identity():
    """(n+1)[t^(n+1)]E = -2 nu [t^n]Z, harmonic by harmonic."""
    for n in range(14):
        ms = set(SERIES['orders'][str(n)]) | set(SERIES['energy_orders'][str(n + 1)])
        for m in ms:
            lhs = trim([(n + 1) * a for a in poly(n + 1, m, 'energy_orders')])
            rhs = trim([Fr(0)] + [-2 * a for a in poly(n, m)])
            assert lhs == rhs, (n, m)


def test_exact_code_reproduces_series_through_order_8():
    import taylor_exact
    Zc, Ec, info = taylor_exact.compute(8)
    Zs, Es = taylor_exact.serialize(Zc), taylor_exact.serialize(Ec)
    for n in range(9):
        assert Zs[str(n)] == SERIES['orders'][str(n)], n
        assert Es[str(n)] == SERIES['energy_orders'][str(n)], n
    assert info['modes'][8] == SERIES['modes_per_order_U_n']['8']


def test_third_implementation_at_one_nu():
    """Rotational form, complex rationals, nu fixed: matches the nu-polynomials exactly."""
    from flint import fmpq
    import exact_single_nu as e
    for nu in (fmpq(1, 28), fmpq(-2, 3)):
        Zc, Ec, diag = e.run(nu, 6)
        assert e.compare(Zc, SERIES, nu) == []
        assert diag['div_max_nonzero'] == 0 and diag['reality_violations'] == 0
        assert diag['support_violations'] == 0 and not diag['mean_force_nonzero']


def test_leaf_set_T2_carries_all_of_c62_and_c72():
    from flint import fmpq
    import ljet
    T2 = (0, 2, 1, 1, 0, 2, 2, 0)          # {a-^2 b+ b- c-^2 d+^2}
    U = ljet.jet(7, keep=lambda S: all(a <= b for a, b in zip(S, T2)))

    def from_T2(n):
        tot = fmpq(0)
        for (j, S1, S2), s in ljet.zterms(U, n).items():
            if tuple(a + b for a, b in zip(S1, S2)) == T2:
                tot += s
        return tot
    assert from_T2(6) == fmpq(-6487, 3110400)
    assert from_T2(7) == fmpq(207269, 14515200)    # coefficient of nu


def test_float_fft_check_low_order():
    import float_check as fc
    g = fc.Grid(20)
    for nu in (Fr(1, 28), Fr(1, 3)):
        for phi in (0.0, 0.971, 2.16):
            Zn = fc.jet(g, float(nu), phi, 8)
            for n in range(9):
                ex = sum(float(sum(Fr(a) * nu ** d for d, a in enumerate(p))) * math.cos(int(m) * phi)
                         for m, p in SERIES['orders'][str(n)].items())
                assert abs(Zn[n] - ex) <= 1e-12 * max(1.0, abs(ex)), (nu, phi, n, Zn[n], ex)
