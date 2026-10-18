"""Radix-2 Cooley–Tukey FFT.

Twin of `sgrounds/lib/piano/hilbert.ts`'s `fftInPlace` / `ifftInPlace`.
Numpy already ships an excellent FFT; we keep our own radix-2 here only
to match the TS implementation bit-for-bit on shared JSON vectors.
Downstream callers that don't need twin agreement should use
`numpy.fft.fft` directly.

Operates on in-place `float64` arrays. Length must be a power of two.
"""

from __future__ import annotations

import numpy as np

__all__ = ["fft_in_place", "ifft_in_place", "next_pow2"]


def next_pow2(n: int) -> int:
    """Smallest power of two ≥ n (returns 1 for n ≤ 0)."""
    if n <= 1:
        return 1
    p = 1
    while p < n:
        p <<= 1
    return p


def fft_in_place(re: np.ndarray, im: np.ndarray) -> None:
    """In-place radix-2 Cooley–Tukey FFT.

    Mutates `re` and `im`. Both must be 1-D float64 arrays of the same
    length N, where N is a power of two.
    """
    n = re.size
    if im.size != n:
        raise ValueError("fft: re/im length mismatch")
    if n & (n - 1):
        raise ValueError(f"fft: length {n} is not a power of 2")

    # Bit-reverse permutation.
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            re[i], re[j] = re[j], re[i]
            im[i], im[j] = im[j], im[i]

    # Butterflies.
    length = 2
    while length <= n:
        half = length >> 1
        theta = -2 * np.pi / length
        wpr = np.cos(theta)
        wpi = np.sin(theta)
        for i in range(0, n, length):
            wr, wi = 1.0, 0.0
            for k in range(half):
                a = i + k
                b = a + half
                t_re = wr * re[b] - wi * im[b]
                t_im = wr * im[b] + wi * re[b]
                re[b] = re[a] - t_re
                im[b] = im[a] - t_im
                re[a] += t_re
                im[a] += t_im
                nwr = wr * wpr - wi * wpi
                wi = wr * wpi + wi * wpr
                wr = nwr
        length <<= 1


def ifft_in_place(re: np.ndarray, im: np.ndarray) -> None:
    """Inverse of `fft_in_place`, in place and 1/N normalised."""
    np.negative(im, out=im)
    fft_in_place(re, im)
    n = re.size
    re /= n
    np.negative(im, out=im)
    im /= n
