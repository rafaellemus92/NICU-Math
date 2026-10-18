"""Verify only the prefiled two-compartment exact-computation claim."""

import numpy as np
import pytest
import scipy
from scipy.integrate import solve_ivp

from physiology.two_compartment import (
    Compartment, passive_emptying_series, passive_retained_fraction, tau,
)


def cases(R=1.0, C=1.0):
    return ([Compartment(2 * R, C / 2)] * 2,
            [Compartment(2 * R, 0.9 * C), Compartment(2 * R, 0.1 * C)])


@pytest.mark.parametrize("R,C,P_0", [(1., 1., 1.), (3., 2., 4.), (0.2, 7., 0.3)])
def test_headline(R, C, P_0):
    """Same total C and initial excess volume; different retained fractions."""
    a, b = cases(R, C)
    for compartments in (a, b):
        assert sum(c.C for c in compartments) == pytest.approx(C)
        initial = passive_emptying_series(compartments, P_0, np.array([0.]))
        assert initial.sum() == pytest.approx(C * P_0)
    assert tau(a[0]) == R * C
    assert tau(b[0]) == pytest.approx(1.8 * R * C)
    assert tau(b[1]) == pytest.approx(0.2 * R * C)
    fa = passive_retained_fraction(a, P_0, R * C)
    fb = passive_retained_fraction(b, P_0, R * C)
    assert abs(fa - np.exp(-1)) < 1e-10
    assert abs(fb - (0.9 * np.exp(-1 / 1.8) + 0.1 * np.exp(-5))) < 1e-10
    # Headline floating evaluation is also checked at float64 roundoff scale.
    assert abs(fa - 0.36787944117144233) <= 2 * np.finfo(float).eps
    assert abs(fb - 0.5170518733635980) <= 2 * np.finfo(float).eps
    assert fb - fa > 0.14


@pytest.mark.parametrize("index", [0, 1])
def test_solve_ivp_crosscheck(index):
    """Independent ODE integration, including the required symmetric case."""
    if index == 0:
        print(f"Verification versions: NumPy {np.__version__}, SciPy {scipy.__version__}")
    compartments = cases(R=3., C=2.)[index]
    grid = np.linspace(0., 30., 101)
    initial = np.array([c.C * 4. for c in compartments])
    numerical = solve_ivp(
        lambda t, v: -v / np.array([tau(c) for c in compartments]),
        (0., 30.), initial, t_eval=grid, rtol=1e-10, atol=1e-12,
    )
    assert numerical.success
    analytical = passive_emptying_series(compartments, 4., grid)
    error = np.max(np.abs(numerical.y - analytical))
    print(f"solve_ivp case {index}: max absolute volume error={error:.3e}")
    assert error < 1e-6


def test_series_shape_order_decay_and_pressure_scaling():
    compartments = cases()[1]
    grid = np.array([0., 0.2, 1., 10., 1e300])
    volumes = passive_emptying_series(compartments, 2., grid)
    assert volumes.shape == (2, 5)
    assert np.all(np.diff(volumes, axis=1) <= 0)
    assert np.all(volumes >= 0)
    assert np.all(volumes[:, -1] == 0)
    np.testing.assert_array_equal(
        passive_emptying_series(compartments, 2., grid[[2, 0, 2]]),
        volumes[:, [2, 0, 2]],
    )
    assert passive_emptying_series(compartments, 2., np.array([])).shape == (2, 0)
    assert passive_retained_fraction(compartments, 2., 0.) == 1.
    assert passive_retained_fraction(compartments, 2., 1.) == pytest.approx(
        passive_retained_fraction(compartments, 7., 1.))


def test_zero_pressure():
    compartments = cases()[0]
    assert np.all(passive_emptying_series(compartments, 0., np.arange(3)) == 0)
    with pytest.raises(ValueError):
        passive_retained_fraction(compartments, 0., 1.)


@pytest.mark.parametrize("bad", [0., -1., np.nan, np.inf, -np.inf, [1.], 1j, True])
@pytest.mark.parametrize("field", ["R", "C"])
def test_invalid_compartment(bad, field):
    with pytest.raises(ValueError):
        Compartment(**{field: bad, "C" if field == "R" else "R": 1.})


@pytest.mark.parametrize("R,C", [(1e308, 2.), (1e-300, 1e-300)])
def test_unrepresentable_time_constant(R, C):
    with pytest.raises(ValueError):
        Compartment(R, C)


@pytest.mark.parametrize("bad", [-1., np.inf, np.nan, [1.], 1j])
def test_invalid_pressure_or_scalar_time(bad):
    for pressure, time in ((bad, 1.), (1., bad)):
        with pytest.raises(ValueError):
            passive_retained_fraction(cases()[0], pressure, time)


@pytest.mark.parametrize("grid", [[-1.], [np.nan], [np.inf], [[1.]], 1., [1j]])
def test_invalid_grid(grid):
    with pytest.raises(ValueError):
        passive_emptying_series(cases()[0], 1., grid)


@pytest.mark.parametrize("compartments,pressure", [
    ([], 1.), ([1.], 1.), ([Compartment(1., 1e308)] * 2, 1.),
    ([Compartment(1., 1e-300)], 1e-300),
    ([Compartment(1., 1e308)], 2.),
])
def test_invalid_initial_state(compartments, pressure):
    with pytest.raises(ValueError):
        passive_emptying_series(compartments, pressure, np.array([0.]))
