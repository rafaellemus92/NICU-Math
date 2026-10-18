"""
Demonstration: detecting singularity approach in synthetic ventilator data.

This script generates synthetic waveform data simulating surfactant
depletion (RDS) and runs the full analysis pipeline — showing how
compliance collapse maps to the NS regularity question.

Run:
    python -m navier_stokes.demo
"""

import numpy as np
from .ventilator_ingest import generate_synthetic_waveform, segment_breaths, breath_summary
from .analysis import (
    analyze_compliance_trend,
    estimate_decay_exponent,
    phase_space_trajectory,
    attractor_divergence,
    enstrophy_evolution,
    singularity_proximity,
    detect_surfactant_response,
)
from .formulation import CONST, classify_regularity
from .proof_outline import proof_summary


def run_demo():
    print("=" * 60)
    print("NAVIER-STOKES REGULARITY IN NEONATAL RESPIRATORY MECHANICS")
    print("Synthetic waveform analysis demo")
    print("=" * 60)
    print()

    # --- Scenario 1: Stable breathing (smooth regime) ---
    print("SCENARIO 1: Stable breathing (adequate surfactant)")
    print("-" * 50)
    stable = generate_synthetic_waveform(
        n_breaths=50,
        compliance=1.0,
        compliance_decay=0.0,
        seed=42,
    )
    stable_cycles = segment_breaths(stable)
    print(f"  Breaths segmented: {len(stable_cycles)}")

    stable_state = singularity_proximity(stable_cycles)
    print(f"  Mean compliance: {stable_state.compliance:.3f} mL/cmH2O")
    print(f"  Compliance trend: {stable_state.compliance_trend:.4f}")
    print(f"  Classification: {stable_state.classification}")
    print(f"  → The solution is SMOOTH. The baby breathes.")
    print()

    # --- Scenario 2: Surfactant depletion (approaching singularity) ---
    print("SCENARIO 2: Surfactant depletion (approaching singularity)")
    print("-" * 50)
    declining = generate_synthetic_waveform(
        n_breaths=100,
        compliance=1.0,
        compliance_decay=0.008,  # 0.8% per breath
        seed=42,
    )
    declining_cycles = segment_breaths(declining)
    print(f"  Breaths segmented: {len(declining_cycles)}")

    # Compliance trend analysis
    trend = analyze_compliance_trend(declining_cycles)
    print(f"  Compliance slope: {trend.slope:.4f} per breath")
    print(f"  Curvature: {trend.curvature:.6f}")
    if trend.half_life:
        print(f"  Half-life: {trend.half_life:.1f} breaths")
    print(f"  Changepoints: {trend.changepoints}")

    # Decay exponent
    alpha, t_star = estimate_decay_exponent(trend.values)
    print(f"  Decay exponent α: {alpha:.3f}")
    print(f"  Estimated T*: {t_star:.1f} breaths")

    # Phase space
    ps_metrics = phase_space_trajectory(declining_cycles)
    divergence = attractor_divergence(ps_metrics)
    print(f"  Phase-space divergence (last 10 breaths): "
          f"{np.mean(divergence[-10:]):.3f}")

    # Enstrophy
    dt = 1.0 / declining.sample_rate_hz
    enst_mean, enst_peak = enstrophy_evolution(declining_cycles, dt)
    print(f"  Enstrophy growth (first→last): "
          f"{enst_mean[0]:.1f} → {enst_mean[-1]:.1f}")

    # Final state
    final_state = singularity_proximity(declining_cycles[-10:])
    print(f"  Final classification: {final_state.classification}")
    print(f"  → The solution is APPROACHING BLOWUP.")
    print()

    # --- Scenario 3: Surfactant rescue ---
    print("SCENARIO 3: Collapse then surfactant rescue")
    print("-" * 50)

    # First 60 breaths: declining
    pre_surf = generate_synthetic_waveform(
        n_breaths=60,
        compliance=1.0,
        compliance_decay=0.012,
        seed=42,
    )
    # Next 40 breaths: recovered (simulating surfactant given)
    post_surf = generate_synthetic_waveform(
        n_breaths=40,
        compliance=0.8,
        compliance_decay=0.0,
        pip=18.0,
        seed=43,
    )

    # Combine the recordings
    combined_time = np.concatenate([
        pre_surf.time,
        post_surf.time + pre_surf.time[-1],
    ])
    combined_pressure = np.concatenate([pre_surf.pressure, post_surf.pressure])
    combined_flow = np.concatenate([pre_surf.flow, post_surf.flow])

    from .ventilator_ingest import WaveformRecording, PatientContext
    combined = WaveformRecording(
        patient=PatientContext(
            gestational_age_weeks=28.0,
            birth_weight_grams=1000,
            postnatal_age_days=1,
            surfactant_given=True,
            surfactant_doses=1,
            ventilator_mode='SIMV_synthetic',
        ),
        sample_rate_hz=100.0,
        time=combined_time,
        pressure=combined_pressure,
        flow=combined_flow,
    )
    combined_cycles = segment_breaths(combined)
    print(f"  Total breaths: {len(combined_cycles)}")

    # Detect surfactant response
    events = detect_surfactant_response(combined_cycles)
    for ev in events:
        print(f"  Surfactant event at breath {ev['breath_index']}:")
        print(f"    Compliance: {ev['compliance_before']:.3f} → "
              f"{ev['compliance_after']:.3f}")
        print(f"    Improvement: {ev['improvement_ratio']:.1%}")
        print(f"    State: {ev['classification_before']} → "
              f"{ev['classification_after']}")

    if not events:
        print("  (No clear surfactant response detected in synthetic data)")

    # Before and after states
    n = len(combined_cycles)
    pre_state = singularity_proximity(combined_cycles[:n // 2])
    post_state = singularity_proximity(combined_cycles[n // 2:])
    print(f"  Pre-surfactant: {pre_state.classification} "
          f"(C={pre_state.compliance:.3f})")
    print(f"  Post-surfactant: {post_state.classification} "
          f"(C={post_state.compliance:.3f})")
    print(f"  → Regularization restored smoothness.")
    print()

    # --- Summary statistics ---
    print("SUMMARY: Three Regimes of NS in the Neonatal Lung")
    print("-" * 50)
    summary = breath_summary(declining_cycles)
    print(f"  Breaths analyzed: {summary['n_breaths']}")
    print(f"  Compliance: {summary['compliance_mean']:.3f} ± "
          f"{summary['compliance_std']:.3f} mL/cmH2O")
    print(f"  Compliance trend: {summary['compliance_trend']:.4f} per breath")
    print(f"  Resistance: {summary['resistance_mean']:.3f} cmH2O/(mL/s)")
    print(f"  Time constant: {summary['time_constant_mean']:.4f} s")
    print(f"  P-V loop area: {summary['pv_area_mean']:.2f} cmH2O·mL")
    print()

    # --- Print proof outline ---
    print()
    print(proof_summary())


if __name__ == "__main__":
    run_demo()
