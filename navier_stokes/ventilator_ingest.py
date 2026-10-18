"""Synthetic waveform fixtures and legacy local CSV parsing.

Use synthetic data only. Existing metadata fields and parsers are not a
privacy guarantee or approval for patient-data processing. Database/schema
review is separate; this task neither enables nor accesses a database."""

import csv
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple

from .formulation import BreathCycle


@dataclass
class PatientContext:
    """Legacy metadata structure, used here only for fictional synthetic fixtures."""
    gestational_age_weeks: float     # e.g., 28.3
    birth_weight_grams: int          # e.g., 980
    postnatal_age_days: int          # e.g., 2
    surfactant_given: bool = False
    surfactant_doses: int = 0
    ventilator_mode: str = ''        # e.g., 'SIMV', 'HFOV', 'CPAP'
    fio2: float = 0.21
    peep: float = 5.0               # cmH2O
    notes: str = ''


@dataclass
class WaveformRecording:
    """A continuous ventilator waveform recording."""
    patient: PatientContext
    sample_rate_hz: float           # typically 100 or 200
    time: np.ndarray                # seconds from recording start
    pressure: np.ndarray            # cmH2O
    flow: np.ndarray                # mL/s
    volume: Optional[np.ndarray] = None  # mL (computed if not provided)

    # Only a synthetic generator or a caller with known acquisition boundaries
    # may assert these. Interior ground truth is never used by segmentation.
    starts_at_cycle_boundary: bool = False
    ends_at_cycle_boundary: bool = False

    def __post_init__(self):
        if self.volume is None:
            # Flow samples are interval averages; V[k] is at interval start.
            dt = 1.0 / self.sample_rate_hz
            self.volume = np.concatenate(([0.0], np.cumsum(self.flow[:-1]) * dt)) if len(self.flow) else np.array([])


def load_csv_waveform(
    filepath: Path,
    patient: PatientContext,
    time_col: str = 'time',
    pressure_col: str = 'pressure',
    flow_col: str = 'flow',
    volume_col: Optional[str] = None,
    sample_rate_hz: float = 100.0,
) -> WaveformRecording:
    """Read a local synthetic fixture CSV: seconds, cmH2O, mL/s, optional mL. Not approved for patient data."""
    time_vals = []
    pressure_vals = []
    flow_vals = []
    volume_vals = []

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_vals.append(float(row.get(time_col, 0)))
            pressure_vals.append(float(row.get(pressure_col, 0)))
            flow_vals.append(float(row.get(flow_col, 0)))
            if volume_col and volume_col in row:
                volume_vals.append(float(row[volume_col]))

    return WaveformRecording(
        patient=patient,
        sample_rate_hz=sample_rate_hz,
        time=np.array(time_vals),
        pressure=np.array(pressure_vals),
        flow=np.array(flow_vals),
        volume=np.array(volume_vals) if volume_vals else None,
    )


def segment_breaths(
    recording: WaveformRecording,
    *,
    min_phase_seconds: float = 0.04,
    min_cycle_seconds: float = 0.3,
) -> List[BreathCycle]:
    """Segment pressure-driven synthetic cycles using pressure hysteresis.

    The 10th/90th pressure percentiles define a robust span. Confirm at
    least min_phase_seconds below 30% of this span before accepting a run
    above 70% lasting the same duration. Onsets are the first samples of
    confirmed high runs, separated by min_cycle_seconds. Flow is not used
    to count breaths: its noisy near-zero tails formerly created fragments.

    Return onset-to-onset cycles, with timestamps relative to recording
    origin (not reset per cycle). Discard the initial high phase if its
    onset predates the recording. Include the first/final acquisition edge
    only when explicitly marked as a known cycle boundary. Unknown trailing
    cycles are discarded even if expiration appears complete. No padding
    or invented samples. Partial records must clear the boundary flags.

    This requires distinct pressure phases lasting >=40 ms and cycles
    >=300 ms at the defaults. It is not a general detector for spontaneous
    breathing, variable baselines, high-frequency ventilation or patient data.
    """
    if not np.isfinite(recording.sample_rate_hz) or recording.sample_rate_hz <= 0:
        raise ValueError('sample_rate_hz must be finite and positive')
    if (not np.isfinite(min_phase_seconds) or min_phase_seconds <= 0 or
            not np.isfinite(min_cycle_seconds) or min_cycle_seconds <= 0):
        raise ValueError('phase and cycle durations must be finite and positive')
    arrays = [np.asarray(x, dtype=float) for x in
              (recording.time, recording.pressure, recording.flow, recording.volume)]
    if any(x.ndim != 1 or len(x) != len(arrays[0]) or not np.all(np.isfinite(x)) for x in arrays):
        raise ValueError('waveforms must be aligned finite one-dimensional arrays')
    time, pressure, flow, volume = arrays
    if len(time) < 2:
        return []
    dt = 1.0 / recording.sample_rate_hz
    if not np.allclose(np.diff(time), dt, rtol=1e-6, atol=1e-10):
        raise ValueError('timestamps must match the uniform sample rate')
    low, high = np.quantile(pressure, [0.1, 0.9])
    span = high - low
    if span <= np.finfo(float).eps * max(1.0, abs(low), abs(high)) * 10:
        return []
    lower, upper = low + .3 * span, low + .7 * span
    dwell = max(1, int(np.ceil(min_phase_seconds / dt)))
    separation = max(1, int(np.ceil(min_cycle_seconds / dt)))
    onsets = []
    armed, low_run, high_run = recording.starts_at_cycle_boundary, 0, 0
    for i, pressure_i in enumerate(pressure):
        if not armed:
            low_run = low_run + 1 if pressure_i <= lower else 0
            if low_run >= dwell:
                armed, high_run = True, 0
        else:
            high_run = high_run + 1 if pressure_i >= upper else 0
            if high_run >= dwell:
                onset = i - dwell + 1
                known_start = onset == 0 and recording.starts_at_cycle_boundary
                # A high run already present at t=0 may be an incomplete breath.
                if (onset > 0 or known_start) and (not onsets or onset - onsets[-1] >= separation):
                    onsets.append(onset)
                armed, low_run, high_run = False, 0, 0
    ends = onsets[1:]
    if recording.ends_at_cycle_boundary and onsets:
        ends = ends + [len(time)]
    cycles = []
    for start, end in zip(onsets, ends):
        # Require both a confirmed inspiration and a confirmed expiration.
        tail = pressure[start:end]
        low_count = 0
        has_expiration = False
        for value in tail:
            low_count = low_count + 1 if value <= lower else 0
            has_expiration |= low_count >= dwell
        if end - start < separation or not has_expiration:
            continue
        cycles.append(BreathCycle(time=time[start:end], pressure=pressure[start:end],
                                 flow=flow[start:end], volume=volume[start:end] - volume[start]))
    return cycles


def breath_summary(cycles: List[BreathCycle]) -> dict:
    """Summary statistics across all breath cycles in a recording."""
    if not cycles:
        return {}

    compliances = [c.dynamic_compliance for c in cycles]
    resistances = [c.resistance for c in cycles]
    taus = [c.time_constant for c in cycles]
    areas = [c.phase_area for c in cycles]

    return {
        'n_breaths': len(cycles),
        'compliance_mean': float(np.mean(compliances)),
        'compliance_std': float(np.std(compliances)),
        'compliance_trend': float(np.polyfit(range(len(compliances)), compliances, 1)[0]),
        'resistance_mean': float(np.mean(resistances)),
        'time_constant_mean': float(np.mean(taus)),
        'pv_area_mean': float(np.mean(areas)),
        'pv_area_trend': float(np.polyfit(range(len(areas)), areas, 1)[0]),
    }


# ============================================================
# Synthetic waveform generator for testing
# ============================================================

def generate_synthetic_waveform(
    n_breaths: int = 100,
    sample_rate: float = 100.0,
    respiratory_rate: float = 40.0,  # requested breaths/min
    compliance: float = 1.0,         # prescribed C0, mL/cmH2O
    resistance: float = 80.0,        # cmH2O/(L/s)
    peep: float = 5.0,              # baseline pressure, cmH2O
    pip: float = 20.0,              # inspiratory pressure, cmH2O
    compliance_decay: float = 0.0,  # prescribed fractional decrement/breath
    noise_level: float = 0.05,
    seed: Optional[int] = None,
) -> WaveformRecording:
    """Sample a prescribed square-pressure, linear RC teaching model.

    On each breath, C=max(C0*(1-decay*b), 0.05) mL/cmH2O and
    R_mL=R*1e-3. Solve R_mL*dV/dt + V/C = P-PEEP exactly on
    each constant-pressure phase, with inspiration lasting 35% of a cycle.
    Tau is R_mL*C, with no numerical floor. Volume is continuous across
    phase/breath boundaries; for constant C the initial volume is the
    periodic steady-state value. PEEP defines the excess-volume baseline.

    Period is rounded to the nearest sampling interval (at least 20
    samples), so realized rate can differ slightly from the request.
    V[k] is the left-edge excess volume; Q[k]=(V[k+1]-V[k])/dt is
    interval-average flow in mL/s. Pressure is also interval averaged.
    These conventions preserve integrated flow without endpoint phase
    misalignment. First/final acquisition edges are known cycle boundaries.

    Independent Gaussian measurement noise is added to pressure and flow;
    flow noise is integrated into volume without artificial detrending.
    Noise breaks the exact RC relation and can bias the volume/pressure
    range descriptor. That descriptor is not the prescribed C. A specified
    seed gives reproducibility; seed=None does not. No disease, treatment,
    Navier-Stokes, or patient-specific predictive model is claimed.
    """
    if isinstance(n_breaths, bool) or not isinstance(n_breaths, (int, np.integer)) or n_breaths < 1:
        raise ValueError('n_breaths must be a positive integer')
    for name, value in (('sample_rate', sample_rate), ('respiratory_rate', respiratory_rate),
                        ('compliance', compliance), ('resistance', resistance)):
        if not np.isfinite(value) or value <= 0:
            raise ValueError(f'{name} must be finite and positive')
    for name, value in (('compliance_decay', compliance_decay), ('noise_level', noise_level)):
        if not np.isfinite(value) or value < 0:
            raise ValueError(f'{name} must be finite and nonnegative')
    if not np.isfinite(peep) or not np.isfinite(pip) or pip <= peep:
        raise ValueError('finite pip > peep is required')
    n = int(round(60.0 / respiratory_rate * sample_rate))
    if n < 20:
        raise ValueError('at least 20 samples per cycle are required')
    dt, R = 1.0 / sample_rate, resistance * 1e-3
    period = n * dt
    ti, te = .35 * period, .65 * period
    dP = pip - peep
    edges = np.arange(n + 1) * dt
    rng = np.random.default_rng(seed)
    initial_tau = R * max(compliance, .05)
    initial_volume = (max(compliance, .05) * dP * (-np.expm1(-ti / initial_tau)) *
                      np.exp(-te / initial_tau) / (-np.expm1(-period / initial_tau)))
    v_start = initial_volume
    pressures, flows = [], []
    for b in range(n_breaths):
        C = max(compliance * (1.0 - compliance_decay * b), .05)
        tau = R * C
        if not np.isfinite(tau) or tau <= 0:
            raise ValueError('R*C must be representable and positive')
        v_peak = v_start + (C * dP - v_start) * (-np.expm1(-ti / tau))
        values = np.where(edges <= ti,
                          v_start + (C * dP - v_start) * (-np.expm1(-np.minimum(edges, ti) / tau)),
                          v_peak * np.exp(-np.maximum(edges - ti, 0) / tau))
        q = np.diff(values) / dt
        fraction_high = np.clip((ti - edges[:-1]) / dt, 0, 1)
        p = peep + dP * fraction_high
        p += rng.normal(0, noise_level * dP, n)
        q += rng.normal(0, noise_level * np.max(np.abs(q)), n)
        pressures.append(p)
        flows.append(q)
        v_start = values[-1]
    flow = np.concatenate(flows)
    volume = initial_volume + np.concatenate(([0.0], np.cumsum(flow[:-1]) * dt))
    patient = PatientContext(gestational_age_weeks=28.0, birth_weight_grams=1000,
                             postnatal_age_days=1, ventilator_mode='RC_synthetic',
                             notes=f'synthetic prescribed C0={compliance}; decay={compliance_decay}')
    return WaveformRecording(patient=patient, sample_rate_hz=sample_rate,
                             time=np.arange(len(flow)) * dt, pressure=np.concatenate(pressures),
                             flow=flow, volume=volume, starts_at_cycle_boundary=True,
                             ends_at_cycle_boundary=True)
