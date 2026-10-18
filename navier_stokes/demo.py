"""Run synthetic descriptors: python -m navier_stokes.demo. No clinical validation."""
from .ventilator_ingest import generate_synthetic_waveform, segment_breaths
from .analysis import summarize_compliance, flow_derivative_evolution
from .proof_outline import proof_summary


def run_demo():
    print("Synthetic prescribed RC-shaped waveforms; not Navier-Stokes solutions")
    print("Illustrative compliance labels; no patient-specific or treatment inference")
    for label, decay in (("constant schedule", 0.0), ("declining schedule", 0.008)):
        recording = generate_synthetic_waveform(n_breaths=50, compliance_decay=decay, noise_level=0, seed=42)
        cycles = segment_breaths(recording)
        state = summarize_compliance(cycles)
        means, peaks = flow_derivative_evolution(cycles, 1 / recording.sample_rate_hz)
        print(f"{label}: {len(cycles)} cycles; {state.classification}; C={state.compliance:.4f} mL/cmH2O")
        print(f"  mean squared flow time derivative: {means.mean():.4f} mL^2/s^4")
    print(proof_summary())


if __name__ == '__main__':
    run_demo()
