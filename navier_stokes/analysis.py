"""Descriptive analysis of synthetic waveforms. No PDE or clinical diagnostic is inferred."""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

from .formulation import (
    BreathCycle, ComplianceState, classify_compliance,
    capillary_pressure_ratio, kinetic_energy_per_length, squared_flow_time_derivative,
    CONST,
)


# ============================================================
# 1. Compliance time-series analysis
# ============================================================

@dataclass
class ComplianceTrend:
    """Result of compliance trend analysis over a window of breaths."""
    values: np.ndarray
    times: np.ndarray          # breath index or timestamp
    slope: float               # linear trend (negative = deteriorating)
    half_life: Optional[float] # breaths until compliance halves (if declining)
    curvature: float           # second derivative — acceleration of decline
    changepoints: List[int]    # indices where trend shifts significantly


def analyze_compliance_trend(
    cycles: List[BreathCycle],
    window: int = 20,
) -> ComplianceTrend:
    """Fit descriptive linear/quadratic trends, not a collapse or singularity predictor."""
    compliances = np.array([c.dynamic_compliance for c in cycles])
    indices = np.arange(len(compliances), dtype=float)

    if len(compliances) < 3 or not np.all(np.isfinite(compliances)):
        return ComplianceTrend(
            values=compliances, times=indices,
            slope=float("nan"), half_life=None, curvature=float("nan"), changepoints=[],
        )

    # Linear trend
    coeffs = np.polyfit(indices, compliances, 1)
    slope = coeffs[0]

    # Quadratic fit for curvature
    if len(compliances) >= 5:
        q_coeffs = np.polyfit(indices, compliances, 2)
        curvature = 2.0 * q_coeffs[0]  # second derivative of at^2+bt+c
    else:
        curvature = 0.0

    # Half-life estimate (breaths until compliance halves)
    half_life = None
    if slope < 0 and compliances[0] > 0:
        half_life = -compliances[0] / (2.0 * slope)

    # Change-point detection: sliding window variance ratio
    changepoints = _detect_changepoints(compliances, window)

    return ComplianceTrend(
        values=compliances,
        times=indices,
        slope=slope,
        half_life=half_life,
        curvature=curvature,
        changepoints=changepoints,
    )


def _detect_changepoints(series: np.ndarray, window: int) -> List[int]:
    """Heuristic mean shifts exceeding twice the full-series standard deviation; no causal attribution."""
    if len(series) < 2 * window:
        return []

    sigma = np.std(series)
    if sigma < 1e-12:
        return []

    changepoints = []
    for i in range(window, len(series) - window):
        left_mean = np.mean(series[i - window:i])
        right_mean = np.mean(series[i:i + window])
        if abs(right_mean - left_mean) > 2.0 * sigma:
            if not changepoints or i - changepoints[-1] >= window:
                changepoints.append(i)

    return changepoints


@dataclass(frozen=True)
class DecayFit:
    """Descriptive fit outcome; horizon is relative to the selected breath window.

    A resolved fit is an extrapolation under a chosen power-law form, not
    a predicted event, uncertainty bound or physiological calibration.
    Unresolved/invalid fits carry no fabricated exponent or finite horizon.
    """
    status: str
    exponent: Optional[float]
    horizon: Optional[float]
    reason: str


def estimate_decay_exponent(compliances: np.ndarray, t0: int = 0) -> DecayFit:
    """Fit only when a positive declining series extrapolates beyond its window.

    Descriptor index i represents breath interval [i,i+1), so the observed
    window ends at n, not n-1. A linear zero crossing at/before n is
    unresolved; it is never replaced by n*1.5. At least five finite positive
    values are needed. t0 selects a nonnegative integer start index.
    """
    raw = np.asarray(compliances, dtype=float)
    if raw.ndim != 1 or isinstance(t0, bool) or not isinstance(t0, (int, np.integer)) or t0 < 0:
        return DecayFit('invalid', None, None, 'expected a 1D series and nonnegative integer t0')
    c = raw[t0:]
    if len(c) < 5 or not np.all(np.isfinite(c)) or np.any(c <= 0):
        return DecayFit('invalid', None, None, 'need at least five finite positive descriptors')
    n = len(c)
    t = np.arange(n, dtype=float)
    if np.ptp(c) <= 10 * np.finfo(float).eps * np.max(c):
        return DecayFit('unresolved', None, None, 'no resolved decline')
    slope, intercept = np.polyfit(t, c, 1)
    if slope >= 0:
        return DecayFit('unresolved', None, None, 'nondeclining linear fit')
    horizon = -intercept / slope
    if not np.isfinite(horizon) or horizon <= n:
        return DecayFit('unresolved', None, None, 'linear zero crossing is not beyond the observed window')
    exponent = float(np.polyfit(np.log(horizon - t), np.log(c), 1)[0])
    if not np.isfinite(exponent) or exponent <= 0:
        return DecayFit('unresolved', None, None, 'no finite positive decay exponent')
    return DecayFit('resolved', exponent, float(horizon), 'descriptive extrapolation only')


# ============================================================
# 2. Phase-space analysis (P-V-Q trajectory)
# ============================================================

@dataclass
class PhaseSpaceMetrics:
    """Geometric properties of the P-V loop for one breath."""
    area: float                # enclosed area (hysteresis)
    eccentricity: float        # how elongated the loop is (0=circle, 1=line)
    centroid_p: float          # mean pressure
    centroid_v: float          # mean volume
    orientation: float         # principal axis angle (radians)


def pv_loop_geometry(cycle: BreathCycle) -> PhaseSpaceMetrics:
    """Describe a sampled P-V curve; area in cmH2O*mL.

    Eccentricity and orientation depend on the numerical axis units;
    these are not invariant attractor or PDE regularity measurements."""
    p = cycle.pressure
    v = cycle.volume

    # Area via shoelace formula
    area = 0.5 * abs(np.sum(p[:-1] * v[1:] - p[1:] * v[:-1]))

    # Centroid
    cp = float(np.mean(p))
    cv = float(np.mean(v))

    # PCA for eccentricity and orientation
    centered = np.column_stack([p - cp, v - cv])
    cov = np.cov(centered.T)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.sort(eigvals)[::-1]

    if eigvals[0] > 0:
        eccentricity = float(np.sqrt(1.0 - eigvals[1] / eigvals[0]))
    else:
        eccentricity = 0.0

    # Orientation: angle of principal eigenvector
    _, eigvecs = np.linalg.eigh(cov)
    orientation = float(np.arctan2(eigvecs[1, -1], eigvecs[0, -1]))

    return PhaseSpaceMetrics(
        area=float(area),
        eccentricity=eccentricity,
        centroid_p=cp,
        centroid_v=cv,
        orientation=orientation,
    )


def phase_space_trajectory(
    cycles: List[BreathCycle],
) -> List[PhaseSpaceMetrics]:
    """Compute phase-space metrics for each breath in a sequence."""
    return [pv_loop_geometry(c) for c in cycles]


def loop_metric_distance(
    metrics: List[PhaseSpaceMetrics],
    reference_idx: int = 0,
) -> np.ndarray:
    """Reference-scaled distance between loop descriptors; no dynamical attractor is reconstructed."""
    if not metrics:
        return np.array([])

    ref = metrics[reference_idx]
    ref_vec = np.array([ref.area, ref.eccentricity, ref.centroid_p,
                        ref.centroid_v, ref.orientation])

    divergences = np.zeros(len(metrics))
    for i, m in enumerate(metrics):
        vec = np.array([m.area, m.eccentricity, m.centroid_p,
                        m.centroid_v, m.orientation])
        # Normalize each component by reference magnitude
        scale = np.abs(ref_vec) + 1e-10
        divergences[i] = np.linalg.norm((vec - ref_vec) / scale)

    return divergences


# ============================================================
# 3. Temporal flow derivative analysis
# ============================================================

def flow_derivative_evolution(
    cycles: List[BreathCycle],
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Per-breath mean and peak of (dQ/dt)^2 [mL^2/s^4], not spatial enstrophy."""
    means = np.zeros(len(cycles))
    peaks = np.zeros(len(cycles))

    for i, c in enumerate(cycles):
        omega = squared_flow_time_derivative(c.flow, dt)
        means[i] = np.mean(omega)
        peaks[i] = np.max(omega)

    return means, peaks


def scaled_flow_derivative_index(
    cycles: List[BreathCycle],
    dt: float,
) -> np.ndarray:
    """Historical scaled temporal-flow index nu*mean((dQ_SI/dt)^2)/A.

    Units m^6/s^5. This is not energy dissipation and has no validated
    physiological interpretation. Prefer the unscaled derivative diagnostic."""
    nu = CONST.nu_air
    A_eff = np.pi * (CONST.airway_diameter_trachea / 2) ** 2
    rates = np.zeros(len(cycles))

    for i, c in enumerate(cycles):
        flow_m3s = c.flow * 1e-6
        dQdt = np.sqrt(squared_flow_time_derivative(flow_m3s, dt))
        rates[i] = nu * np.mean(dQdt ** 2) / A_eff

    return rates


# ============================================================
# 4. Synthetic compliance summary
# ============================================================

def summarize_compliance(
    cycles: List[BreathCycle],
    gamma: float = CONST.gamma_no_surfactant,
    r_min: float = CONST.alveolar_radius_preterm,
) -> ComplianceState:
    """Summarize synthetic compliance; missing or invalid cycles yield insufficient_data."""
    if not cycles or any(not c.valid or not np.isfinite(c.dynamic_compliance) for c in cycles):
        return ComplianceState(
            compliance=float('nan'), compliance_trend=float('nan'), capillary_ratio=float('nan'),
            re_max=float('nan'), pv_loop_area=float('nan'), classification='insufficient_data',
        )

    # Compliance
    compliances = np.array([c.dynamic_compliance for c in cycles])
    c_mean = float(np.mean(compliances))

    # Trend (slope of linear fit)
    if len(compliances) >= 3:
        slope = float(np.polyfit(range(len(compliances)), compliances, 1)[0])
    else:
        slope = 0.0

    # Pressure scale ratio
    L = CONST.airway_diameter_trachea
    lam = capillary_pressure_ratio(gamma, r_min, CONST.nu_air, L)

    # Reynolds number (max across all cycles)
    re_max = 0.0
    for c in cycles:
        Q_peak = float(np.max(np.abs(c.flow))) * 1e-6  # mL/s -> m^3/s
        from .formulation import reynolds_number
        re = reynolds_number(Q_peak, CONST.airway_diameter_trachea)
        re_max = max(re_max, re)

    # Phase space area (mean)
    areas = np.array([c.phase_area for c in cycles])
    area_mean = float(np.mean(areas))

    # Classification
    classification = classify_compliance(c_mean, slope)

    return ComplianceState(
        compliance=c_mean,
        compliance_trend=slope,
        capillary_ratio=lam,
        re_max=re_max,
        pv_loop_area=area_mean,
        classification=classification,
    )


# ============================================================
# 5. Descriptive compliance increases
# ============================================================

def detect_compliance_increases(
    cycles: List[BreathCycle],
    window: int = 10,
    improvement_threshold: float = 0.3,
) -> List[dict]:
    """Find relative increases in sliding mean compliance.

    Descriptive heuristic only: cannot identify a treatment, mechanism,
    PDE regularization or clinical response. Threshold is illustrative."""
    if len(cycles) < 2 * window:
        return []

    compliances = np.array([c.dynamic_compliance for c in cycles])
    events = []

    for i in range(window, len(compliances) - window):
        pre = np.mean(compliances[i - window:i])
        post = np.mean(compliances[i:i + window])

        if pre > 0 and (post - pre) / pre > improvement_threshold:
            events.append({
                'breath_index': i,
                'compliance_before': float(pre),
                'compliance_after': float(post),
                'improvement_ratio': float((post - pre) / pre),
                'classification_before': classify_compliance(pre, 0.0),
                'classification_after': classify_compliance(post, 0.0),
            })

    return events
