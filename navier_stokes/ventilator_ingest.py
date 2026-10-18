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

    def __post_init__(self):
        if self.volume is None:
            dt = 1.0 / self.sample_rate_hz
            self.volume = np.cumsum(self.flow) * dt


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
    flow_threshold: float = 0.5,
) -> List[BreathCycle]:
    """
    Segment a continuous recording into individual breath cycles.

    Uses zero-crossings in the flow signal (inspiration onset = flow
    crossing from negative to positive).
    """
    flow = recording.flow
    pressure = recording.pressure
    volume = recording.volume
    dt = 1.0 / recording.sample_rate_hz

    # Find positive zero-crossings (start of inspiration)
    crossings = []
    for i in range(1, len(flow)):
        if flow[i - 1] <= flow_threshold and flow[i] > flow_threshold:
            crossings.append(i)

    cycles = []
    for j in range(len(crossings) - 1):
        start = crossings[j]
        end = crossings[j + 1]
        if end - start < 5:
            continue

        t_cycle = np.arange(end - start) * dt
        p_cycle = pressure[start:end]
        f_cycle = flow[start:end]
        v_cycle = volume[start:end] - volume[start]  # zero-based volume

        cycles.append(BreathCycle(
            time=t_cycle,
            pressure=p_cycle,
            flow=f_cycle,
            volume=v_cycle,
        ))

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
    respiratory_rate: float = 40.0,     # breaths/min
    compliance: float = 1.0,            # mL/cmH2O
    resistance: float = 80.0,           # cmH2O/(L/s)
    peep: float = 5.0,                  # cmH2O
    pip: float = 20.0,                  # cmH2O
    compliance_decay: float = 0.0,      # prescribed fractional decrement per breath
    noise_level: float = 0.05,
    seed: Optional[int] = None,
) -> WaveformRecording:
    """Generate a prescribed RC-shaped waveform, not a Navier-Stokes solution.

    Compliance follows max(C0*(1-decay*b), 0.05) mL/cmH2O; the time
    constant is additionally floored at 0.01 s. Pressure ramps and
    inspiratory/expiratory flow resets are imposed independently, so this
    is not even a coupled solution of a single driven RC ODE. Noise is
    seeded when seed is given. No treatment or disease model is fitted.
    Synthetic teaching use only; not validated for patient care."""
    if n_breaths < 1 or int(n_breaths) != n_breaths:
        raise ValueError('n_breaths must be a positive integer')
    rng = np.random.default_rng(seed)
    breath_period = 60.0 / respiratory_rate
    ti_ratio = 0.35  # inspiratory time fraction

    all_t = []
    all_p = []
    all_q = []
    t_offset = 0.0

    for b in range(n_breaths):
        c_eff = compliance * (1.0 - compliance_decay * b)
        c_eff = max(c_eff, 0.05)  # arbitrary positive demonstration floor

        n_samples = int(breath_period * sample_rate)
        t = np.linspace(0, breath_period, n_samples, endpoint=False)

        # Pressure: square-ish wave (simplified ventilator)
        p = np.where(t < breath_period * ti_ratio, pip, peep)
        # Smooth transitions
        rise_samples = max(1, int(0.05 * sample_rate))
        for i in range(min(rise_samples, len(p))):
            frac = i / rise_samples
            p[i] = peep + (pip - peep) * frac

        # Flow from RC model: Q = dP/R * exp(-t/tau)
        tau = resistance * c_eff * 1e-3  # convert to seconds
        tau = max(tau, 0.01)
        q = np.zeros_like(t)
        # Inspiration
        insp_mask = t < breath_period * ti_ratio
        t_insp = t[insp_mask]
        q[insp_mask] = ((pip - peep) / (resistance * 1e-3)) * np.exp(-t_insp / tau)
        # Expiration
        exp_mask = ~insp_mask
        t_exp = t[exp_mask] - breath_period * ti_ratio
        q[exp_mask] = -((pip - peep) / (resistance * 1e-3)) * np.exp(-t_exp / tau)

        # Add noise
        p += rng.normal(0, noise_level * (pip - peep), len(p))
        q += rng.normal(0, noise_level * np.max(np.abs(q)), len(q))

        all_t.append(t + t_offset)
        all_p.append(p)
        all_q.append(q)
        t_offset += breath_period

    patient = PatientContext(
        gestational_age_weeks=28.0,
        birth_weight_grams=1000,
        postnatal_age_days=1,
        ventilator_mode='SIMV_synthetic',
        notes=f'synthetic, compliance_decay={compliance_decay}',
    )

    return WaveformRecording(
        patient=patient,
        sample_rate_hz=sample_rate,
        time=np.concatenate(all_t),
        pressure=np.concatenate(all_p),
        flow=np.concatenate(all_q),
    )
