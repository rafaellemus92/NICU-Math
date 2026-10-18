"""Synthetic count/timing regressions; these are not clinical validation."""
import numpy as np
import pytest
from dataclasses import replace
from navier_stokes.analysis import estimate_decay_exponent, summarize_compliance

from navier_stokes.ventilator_ingest import generate_synthetic_waveform, segment_breaths


@pytest.mark.parametrize('noise', [0.0, 0.05])
def test_reported_50_breath_regression(noise):
    recording = generate_synthetic_waveform(n_breaths=50, compliance=1.0,
                                            noise_level=noise, seed=42)
    cycles = segment_breaths(recording)
    assert len(cycles) == 50


@pytest.mark.parametrize('seed', [7, 42, 2026])
@pytest.mark.parametrize('noise', [0., .01, .05])
@pytest.mark.parametrize('rate', [100., 200., 1000.])
def test_counts_and_timing_across_sampling_and_noise(seed, noise, rate):
    recording = generate_synthetic_waveform(n_breaths=20, noise_level=noise, seed=seed, sample_rate=rate)
    cycles = segment_breaths(recording)
    assert len(cycles) == 20
    # Detector sees pressure and edge declarations, never interior ground truth.
    np.testing.assert_allclose([c.time[0] for c in cycles], np.arange(20)*1.5, atol=1/rate, rtol=0)
    np.testing.assert_allclose([len(c.time)/rate for c in cycles], 1.5, atol=1/rate, rtol=0)


@pytest.mark.parametrize('seed,rate,rr,noise', [(11, 125., 30., .05), (103, 250., 60., .05), (987, 333., 45., .1)])
def test_held_out_seeds_rates_and_periods(seed, rate, rr, noise):
    recording = generate_synthetic_waveform(n_breaths=17, noise_level=noise, seed=seed,
                                            sample_rate=rate, respiratory_rate=rr)
    cycles = segment_breaths(recording)
    period = round(60/rr*rate)/rate
    assert len(cycles) == 17
    np.testing.assert_allclose([c.time[0] for c in cycles], np.arange(17)*period, atol=1/rate, rtol=0)


def test_unknown_or_cropped_edges_are_not_invented():
    recording = generate_synthetic_waveform(n_breaths=5, noise_level=0)
    unknown = replace(recording, starts_at_cycle_boundary=False, ends_at_cycle_boundary=False)
    cycles = segment_breaths(unknown)
    assert len(cycles) == 3  # only complete onset-to-onset intervals
    np.testing.assert_allclose([c.time[0] for c in cycles], [1.5, 3, 4.5])
    cropped = replace(unknown, **{name: getattr(unknown, name)[50:-50]
                                 for name in ('time', 'pressure', 'flow', 'volume')})
    assert len(segment_breaths(cropped)) == 3
    # A record ending during inspiration cannot claim a complete expiration.
    short = replace(recording, **{name: getattr(recording, name)[:20]
                                 for name in ('time', 'pressure', 'flow', 'volume')})
    assert segment_breaths(short) == []


@pytest.mark.parametrize('rate', [100., 200., 1000.])
@pytest.mark.parametrize('C', [.05, .1, .3, 1., 2.])
def test_noiseless_flow_volume_balance_and_finite_cycle_descriptor(rate, C):
    recording = generate_synthetic_waveform(n_breaths=8, noise_level=0, compliance=C, sample_rate=rate)
    n = int(1.5*rate)
    # Q is interval-averaged, V is at left edges. Units mL/s * s = mL.
    np.testing.assert_allclose(np.diff(recording.volume), recording.flow[:-1]/rate, atol=1e-12, rtol=1e-12)
    # 1e-10 mL allows accumulated float64 cancellation for volumes <=30 mL.
    np.testing.assert_allclose(recording.flow.reshape(8, n).sum(axis=1)/rate, 0, atol=1e-10)
    tau = .08*C
    A, B = np.exp(-.525/tau), np.exp(-.975/tau)
    expected = C*(1-A)*(1-B)/(1-A*B)
    measured = summarize_compliance(segment_breaths(recording)).compliance
    assert abs(measured-expected) <= .015  # finite sampling, not parameter calibration
    # Distinct low-C waveforms: no hidden tau=.01 floor.
    tau_inferred = -(1/rate)/np.log(recording.flow[1]/recording.flow[0])
    assert tau_inferred == pytest.approx(tau, rel=1e-9)


def test_descriptor_converges_towards_analytical_finite_cycle_value():
    C, tau = 2., .16
    A, B = np.exp(-.525/tau), np.exp(-.975/tau)
    expected = C*(1-A)*(1-B)/(1-A*B)
    errors = []
    for rate in (100., 200., 1000.):
        recording = generate_synthetic_waveform(n_breaths=4, noise_level=0, compliance=C, sample_rate=rate)
        errors.append(abs(summarize_compliance(segment_breaths(recording)).compliance-expected))
    assert errors[0] < .015
    assert errors[1] <= errors[0] + 1e-12
    assert errors[2] <= errors[1] + 1e-12
    assert errors[-1] < 1e-10  # the phase boundary lands exactly on these refined grids


def test_noise_is_reproducible_but_not_detrended_or_claimed_unbiased():
    kwargs = dict(n_breaths=10, seed=103, noise_level=.05)
    a, b = generate_synthetic_waveform(**kwargs), generate_synthetic_waveform(**kwargs)
    np.testing.assert_array_equal(a.flow, b.flow)
    np.testing.assert_allclose(np.diff(a.volume), a.flow[:-1]/100., atol=1e-12)
    assert abs(a.flow.sum()/100.) > .01  # measurement-noise integral is retained
    descriptor = summarize_compliance(segment_breaths(a)).compliance
    assert abs(descriptor - 1.) > .01  # no claim of unbiased recovery of prescribed C


@pytest.mark.parametrize('series,status', [
    ([10, 8, 6, 4, .1], 'unresolved'),
    ([1]*5, 'unresolved'), ([1, 2, 3, 4, 5], 'unresolved'),
    ([], 'invalid'), ([1, 2, np.nan, 4, 5], 'invalid'), ([1, 2, 0, 4, 5], 'invalid'),
])
def test_decay_does_not_manufacture_fit(series, status):
    result = estimate_decay_exponent(np.array(series))
    assert result.status == status
    assert result.exponent is None and result.horizon is None
    assert result.reason


def test_descriptive_decay_fit_and_offset():
    series = 20.-np.arange(10.)
    result = estimate_decay_exponent(series)
    assert result.status == 'resolved'
    assert result.exponent == pytest.approx(1.)
    assert result.horizon == pytest.approx(20.)
    assert estimate_decay_exponent(series, t0=2).horizon == pytest.approx(18.)
    assert estimate_decay_exponent(series, t0=-1).status == 'invalid'


@pytest.mark.parametrize('kwargs', [{'sample_rate':0}, {'resistance':0}, {'noise_level':-1},
                                    {'compliance':float('nan')}, {'pip':4}, {'n_breaths':2.5}])
def test_invalid_generator_domain(kwargs):
    with pytest.raises(ValueError):
        generate_synthetic_waveform(**kwargs)


def test_perturbed_unknown_leading_inspiration_is_discarded():
    full = generate_synthetic_waveform(n_breaths=5, noise_level=0)
    cropped = replace(full, **{name: getattr(full, name)[20:].copy()
                              for name in ('time', 'pressure', 'flow', 'volume')},
                      starts_at_cycle_boundary=False, ends_at_cycle_boundary=False)
    cropped.pressure[0] = 14.0  # below upper threshold, not a confirmed low phase
    cycles = segment_breaths(cropped)
    np.testing.assert_allclose([c.time[0] for c in cycles], [1.5, 3, 4.5])


def test_unknown_record_starting_in_expiration_can_arm_next_onset():
    full = generate_synthetic_waveform(n_breaths=5, noise_level=0)
    cropped = replace(full, **{name: getattr(full, name)[100:]
                              for name in ('time', 'pressure', 'flow', 'volume')},
                      starts_at_cycle_boundary=False, ends_at_cycle_boundary=False)
    cycles = segment_breaths(cropped)
    np.testing.assert_allclose([c.time[0] for c in cycles], [1.5, 3, 4.5])


def test_old_positional_flow_threshold_cannot_become_a_duration():
    full = generate_synthetic_waveform(n_breaths=2, noise_level=0)
    with pytest.raises(TypeError):
        segment_breaths(full, .5)
