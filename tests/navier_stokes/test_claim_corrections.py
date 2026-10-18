"""Synthetic implementation checks; universal statements are derived in README."""
import numpy as np
import pytest
from navier_stokes.formulation import (
    BreathCycle, classify_compliance, sphere_volume_rate, static_sphere_pressure,
    laplace_pressure, squared_flow_time_derivative, kinetic_energy_per_length,
    surface_tension_response, CONST,
)
from navier_stokes.analysis import summarize_compliance, flow_derivative_evolution
from navier_stokes.ventilator_ingest import generate_synthetic_waveform, segment_breaths
from navier_stokes.proof_outline import estimate_critical_constant


@pytest.mark.parametrize('r', [0.1, 1, 3])
def test_material_sphere_flux_matches_divergence(r):
    speed = -0.2
    # u(x)=speed*x/r has div u=3*speed/r, and u.n=speed at radius r.
    volume = 4 * np.pi * r**3 / 3
    assert sphere_volume_rate(r, speed) == pytest.approx((3 * speed / r) * volume)
    assert sphere_volume_rate(r, speed) < 0  # incompatible with div u=0
    assert sphere_volume_rate(r, 0) == 0


@pytest.mark.parametrize('gamma', [0.001, 0.07, 1e6])
@pytest.mark.parametrize('r', [0.01, 1.0])
def test_static_sphere_traction(gamma, r):
    p_ext = 3.0
    p = static_sphere_pressure(gamma, r, p_ext)
    normal = np.array([1., 2., 3.]) / np.sqrt(14)
    # u=0 => D(u)=0, T=-p I; outward-normal curvature kappa=2/r.
    stress_jump = (-p + p_ext) * np.eye(3)
    np.testing.assert_allclose(stress_jump @ normal, -gamma * (2 / r) * normal, rtol=1e-12)


def test_reduced_positive_gamma_keeps_inverse_radius_scaling():
    radii = np.array([1., .1, .01, .001])
    for gamma in (.07, .025):
        pressure = np.array([laplace_pressure(gamma, r) for r in radii])
        np.testing.assert_allclose(pressure[1:] / pressure[:-1], 10.)
    # Samples check the identity; they are not a proof of the infinite limit.


@pytest.mark.parametrize('value,trend,label', [
    (np.nan, 0, 'insufficient_data'), (np.inf, 0, 'insufficient_data'),
    (-1, 0, 'insufficient_data'), (1, np.nan, 'insufficient_data'),
    (0, 0, 'low_compliance'), (.3, 0, 'intermediate_compliance'),
    (.5, -.2, 'declining_compliance'), (1, 0, 'higher_compliance'),
])
def test_descriptive_categories(value, trend, label):
    assert classify_compliance(value, trend) == label


def test_empty_and_invalid_cycles_are_insufficient_data():
    assert summarize_compliance([]).classification == 'insufficient_data'
    empty = BreathCycle(*(np.array([]) for _ in range(4)))
    assert summarize_compliance([empty]).classification == 'insufficient_data'
    flat = BreathCycle(np.arange(3.), np.ones(3), np.ones(3), np.arange(3.))
    assert summarize_compliance([flat]).classification == 'insufficient_data'


def test_temporal_flow_derivative_units_and_evolution():
    t = np.arange(10.) * .2
    flow = 3*t + 2  # dQ/dt = 3 mL/s^2
    np.testing.assert_allclose(squared_flow_time_derivative(flow, .2), 9)
    cycle = BreathCycle(t, t+1, flow, t)
    means, peaks = flow_derivative_evolution([cycle], .2)
    np.testing.assert_allclose(means, [9])
    np.testing.assert_allclose(peaks, [9])


@pytest.mark.parametrize('flow,dt', [([], 1), ([1], 1), ([1, np.nan], 1), ([1, 2], 0), ([1, 2], np.inf)])
def test_invalid_derivative_inputs(flow, dt):
    with pytest.raises(ValueError):
        squared_flow_time_derivative(flow, dt)


def test_energy_per_length_and_response_use_declared_units():
    area = np.pi * (CONST.airway_diameter_trachea / 2)**2
    np.testing.assert_allclose(kinetic_energy_per_length(np.array([1e6])), [.5 * CONST.rho_air / area])
    assert surface_tension_response(.1, 0) == .1
    assert surface_tension_response(.1, .5) == .05


def test_synthetic_pipeline_and_retired_threshold():
    recording = generate_synthetic_waveform(n_breaths=6, compliance_decay=.01, seed=42)
    state = summarize_compliance(segment_breaths(recording))
    assert state.classification != 'insufficient_data'
    assert np.isfinite(state.compliance)
    with pytest.raises(NotImplementedError):
        estimate_critical_constant(np.array([1.]), np.array([.1]))


@pytest.mark.parametrize('gamma,r', [(-1, 1), (np.nan, 1), (1, 0), (1, np.inf)])
def test_invalid_static_pressure(gamma, r):
    with pytest.raises(ValueError):
        static_sphere_pressure(gamma, r)
