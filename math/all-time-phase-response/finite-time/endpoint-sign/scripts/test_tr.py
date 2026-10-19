"""Exact toy-equation tests of the cell weights and of the summation by parts used by tr_remainder.py
(audit repair 2). Every test checks the IMPLEMENTED form against an exact answer and requires a plausible
BROKEN form to fail, so a weight or index error cannot pass silently.
Run from this folder:  python3 -I -m unittest -v test_tr
"""
import sys
import unittest
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpmath import iv
from tr_core import inclusive_weight_table, tail_weights, nonincreasing_majorant, abel
iv.dps = 50
N = 12


def exact_cell_ends(rates, f, D):
    """Exact solution of x' = c_k x + f_k on cell k, x(0) = 0 (rate and source constant on each cell):
    x_{k+1} = e^{c_k D} x_k + f_k (e^{c_k D} - 1)/c_k, enclosed in intervals; returns x at every cell end."""
    x, out = iv.mpf(0), []
    for c, s in zip(rates, f):
        e = iv.exp(c * D)
        x = e * x + s * (e - 1) / c
        out.append(x)
    return out


class CellWeights(unittest.TestCase):
    D = iv.mpf(1) / 8
    # rates of the size of m1 - nu (about 2.5) and of 4 m1 + 1 (about 11)
    CASES = ([iv.mpf(2) + iv.mpf(k % 3) / 2 for k in range(N)], [iv.mpf(10) + iv.mpf(k % 4) / 3 for k in range(N)])
    F = [iv.mpf((5 * k + 1) % 7) for k in range(N)]                  # nonnegative sources, some zero

    def bound(self, E, j):
        return sum((E[(i, j)] * self.F[i] for i in range(j + 1)), iv.mpf(0)) * self.D

    def test_inclusive_weight_bounds_the_exact_solution(self):
        worst = 0
        for rates in self.CASES:
            E, x = inclusive_weight_table(rates, self.D, iv.exp), exact_cell_ends(rates, self.F, self.D)
            for j in range(N):
                self.assertTrue(self.bound(E, j).a >= x[j].b, (j, float(self.bound(E, j).a), float(x[j].b)))
                worst = max(worst, float((x[j] / self.bound(E, j)).b))
        print(f'\n  inclusive weights: exact/bound <= {worst:.4f} over both rate families', flush=True)

    def test_weight_excluding_the_source_cell_is_rejected(self):
        for rates in self.CASES:
            E, x = inclusive_weight_table(rates, self.D, iv.exp), exact_cell_ends(rates, self.F, self.D)
            broken = {(i, j): E[(i, j)] / iv.exp(rates[i] * self.D) for (i, j) in E}     # exp(sum_{k=i+1..j})
            self.assertTrue(any(self.bound(broken, j).b < x[j].a for j in range(N)))

    def test_tail_weights_are_the_inclusive_weights_to_the_end(self):
        rates = self.CASES[0]
        E, P = inclusive_weight_table(rates, self.D, iv.exp), tail_weights(rates, self.D, iv.exp)
        for i in range(N):
            self.assertTrue(P[i].a <= E[(i, N - 1)].b and E[(i, N - 1)].a <= P[i].b)


class SummationByParts(unittest.TestCase):
    def trials(self, count=4000):
        seed = 20261019

        def rnd(m):
            nonlocal seed
            seed = (1103515245 * seed + 12345) % 2 ** 31
            return seed % m
        for _ in range(count):
            m = 2 + rnd(11)
            X = [Fr(rnd(9), 1 + rnd(4)) for _ in range(m)]            # cell integrals, X_i >= 0
            w = [Fr(rnd(13), 1 + rnd(3)) for _ in range(m)]           # arbitrary nonnegative weights
            S, s = [], Fr(0)
            for x in X:
                s += x
                S.append(s)
            B = [S[i] + (Fr(rnd(7), 1 + rnd(5)) if rnd(2) else Fr(0)) for i in range(m)]   # valid, unevenly loose
            yield X, w, B

    def test_implemented_form_never_fails_and_every_broken_form_does(self):
        fails = dict(implemented=0, no_majorant=0, no_end_term=0, index_shift=0, cell_differencing=0)
        for X, w, B in self.trials():
            m, truth = len(X), sum(a * b for a, b in zip(w, X))
            phi = nonincreasing_majorant(w)
            fails['implemented'] += abel(phi, B) < truth
            fails['no_majorant'] += abel(w, B) < truth
            fails['no_end_term'] += sum((phi[i] - phi[i + 1]) * B[i] for i in range(m - 1)) < truth
            fails['index_shift'] += (phi[-1] * B[-1] + sum((phi[i] - phi[i + 1]) * (B[i - 1] if i else 0)
                                                            for i in range(m - 1))) < truth
            fails['cell_differencing'] += sum(w[i] * (B[i] - (B[i - 1] if i else 0)) for i in range(m)) < truth
        print(f'\n  failures in 4000 exact trials: {fails}', flush=True)
        self.assertEqual(fails['implemented'], 0)
        for key in ('no_majorant', 'no_end_term', 'index_shift', 'cell_differencing'):
            self.assertGreater(fails[key], 0, key)

    def test_majorant_is_the_smallest_nonincreasing_one(self):
        w = [Fr(3), Fr(1), Fr(4), Fr(1), Fr(5), Fr(0)]
        phi = nonincreasing_majorant(w)
        self.assertEqual(phi, [Fr(5), Fr(5), Fr(5), Fr(5), Fr(5), Fr(0)])
        self.assertTrue(all(phi[i] >= phi[i + 1] for i in range(len(w) - 1)) and all(p >= x for p, x in zip(phi, w)))


class CalculationUsesTheseFunctions(unittest.TestCase):
    def test_tr_remainder_imports_and_does_not_redefine(self):
        src = (Path(__file__).resolve().parent / 'tr_remainder.py').read_text()
        self.assertIn('from tr_core import inclusive_weight_table, tail_weights, nonincreasing_majorant, abel', src)
        for name in ('def abel', 'def nonincreasing_majorant', 'def inclusive_weight_table', 'def tail_weights'):
            self.assertNotIn(name, src)


if __name__ == '__main__':
    unittest.main()
