"""
Navier-Stokes formulation for neonatal respiratory flow.

THE PHYSICAL SYSTEM
===================
A neonate's lung is a bounded domain Omega in R^3 — branching airways
terminating in ~30,000 alveoli (term) or far fewer (preterm). The fluid
transitions from liquid-filled (fetal) to air-filled (postnatal) at birth.

The incompressible Navier-Stokes equations govern the airflow:

    du/dt + (u . grad)u = -grad(p)/rho + nu * laplacian(u) + f
    div(u) = 0

where:
    u(x,t) = velocity field in the airway
    p(x,t) = pressure field
    rho     = air density (~1.2 kg/m^3, but varies with humidification)
    nu      = kinematic viscosity of air (~1.5e-5 m^2/s)
    f       = body forces (gravity on the fluid column, surfactant-driven
              surface tension at the air-liquid interface)

THE REGULARITY QUESTION — CLINICAL TRANSLATION
===============================================
The Millennium Problem asks: given smooth initial data u_0, does the
solution u(x,t) remain smooth for all t > 0?

In the neonatal lung, we observe three regimes:

1. SMOOTH REGIME (adequate surfactant):
   - Surface tension gamma is low (~25 mN/m with surfactant vs ~70 mN/m without)
   - Laplace pressure P = 2*gamma/r stays bounded as alveolar radius r varies
   - Flow remains laminar (Re ~ 1-100 in neonatal airways)
   - The solution stays smooth. The baby breathes.

2. SINGULAR REGIME (surfactant deficiency — RDS):
   - gamma is high (~70 mN/m)
   - As r -> 0 (alveolar collapse), P = 2*gamma/r -> infinity
   - This is a finite-time singularity analog: the pressure field develops
     a 1/r blow-up at the collapsing interface
   - Clinically: atelectasis, respiratory failure, death without intervention
   - The solution "blows up." The baby cannot breathe.

3. INTERVENTION REGIME (exogenous surfactant):
   - Artificial surfactant administered -> gamma drops
   - The 1/r singularity is regularized
   - The solution returns to smooth. The baby breathes again.

This is not metaphor. This is the Laplace-Young equation coupled to NS
in a real physical system where we can measure:
    - Pressure (ventilator data)
    - Flow (ventilator flow sensors)
    - Compliance (volume/pressure = how "smooth" the system is)
    - The regularization parameter (surfactant presence/absence)

THE CONJECTURE
==============
The neonatal lung provides empirical evidence for a conditional regularity
result: NS solutions in bounded domains with surface-tension boundary
conditions remain regular if and only if the surface tension coefficient
gamma satisfies gamma * (1/r_min) < C for some critical constant C
depending on domain geometry and Reynolds number.

Surfactant deficiency violates this condition. The clinical data
(ventilator waveforms, compliance curves) encode the approach to and
retreat from this singularity threshold.

MEASUREMENT PLAN
================
From a single ventilated neonate (N=1), the ventilator records at 100 Hz:
    - Pressure P(t)     [cmH2O]
    - Flow Q(t)         [mL/s]
    - Volume V(t)       [mL, integrated from flow]
    - FiO2              [fraction]

Derived quantities:
    - Dynamic compliance C_dyn = delta_V / delta_P
    - Resistance R = delta_P / Q_peak
    - Time constant tau = R * C_dyn
    - Work of breathing W = integral(P dV) per cycle

Phase space trajectory: (P(t), Q(t), V(t)) traces a loop each breath.
As surfactant fails, these loops deform -> the attractor changes shape.
As surfactant is given, the attractor reforms.

This is directly analogous to monitoring energy ||u||_{H^1} in NS:
compliance collapse = H^1 norm blowup = loss of regularity.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# Physical constants for neonatal respiratory flow
# ============================================================

@dataclass(frozen=True)
class NeonatalConstants:
    """Physical parameters for neonatal lung fluid dynamics."""
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
# Laplace pressure and the singularity threshold
# ============================================================

def laplace_pressure(gamma: float, radius: float) -> float:
    """
    Laplace-Young equation for a spherical alveolus.
    P = 2 * gamma / r

    This is where the singularity lives:
    as r -> 0 (alveolar collapse), P -> infinity.
    Surfactant keeps gamma low, bounding P even as r decreases.
    """
    if radius <= 0:
        return float('inf')
    return 2.0 * gamma / radius


def critical_radius(gamma: float, p_max: float) -> float:
    """
    Minimum alveolar radius before Laplace pressure exceeds p_max.
    r_crit = 2 * gamma / p_max

    Below this radius, the pressure singularity dominates and
    the alveolus collapses (atelectasis).
    """
    if p_max <= 0:
        return float('inf')
    return 2.0 * gamma / p_max


def regularity_parameter(gamma: float, r_min: float, nu: float, L: float) -> float:
    """
    Dimensionless regularity parameter Lambda.

    Lambda = (gamma / r_min) * (L^2 / (rho * nu^2))

    When Lambda >> 1, surface tension forces dominate viscous dissipation
    and the solution approaches singular behavior.
    When Lambda << 1, viscosity regularizes the flow.

    This is the neonatal analog of the Reynolds number for the
    surface-tension-driven blowup mechanism.
    """
    rho = CONST.rho_air
    if r_min <= 0 or nu <= 0:
        return float('inf')
    return (gamma / r_min) * (L ** 2) / (rho * nu ** 2)


# ============================================================
# Reynolds number in neonatal airways
# ============================================================

def reynolds_number(Q: float, d: float, nu: float = CONST.nu_air) -> float:
    """
    Re = u * d / nu where u = Q / A, A = pi * (d/2)^2

    Neonatal airways: Re ~ 1-100 (laminar to transitional).
    This is far from turbulent (Re ~ 4000), which is why the
    regularity question is actually tractable here — we're in a
    regime where smooth solutions SHOULD exist, and the only
    mechanism for blowup is the surface tension singularity.
    """
    A = np.pi * (d / 2) ** 2
    u = abs(Q) / A if A > 0 else 0.0
    return u * d / nu


# ============================================================
# Compliance as a regularity proxy
# ============================================================

@dataclass
class BreathCycle:
    """One respiratory cycle extracted from ventilator data."""
    time: np.ndarray        # seconds within cycle
    pressure: np.ndarray    # cmH2O
    flow: np.ndarray        # mL/s
    volume: np.ndarray      # mL (integrated)

    @property
    def dynamic_compliance(self) -> float:
        """C_dyn = delta_V / delta_P [mL/cmH2O]"""
        dV = np.max(self.volume) - np.min(self.volume)
        dP = np.max(self.pressure) - np.min(self.pressure)
        return dV / dP if dP > 0 else float('inf')

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
        """
        Area enclosed by the P-V loop.
        Larger area = more hysteresis = further from equilibrium.
        As surfactant fails, this area changes characteristic shape.
        """
        _trapz = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
        return abs(float(_trapz(self.pressure, self.volume)))


# ============================================================
# Singularity proximity detector
# ============================================================

@dataclass
class RegularityState:
    """Assessment of how close the system is to singular behavior."""
    compliance: float           # mL/cmH2O
    compliance_trend: float     # derivative (negative = approaching singularity)
    lambda_param: float         # regularity parameter
    re_max: float              # max Reynolds number in cycle
    pv_loop_area: float        # phase space area
    classification: str         # 'smooth' | 'approaching' | 'critical' | 'singular'


def classify_regularity(
    compliance: float,
    compliance_trend: float,
    c_threshold_low: float = 0.3,   # mL/cmH2O — below this is critical
    c_threshold_high: float = 1.0,  # mL/cmH2O — above this is smooth
) -> str:
    """
    Classify the regularity state from compliance measurements.

    In NS terms:
    - 'smooth': ||u||_{H^1} bounded, solution regular
    - 'approaching': ||u||_{H^1} growing, approaching critical threshold
    - 'critical': near the blowup threshold, intervention needed
    - 'singular': compliance near zero = alveolar collapse = "blowup"
    """
    if compliance < c_threshold_low:
        return 'singular' if compliance_trend <= 0 else 'critical'
    if compliance < c_threshold_high:
        return 'critical' if compliance_trend < -0.1 else 'approaching'
    return 'smooth'


# ============================================================
# Surfactant as regularization
# ============================================================

def surfactant_regularization(
    gamma_0: float,
    surfactant_concentration: float,
    c_half: float = 0.5,
) -> float:
    """
    Surface tension as a function of surfactant concentration.

    gamma(c) = gamma_water * (1 - c / (c + c_half))

    At c = 0 (no surfactant): gamma = gamma_water ~ 70 mN/m
    At c >> c_half: gamma -> 0 (full regularization)
    At clinical levels: gamma ~ 25 mN/m

    This is the regularization operator. In PDE terms, adding surfactant
    is analogous to adding a viscosity term that prevents blowup.
    The clinical question "how much surfactant to give" maps directly to
    "how much regularization is needed to maintain smooth solutions."
    """
    gamma_water = CONST.gamma_no_surfactant
    return gamma_water * (1.0 - surfactant_concentration / (surfactant_concentration + c_half))


# ============================================================
# Energy functional (the NS quantity to monitor)
# ============================================================

def energy_from_ventilator(
    pressure: np.ndarray,
    flow: np.ndarray,
    dt: float,
) -> np.ndarray:
    """
    Approximate the kinetic energy of airflow from ventilator data.

    E(t) ~ (1/2) * rho * integral(u^2 dV) ~ (1/2) * rho * Q(t)^2 / A_eff

    In NS regularity theory, the energy inequality is:
        ||u(t)||^2 + 2*nu * integral_0^t ||grad u||^2 ds <= ||u_0||^2

    If this inequality is violated, the solution has lost regularity.
    We approximate this from measurable quantities.
    """
    rho = CONST.rho_air
    A_eff = np.pi * (CONST.airway_diameter_trachea / 2) ** 2
    flow_m3s = flow * 1e-6  # mL/s -> m^3/s
    kinetic = 0.5 * rho * (flow_m3s ** 2) / A_eff

    dissipation = np.cumsum(kinetic) * dt
    return kinetic


def enstrophy_proxy(flow: np.ndarray, dt: float) -> np.ndarray:
    """
    Enstrophy (integral of vorticity squared) is the key quantity in
    NS regularity — if enstrophy stays bounded, the solution is smooth.

    We approximate it from the flow signal's derivative (a proxy for
    velocity gradient, which relates to vorticity in the airway).

    Omega(t) ~ (dQ/dt)^2

    When this spikes — rapid flow acceleration/deceleration — the
    system is experiencing high vorticity, approaching turbulent transition.
    In the collapsing alveolus, this diverges.
    """
    dQdt = np.gradient(flow, dt)
    return dQdt ** 2
