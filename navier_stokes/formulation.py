"""Synthetic respiratory descriptors and elementary spherical identities.

No diagnostic here determines spatial Navier-Stokes regularity. Pressure,
flow and volume traces do not reconstruct a three-dimensional velocity field.
All examples are teaching instruments, not validated for patient care.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# Physical constants for neonatal respiratory flow
# ============================================================

@dataclass(frozen=True)
class NeonatalConstants:
    """Illustrative fixed parameters; not patient-specific or clinically calibrated."""
    rho_air: float = 1.2           # kg/m^3 (humidified, body temp)
    nu_air: float = 1.5e-5         # m^2/s kinematic viscosity
    gamma_surfactant: float = 0.025    # N/m surface tension WITH surfactant
    gamma_no_surfactant: float = 0.070 # N/m surface tension WITHOUT
    alveolar_radius_term: float = 50e-6    # m (50 um, term infant)
    alveolar_radius_preterm: float = 30e-6 # m (30 um, 28 weeks)
    airway_diameter_trachea: float = 3.5e-3  # m (neonatal trachea ~3.5mm)
    typical_tidal_volume: float = 5e-6   # m^3 (5 mL for 1kg infant)
    respiratory_rate: float = 40.0       # breaths/min (typical preterm)


CONST = NeonatalConstants()


# ============================================================
# Static spherical pressure identity
# ============================================================

def laplace_pressure(gamma: float, radius: float) -> float:
    """Spherical static pressure jump 2*gamma/r, in Pa for N/m and m.

    At every fixed positive gamma this diverges as r approaches zero.
    Reducing gamma to another positive constant changes the coefficient,
    not that limit. This identity supplies no radius evolution equation."""
    _positive(radius, 'radius')
    _nonnegative(gamma, 'gamma')
    return 2.0 * gamma / radius


def pressure_reference_radius(gamma: float, p_max: float) -> float:
    """Radius at which 2*gamma/r equals a chosen positive pressure, not a collapse threshold."""
    _positive(p_max, 'p_max')
    _nonnegative(gamma, 'gamma')
    return 2.0 * gamma / p_max


def capillary_pressure_ratio(gamma: float, r_min: float, nu: float, L: float) -> float:
    """Dimensionless ratio (gamma/r)/(rho*nu**2/L**2).

    Uses half the spherical pressure jump by convention. It is a scale
    comparison, not a regularity criterion or calibrated clinical score."""
    rho = CONST.rho_air
    for value, name in ((r_min, 'r_min'), (nu, 'nu'), (L, 'L')):
        _positive(value, name)
    _nonnegative(gamma, 'gamma')
    return (gamma / r_min) * (L ** 2) / (rho * nu ** 2)


# ============================================================
# Reynolds number in neonatal airways
# ============================================================

def reynolds_number(Q: float, d: float, nu: float = CONST.nu_air) -> float:
    """Bulk Re = abs(Q)/A * d/nu; Q in m^3/s, d in m. No regularity inference."""
    _positive(d, "d")
    _positive(nu, "nu")
    if not np.isfinite(Q):
        raise ValueError("Q must be finite")
    A = np.pi * (d / 2) ** 2
    u = abs(Q) / A if A > 0 else 0.0
    return u * d / nu


# ============================================================
# Synthetic cycle descriptors
# ============================================================

@dataclass
class BreathCycle:
    """Synthetic cycle: time s, pressure cmH2O, flow mL/s, volume mL. Not clinical validation."""
    time: np.ndarray        # seconds within cycle
    pressure: np.ndarray    # cmH2O
    flow: np.ndarray        # mL/s
    volume: np.ndarray      # mL (integrated)

    @property
    def valid(self) -> bool:
        """Whether aligned finite arrays contain at least two ordered samples."""
        arrays = [np.asarray(x) for x in (self.time, self.pressure, self.flow, self.volume)]
        return (all(x.ndim == 1 and len(x) == len(arrays[0]) and
                    np.all(np.isfinite(x)) for x in arrays)
                and len(arrays[0]) >= 2 and bool(np.all(np.diff(arrays[0]) > 0)))

    @property
    def dynamic_compliance(self) -> float:
        """C_dyn = delta_V / delta_P [mL/cmH2O]"""
        if not self.valid:
            return float("nan")
        dV = np.max(self.volume) - np.min(self.volume)
        dP = np.max(self.pressure) - np.min(self.pressure)
        return dV / dP if dP > 0 else float("nan")

    @property
    def resistance(self) -> float:
        """R = delta_P / Q_peak [cmH2O / (mL/s)]"""
        Q_peak = np.max(np.abs(self.flow))
        dP = np.max(self.pressure) - np.min(self.pressure)
        return dP / Q_peak if Q_peak > 0 else float('inf')

    @property
    def time_constant(self) -> float:
        """tau = R * C [seconds]"""
        return self.resistance * self.dynamic_compliance

    @property
    def work_of_breathing(self) -> float:
        """W = integral(P dV) [cmH2O * mL]"""
        _trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        return float(_trapz(self.pressure, self.volume))

    @property
    def phase_area(self) -> float:
        """Absolute integral P dV [cmH2O*mL]; geometric descriptor, not a PDE diagnostic."""
        _trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        return abs(float(_trapz(self.pressure, self.volume)))


# ============================================================
# Compliance descriptors
# ============================================================

@dataclass
class ComplianceState:
    """Descriptive synthetic compliance summary; thresholds have no clinical validation."""
    compliance: float           # mL/cmH2O
    compliance_trend: float     # mL/cmH2O per breath
    capillary_ratio: float         # dimensionless scale ratio
    re_max: float              # max Reynolds number in cycle
    pv_loop_area: float        # phase space area
    classification: str         # descriptive category or insufficient_data


def classify_compliance(
    compliance: float,
    compliance_trend: float,
    c_threshold_low: float = 0.3,   # illustrative mL/cmH2O threshold
    c_threshold_high: float = 1.0,  # illustrative mL/cmH2O threshold
) -> str:
    """Describe compliance using illustrative thresholds in mL/cmH2O.

    Trend units are mL/cmH2O per breath. Missing/nonfinite or negative
    compliance yields insufficient_data. These labels imply no treatment
    decision, PDE regularity or patient-specific diagnosis."""
    if not (0 < c_threshold_low < c_threshold_high < float("inf")):
        raise ValueError("thresholds must be finite, positive and increasing")
    if not np.isfinite(compliance) or not np.isfinite(compliance_trend) or compliance < 0:
        return 'insufficient_data'
    if compliance < c_threshold_low:
        return 'low_compliance'
    if compliance < c_threshold_high:
        return 'declining_compliance' if compliance_trend < -0.1 else 'intermediate_compliance'
    return 'higher_compliance'


# ============================================================
# Illustrative surface-tension response
# ============================================================

def surface_tension_response(
    gamma_0: float,
    surfactant_concentration: float,
    c_half: float = 0.5,
) -> float:
    """Illustrative saturating response gamma_0*c_half/(c+c_half).

    Concentration and c_half share arbitrary units. Not a dose-response
    calibration or a proof of smoothing. Positive finite gamma still
    leaves the 2*gamma/r limit unbounded as r approaches zero."""
    _nonnegative(gamma_0, 'gamma_0')
    _nonnegative(surfactant_concentration, 'surfactant_concentration')
    _positive(c_half, 'c_half')
    return gamma_0 * c_half / (surfactant_concentration + c_half)


# ============================================================
# Plug-flow energy per unit length
# ============================================================

def kinetic_energy_per_length(
    flow: np.ndarray,
) -> np.ndarray:
    """Kinetic energy per unit length [J/m] under a uniform plug-flow assumption.

    Flow input is mL/s; a fixed illustrative cross-section A is assumed.
    Returns rho*Q_SI**2/(2*A), not total energy or an NS energy balance."""
    rho = CONST.rho_air
    A_eff = np.pi * (CONST.airway_diameter_trachea / 2) ** 2
    flow_m3s = np.asarray(flow, dtype=float) * 1e-6  # mL/s -> m^3/s
    kinetic = 0.5 * rho * (flow_m3s ** 2) / A_eff

    return kinetic


def squared_flow_time_derivative(flow: np.ndarray, dt: float) -> np.ndarray:
    """Squared temporal derivative of scalar flow, (dQ/dt)^2.

    For Q in mL/s and dt in seconds, units are mL^2/s^4. A temporal
    scalar derivative is not spatial curl or enstrophy. Requires a finite
    one-dimensional signal with at least two samples and positive dt."""
    _positive(dt, 'dt')
    flow = np.asarray(flow, dtype=float)
    if flow.ndim != 1 or len(flow) < 2 or not np.all(np.isfinite(flow)):
        raise ValueError("flow must contain at least two finite samples")
    dQdt = np.gradient(flow, dt)
    return dQdt ** 2


def _positive(value: float, name: str) -> None:
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")


def _nonnegative(value: float, name: str) -> None:
    if not np.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")


def sphere_volume_rate(radius: float, radial_speed: float) -> float:
    """d(4*pi*r^3/3)/dt = 4*pi*r^2*r_dot [m^3/s].

    For a closed material boundary this equals integral(u.n dS).
    Incompressibility and the divergence theorem require zero flux,
    so a positive-radius material sphere cannot shrink or expand.
    Nonzero output is an incompatibility check, not an admissible solution.
    """
    _positive(radius, 'radius')
    if not np.isfinite(radial_speed):
        raise ValueError('radial_speed must be finite')
    return float(4 * np.pi * radius**2 * radial_speed)


def static_sphere_pressure(gamma: float, radius: float, p_ext: float = 0.0) -> float:
    """Pressure of a stationary spherical equilibrium, p_ext + 2*gamma/r.

    Outward n and kappa=2/r; stress T=-p I+2*mu*D(u).
    Traction convention: (T_in-T_out)n = -gamma*kappa*n,
    with T_out=-p_ext I. For u=0, constant p and zero body force,
    the bulk PDE, incompressibility, kinematic and traction conditions
    hold for every finite gamma>=0 and radius>0. No universal gamma
    threshold can force all these equilibria to blow up. This does
    not disprove an existential claim about other initial data.
    """
    if not np.isfinite(p_ext):
        raise ValueError('p_ext must be finite')
    return float(p_ext + laplace_pressure(gamma, radius))
