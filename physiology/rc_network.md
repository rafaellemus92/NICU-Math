# Spatial compliance in a passive RC teaching network

This synthetic example isolates compliance assignment on a fixed graph. It is
not calibrated neonatal physiology, a treatment model, or a link to a
Navier–Stokes theorem. Pressures are cmH2O, times seconds, excess elastic volumes
mL, resistances cmH2O s/mL and compliances mL/cmH2O. Parameters are chosen for
transparent algebra, not from patients. There is no recruitment, inertance,
nonlinear compliance or dynamic chest-wall coupling.

## Graph and equations

Each of two identical subtrees connects an ideal prescribed pressure P through
one trunk resistance R0 to a massless junction, then through two terminal
resistances Ri to compliant terminals Ci. Only siblings are dynamically coupled:
the two subtrees are independent under the ideal boundary. With gi=1/Ri,
g0=1/R0 and h=g0+g1+g2, the junction pressure is

    pj = (g0 P + g1 p1 + g2 p2)/h,
    qi = gi(pj-pi),   Ci pi' = qi.

The two-terminal block is L=diag(g)-ggᵀ/h and b=g0 g/h. Assemble the
blocks to obtain C p'=-L p+bP, with diagonal C and b=L1. For finite positive
resistances, L is symmetric positive definite (the resistor dissipation is
positive for every nonzero state with boundary zero). With positive C,
S=C^(-1/2)L C^(-1/2) is symmetric positive definite and

    p(t) = P1 + C^(-1/2) exp(-St) C^(1/2) (p(0)-P1).

This is an exact constant-boundary formula; the implementation evaluates its
symmetric eigendecomposition approximately in float64. Piecewise constant
boundaries can be chained by passing the terminal state between segments.
Nonnegative initial and boundary pressures give nonnegative trajectories in
exact arithmetic. Signed flows allow emptying and redistribution.

Summing terminal volumes Vi=Ci pi gives V'=sum(qtrunk). Junction conservation
is qtrunk=q1+q2. The elastic energy E=pᵀCp/2 satisfies

    E' = P sum(qtrunk) - sum_terminal Ri qi² - sum_trunk R0 qtrunk².

In particular E'=-pᵀLp<0 at P=0 for any nonzero state. These are passive
network identities, not clinical observations.

## Fixed comparison and exact calculation

The [plan](spatial_compliance_plan.md) fixed all resistances at 1, initial
terminal pressures at 1, and a boundary release from 1 to 0 at t=0 before
endpoint evaluation. Grouped assignment G=(1,1)|(2,2) and mixed assignment
M=(1,2)|(1,2) have the same graph, every resistance, compliance multiset,
terminal RiCi multiset, total compliance 6, initial volume 6 and energy 3.
The only change is which compliances share each trunk. This is not merely a
relabeling of the entire network.

Each conductance block is [[2,-1],[-1,2]]/3. In G, equal siblings stay equal,
so the total excess volume is exactly

    VG(t) = 2 exp(-t/3) + 4 exp(-t/6).

For each mixed block, C^(-1)L has eigenvalues (1±1/sqrt(3))/2.
Matching initial volume and its derivative yields

    VM(t) = exp(-t/2) [6 cosh(t/(2 sqrt(3)))
                              + (10/sqrt(3)) sinh(t/(2 sqrt(3)))].

The code uses the equivalent positive exponential sum to avoid hyperbolic
overflow. Both totals start with V=6, V'=-4/3, V''=1/3, but
VG'''(0)=-5/54 and VM'''(0)=-1/9. Therefore

    VG(t)-VM(t) = t³/324 + O(t⁴),
    fG(t)-fM(t) = t³/1944 + O(t⁴),   f=V/6.

Independent rational-arithmetic tests derive these derivatives from the edge
conductances. Matching the compliance and local terminal time-constant
multisets is insufficient to determine aggregate emptying on this graph.
No novelty claim or general spatial-network theorem is asserted.

The preregistered primary endpoint is t=1 second. Float64 evaluation gives
fG(1)=0.8031649201183390, fM(1)=0.8028092780126327 and
**fG(1)-fM(1)=0.0003556421057062664** (about 0.0355642 percentage points).
The difference in volume is about 0.00213385 mL. This small synthetic effect
has no established clinical significance. Parameters/time were not retuned.
The [stored output](spatial_compliance_results/fixed_example.json) contains
all six fixed observation times and local volumes; discrepancies from the
closed formulas are at most 1.78e-15 mL at those times. Those discrepancies
measure numerical agreement, not certified accuracy of every displayed digit.

## Controls, numerical domain and verification

Setting both trunk resistances exactly to zero contracts each junction to the
boundary, rather than dividing by zero. Both assignments then have the same
total 2 exp(-t)+4 exp(-t/2). A near-zero positive trunk check approaches this
limit. Simultaneously permuting the graph, parameters, states and output indices
preserves the solution, tested with unequal resistances and nonuniform initial
pressures. Compliance-only regrouping is a different physical assignment.

The API requires finite positive C and terminal R, finite nonnegative trunk R,
nonnegative pressures and observation times, and a partition of terminal indices.
Zero trunk uses contraction. Unrepresentable float64 coefficients, volumes or
diagnostics are rejected; arbitrary ill-conditioned parameter ranges are not
certified. Negative eigensolver roundoff of magnitude at most
64 eps max(initial pressure, boundary pressure) is floored to zero; larger
negative excursions fail. This explicit numerical safeguard is not an exact
positivity proof or a guarantee of conservation after rounding. Inputs are
copied into immutable tuples. Empty, repeated and unsorted observation times
are supported. The model accepts constant boundaries; it does not interpolate
arbitrary waveforms.

Run from the repository root using existing NumPy, SciPy and pytest:

```sh
python -B -m physiology.rc_network
python -B -m pytest -q tests/physiology
```

The complete physiology suite passed **87 tests** (41 existing and 46 new).
Checks include independent SciPy expm agreement, exact rational derivatives,
closed forms, conservation, dissipation and integrated energy loss, graph
relabeling, contraction, boundary equilibrium/chaining and input rejection.
See [run metadata](spatial_compliance_results/run_metadata.json) for source
hashes and Python/NumPy/SciPy versions, and the preserved test log. The existing
two-compartment implementation and its tests are unchanged. An independent AI
source/math review is documented with its limits in the results folder;
this is neither human peer review nor physiological validation.
