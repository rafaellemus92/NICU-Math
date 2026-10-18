# navier_stokes — Neonatal fluid dynamics and the regularity question
#
# Core thesis: neonatal respiratory mechanics provide a physically bounded
# domain where Navier-Stokes solutions are directly observable. Surfactant
# dynamics act as a measurable regularization parameter. Its absence produces
# clinically observed finite-time singularity analogs (alveolar collapse).
#
# Modules:
#   formulation      — NS equations, Laplace pressure, compliance, energy
#   ventilator_ingest — Waveform data loading, breath segmentation, synthetic data
#   analysis         — Singularity proximity detection, phase-space analysis
#   proof_outline    — Formal conjecture and proof structure
#   demo             — End-to-end demonstration on synthetic data
#
# TODO Phase 3 (30+ entries / sufficient clinical data):
# - PLV calculation across respiratory-cardiac oscillator coupling
# - CRQA nonlinear coupling detection in ventilator waveforms
# - Fractal/1f analysis of flow time series near collapse events
