"""Cell-sum primitives used by tr_remainder.py, kept importable so that test_tr.py exercises the same code.

Arithmetic is generic: the caller supplies numbers (mpmath intervals in tr_remainder.py, exact Fractions or
intervals in the tests) and, where needed, the exponential.
"""


def inclusive_weight_table(rates, D, exp):
    """E[(i, j)] = exp(sum_{k=i..j} rates[k] * D) for 0 <= i <= j < n.

    The weight for a source in cell i covers cells i through j INCLUSIVE: for s in cell i and t in cell j,
    int_s^t rate <= sum_{k=i..j} rate_k D when every per-cell rate bound rate_k is nonnegative. Prefix sums
    of the explicit per-cell bounds are exact sums, so their differences are exact partial sums (no cumulative
    upper bound of an integral is differenced here)."""
    pre = [rates[0] * 0]
    for r in rates:
        pre.append(pre[-1] + r * D)
    n = len(rates)
    return {(i, j): exp(pre[j + 1] - pre[i]) for j in range(n) for i in range(j + 1)}


def tail_weights(rates, D, exp):
    """P[i] = exp(sum_{k >= i} rates[k] * D): the inclusive weight from cell i to the final time."""
    pre = [rates[0] * 0]
    for r in rates:
        pre.append(pre[-1] + r * D)
    n = len(rates)
    return [exp(pre[n] - pre[i]) for i in range(n)]


def nonincreasing_majorant(w):
    """Smallest nonincreasing sequence phi with phi_i >= w_i: phi_i = max_{k >= i} w_k."""
    out = list(w)
    for i in range(len(out) - 2, -1, -1):
        out[i] = max(out[i], out[i + 1])
    return out


def abel(phi, B):
    """Summation by parts: an upper bound of sum_i phi_i X_i for X_i >= 0 whose partial sums satisfy
    sum_{k <= i} X_k <= B_i, VALID ONLY for phi nonincreasing (callers pass a nonincreasing majorant):
        sum_i phi_i X_i = phi_{m-1} S_{m-1} + sum_{i < m-1} (phi_i - phi_{i+1}) S_i
                       <= phi_{m-1} B_{m-1} + sum_{i < m-1} (phi_i - phi_{i+1}) B_i."""
    m = len(phi)
    tot = phi[-1] * B[m - 1]
    for i in range(m - 1):
        tot = tot + (phi[i] - phi[i + 1]) * B[i]
    return tot
