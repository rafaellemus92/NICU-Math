# Two-compartment passive emptying

**Tier: exact computation.** The closed form is analytically derived below;
its floating-point evaluation is verified at machine precision. This is
not a formal proof certificate. This model is a teaching instrument only,
not a validated predictive clinical tool or a model of any specific patient.

## Assumptions and derivation

Each independent passive linear compartment obeys

\[
R_i \frac{dV_i}{dt}+\frac{V_i}{C_i}=\Delta P(t),
\qquad R_i>0,\quad C_i>0.
\]

Resistance and compliance are constant. Volume is **excess volume relative
to the zero-driving-pressure equilibrium baseline**. The model specifies
neither resting end-expiratory absolute volume nor clinical residual volume.
There is no shared dynamic chest-wall coupling. Use consistent units:
resistance is pressure × time / volume, compliance is volume / pressure.

Initially the compartments equilibrate at the same pressure P₀ > 0,
so Vᵢ(0) = CᵢP₀. After release to zero driving pressure at t = 0,
separation of variables gives dVᵢ/Vᵢ = −dt/(RᵢCᵢ), hence

\[
\tau_i=R_iC_i,\qquad V_i(t)=C_iP_0e^{-t/\tau_i},\qquad
f(t)=\frac{\sum_i C_i e^{-t/\tau_i}}{\sum_i C_i}.
\]

Set R₁ = R₂ = 2R and total compliance C₁ + C₂ = C in both cases.
Matched initial driving pressure therefore also implies matched total
initial excess volume CP₀ in this model.

| Case | (C₁, C₂) | (τ₁, τ₂) | Retained fraction at t = RC |
|---|---|---|---|
| A | (C/2, C/2) | (RC, RC) | exp(−1) ≈ 0.36787944117144233 |
| B | (0.9C, 0.1C) | (1.8RC, 0.2RC) | 0.9 exp(−1/1.8) + 0.1 exp(−5) ≈ 0.51705187336359804 |

The difference is approximately 0.14917243219215571 of the initial excess
volume. Equal total compliance and initial excess volume do not determine
the emptying trajectory: this is a summary-statistic obstruction caused by
the hidden distribution of local time constants.

## API and verification

`Compartment(R, C)` validates finite positive constants and a representable
positive time constant. `tau(compartment)` returns R × C.
`passive_emptying_series(compartments, P_0, t_grid)` returns a float64 array
of shape `(n_compartments, n_times)` with compartments in rows. A nonempty
sequence of compartments and finite nonnegative times are required. The
one-dimensional time grid may be empty, repeated, or unsorted. Initial
volumes and their sum must be representable; late-time underflow to zero
is allowed.

`passive_retained_fraction(compartments, P_0, t)` returns a scalar fraction.
For P₀ = 0, the volume series is identically zero but the fraction is
undefined (0/0); the fraction function raises `ValueError`. Negative
pressure is outside the chosen positive-excess-volume domain.

From the repository root:

```sh
python -m physiology.two_compartment
python -m pytest -q -s tests/physiology
```

The unit-scale script evaluates both headline expressions with absolute
formula self-consistency discrepancy 0.000e+00. Both sides evaluate the same
expressions; zero discrepancy is not independent verification. The expressions
are exact under the stated model assumptions; printed decimals approximate
them in float64. Tests check total compliance, initial
volume, time constants, headline errors below 1e−10 (also float64 roundoff
scale), shape and domain behavior, and independent SciPy `solve_ivp`
integration of both symmetric and heterogeneous cases below 1e−6 absolute
volume error. This is an independent numerical ODE integration crosscheck,
not a proof or certification of all displayed digits. Production uses NumPy
only; SciPy is used only in tests. Reverification environment: **NumPy 2.0.2,
SciPy 1.18.1**; versions recorded here do not add dependency requirements.

## Strict significance and limits

This construction isolates a summary-statistic obstruction within a
specified linear system. It does not incorporate nonlinear compliance,
recruitment, active breathing, or shared dynamic chest-wall coupling.
It makes no patient-specific inference and is not validated for patient
care. No other physiology ledger claims are tested or promoted here.
