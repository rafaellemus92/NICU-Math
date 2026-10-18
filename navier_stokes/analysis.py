"""
Singularity proximity analysis for neonatal respiratory waveforms.

Given ventilator data (pressure, flow, volume at 100-200 Hz), this module
detects approach to and retreat from the compliance singularity — the
point where alveolar collapse causes a finite-time blowup analog in the
pressure field.

The core idea: compliance C_dyn = dV/dP is the measurable regularity
proxy. When C_dyn → 0, the system approaches singular behavior
(atelectasis). The rate and trajectory of compliance decline encode
the approach to blowup, and surfactant administration provides a
measurable regularization event.

Three analysis axes:
1. Time-series: compliance trend, change-point detection, decay rate
2. Phase-space: P-V loop geometry, attractor reconstruction
3. Spectral: enstrophy evolution, frequency content near collapse
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

from .formulation import (
    BreathCycle, RegularityState, classify_regularity,
    regularity_parameter, energy_from_ventilator, enstrophy_proxy,
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
    """
    Analyze the compliance trajectory over a sequence of breaths.

    Fits a local linear model and detects acceleration (curvature).
    A negative slope with negative curvature = accelerating collapse
    (the system is approaching the singularity faster than linearly).
    """
    compliances = np.array([c.dynamic_compliance for c in cycles])
    indices = np.arange(len(compliances), dtype=float)

    if len(compliances) < 3:
        return ComplianceTrend(
            values=compliances, times=indices,
            slope=0.0, half_life=None, curvature=0.0, changepoints=[],
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
    """
    Simple change-point detection via sliding-window mean shift.

    A changepoint is declared when the difference between the mean
    of the preceding and following windows exceeds 2 standard deviations
    of the full series. This catches surfactant administration events
    (sudden compliance improvement) and collapse onset (sudden decline).
    """
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


def estimate_decay_exponent(
    compliances: np.ndarray,
    t0: int = 0,
) -> Tuple[float, float]:
    """
    Fit C(t) ~ C_0 * (T* - t)^alpha near a collapse event.

    In NS blowup theory, the approach to singularity follows a
    power law. If compliance decays as (T* - t)^alpha:
      alpha > 0: finite-time singularity at t = T*
      alpha ~ 0.5: consistent with self-similar blowup
      alpha ~ 1: linear decay (less severe)

    Returns (alpha, T_star_estimate).
    """
    c = compliances[t0:]
    if len(c) < 5 or np.min(c) <= 0:
        return (0.0, 0.0)

    n = len(c)
    t = np.arange(n, dtype=float)

    # Estimate T* by extrapolating linear fit to zero
    coeffs = np.polyfit(t, c, 1)
    if coeffs[0] >= 0:
        return (0.0, float('inf'))

    T_star = -coeffs[1] / coeffs[0]
    if T_star <= n:
        T_star = n * 1.5  # singularity hasn't happened yet

    # Fit log(C) vs log(T* - t)
    dt_to_star = T_star - t
    valid = dt_to_star > 0.1
    if np.sum(valid) < 3:
        return (0.0, T_star)

    log_c = np.log(c[valid])
    log_dt = np.log(dt_to_star[valid])
    alpha_coeffs = np.polyfit(log_dt, log_c, 1)
    alpha = alpha_coeffs[0]

    return (float(alpha), float(T_star))


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
    """
    Compute geometric properties of the pressure-volume loop.

    As the system approaches singularity:
    - Area collapses (less volume exchanged per pressure swing)
    - Eccentricity increases (loop degenerates toward a line)
    - Centroid shifts to higher pressure, lower volume
    - Orientation rotates (compliance axis tilts)

    These geometric changes in phase space are the measurable
    signature of approaching blowup in the bounded NS system.
    """
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


def attractor_divergence(
    metrics: List[PhaseSpaceMetrics],
    reference_idx: int = 0,
) -> np.ndarray:
    """
    Measure how far each breath's P-V loop has diverged from a reference.

    Uses Euclidean distance in the 5D metric space
    (area, eccentricity, centroid_p, centroid_v, orientation).

    Increasing divergence = the attractor is deforming = approaching
    regime change (smooth → singular or singular → smooth after surfactant).
    """
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
# 3. Spectral / enstrophy analysis
# ============================================================

def enstrophy_evolution(
    cycles: List[BreathCycle],
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Track enstrophy proxy across breaths.

    Returns (per_breath_mean_enstrophy, per_breath_peak_enstrophy).

    In NS regularity theory, bounded enstrophy implies regularity.
    If mean enstrophy grows without bound, the solution is losing
    regularity. In the neonatal lung, this corresponds to
    increasingly violent pressure/flow oscillations as alveoli
    collapse and re-recruit.
    """
    means = np.zeros(len(cycles))
    peaks = np.zeros(len(cycles))

    for i, c in enumerate(cycles):
        omega = enstrophy_proxy(c.flow, dt)
        means[i] = np.mean(omega)
        peaks[i] = np.max(omega)

    return means, peaks


def energy_dissipation_rate(
    cycles: List[BreathCycle],
    dt: float,
) -> np.ndarray:
    """
    Estimate energy dissipation rate per breath.

    In the NS energy inequality:
        d/dt ||u||^2 + 2*nu * ||grad u||^2 = <f, u>

    The dissipation term 2*nu * ||grad u||^2 must balance the forcing.
    If dissipation cannot keep up with forcing, energy grows
    unboundedly → loss of regularity.

    We estimate dissipation from the flow signal as:
        epsilon ~ nu * mean((dQ/dt)^2) / A_eff
    """
    nu = CONST.nu_air
    A_eff = np.pi * (CONST.airway_diameter_trachea / 2) ** 2
    rates = np.zeros(len(cycles))

    for i, c in enumerate(cycles):
        flow_m3s = c.flow * 1e-6
        dQdt = np.gradient(flow_m3s, dt)
        rates[i] = nu * np.mean(dQdt ** 2) / A_eff

    return rates


# ============================================================
# 4. Singularity proximity score
# ============================================================

def singularity_proximity(
    cycles: List[BreathCycle],
    gamma: float = CONST.gamma_no_surfactant,
    r_min: float = CONST.alveolar_radius_preterm,
) -> RegularityState:
    """
    Comprehensive singularity proximity assessment.

    Combines all analysis axes into a single RegularityState
    that classifies how close the system is to blowup.

    This is the function a clinician would call on a window of
    ventilator data to get an assessment of the patient's
    respiratory regularity state.
    """
    if not cycles:
        return RegularityState(
            compliance=0.0, compliance_trend=0.0, lambda_param=float('inf'),
            re_max=0.0, pv_loop_area=0.0, classification='singular',
        )

    # Compliance
    compliances = np.array([c.dynamic_compliance for c in cycles])
    c_mean = float(np.mean(compliances))

    # Trend (slope of linear fit)
    if len(compliances) >= 3:
        slope = float(np.polyfit(range(len(compliances)), compliances, 1)[0])
    else:
        slope = 0.0

    # Regularity parameter
    L = CONST.airway_diameter_trachea
    lam = regularity_parameter(gamma, r_min, CONST.nu_air, L)

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
    classification = classify_regularity(c_mean, slope)

    return RegularityState(
        compliance=c_mean,
        compliance_trend=slope,
        lambda_param=lam,
        re_max=re_max,
        pv_loop_area=area_mean,
        classification=classification,
    )


# ============================================================
# 5. Surfactant response detection
# ============================================================

def detect_surfactant_response(
    cycles: List[BreathCycle],
    window: int = 10,
    improvement_threshold: float = 0.3,
) -> List[dict]:
    """
    Detect compliance jumps consistent with surfactant administration.

    Surfactant is the regularization operator. When administered:
    - Compliance jumps upward (the singularity is regularized)
    - P-V loop area changes characteristic shape
    - Enstrophy drops (flow becomes smoother)

    Returns a list of detected events with breath index and magnitude.
    """
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
                'classification_before': classify_regularity(pre, -0.05),
                'classification_after': classify_regularity(post, 0.05),
            })

    return events
