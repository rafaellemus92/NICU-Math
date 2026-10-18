"""Incomplete conjectural outline, with explicit gaps and analytical sanity checks.

This module makes no assertion about the current status of any general
Navier-Stokes problem. Its corrections concern this repository's arguments.
Nothing here is validated for patient care.
"""
from dataclasses import dataclass

CONJECTURE_STATEMENT = (
    "Motivation: investigate how geometry, surface tension and distributed "
    "mechanics affect explicitly specified models. The earlier gamma/curvature "
    "regularity criterion is incomplete and unproved; its universal converse "
    "is refuted by stationary spheres. No clinical-to-PDE equivalence follows."
)

@dataclass(frozen=True)
class ProofStep:
    number: int
    title: str
    status: str
    statement: str
    limitation: str


PROOF_STEPS = [
    ProofStep(1, 'Specify the free-boundary problem', 'gap', 'A pressure-only boundary condition omits viscous traction. Specify the material kinematic condition, stress convention, forcing, initial compatibility, domain regularity and solution class before proposing a continuation theorem.', 'Respiratory observations motivate a model; they do not supply these PDE hypotheses.'),
    ProofStep(2, 'Energy and trace estimates need hypotheses', 'gap', 'For a smooth closed material interface with constant gamma, no body force and constant exterior pressure, surface work is accounted for by surface energy. A trace bound needs controlled geometry and the full H1 norm; dropping the L2 part requires extra conditions. Energy control alone does not establish the proposed regularity conclusion.', 'Scalar pressure-volume work cannot replace a three-dimensional energy or gradient estimate.'),
    ProofStep(3, 'Vortex stretching remains uncontrolled', 'gap', 'The earlier linear enstrophy inequality assumed a bound on this term that was never proved. Gronwall applies only after its coefficient is shown integrable, with the boundary terms also controlled. A bulk Reynolds number does not close this gap.', 'No compliance threshold in this repository supplies the missing estimate.'),
    ProofStep(4, 'The Sobolev deduction was false', 'refuted', 'In three dimensions, take a nonzero smooth compactly supported bump phi and f_epsilon(x)=epsilon^(-1/2) phi((x-x0)/epsilon), inside a fixed domain. Its L2 norm scales as epsilon, its gradient L2 norm stays constant, and its supremum grows as epsilon^(-1/2). Thus bounded H1 does not give the claimed Linfinity bound. A continuation criterion also needs its own domain and boundary assumptions.', 'A temporal scalar-flow derivative is not spatial vorticity or enstrophy.'),
    ProofStep(5, 'A closed incompressible material sphere cannot shrink', 'identity', 'For a sphere this gives 4*pi*r^2*r_dot=0, hence r_dot=0 at positive radius. The former shrinking-sphere construction violated incompressibility plus the material boundary condition. An open, compressible or multiphase model requires different equations and assumptions.', 'Atelectasis is not thereby identified with a singularity of this closed incompressible model.'),
    ProofStep(6, 'Static spheres defeat a universal threshold claim', 'identity', 'With outward normal, stress T=-pI+2muD(u), and traction jump (T_in-T_out)n=-gamma*kappa*n, a stationary sphere satisfies the unforced equations for every positive constant gamma and radius. Its pressure is spatially constant. Arbitrarily large pressure-scale ratios therefore do not force every solution to blow up. This does not disprove an existential conjecture about other initial data.', 'A pressure-scale ratio is not a clinical risk or intervention score.'),
    ProofStep(7, 'Positive gamma reduction does not remove the radius limit', 'identity', 'Replacing gamma by a smaller positive constant changes the coefficient, not the divergence. Boundedness along a prescribed vanishing-radius path would require gamma(r)=O(r), or a radius bounded away from zero. Neither is proved here. No post-intervention smoothing theorem follows.', 'No dose-response, patient-specific prediction or validated clinical tool is provided.'),
 ]


def proof_summary() -> str:
    """Describe the incomplete conjecture and its failures, not a proof certificate."""
    return "\n\n".join([
        "INCOMPLETE CONJECTURE: GAPS AND SANITY CHECKS", CONJECTURE_STATEMENT,
        *[f"{s.number}. {s.title} [{s.status}]\n{s.statement}\n{s.limitation}" for s in PROOF_STEPS],
        "Analytical identities have stated assumptions; floating samples only check implementations. "
        "Synthetic waveform output is not numerical evidence for PDE regularity. Teaching use only."
    ])


def estimate_critical_constant(*args, **kwargs):
    """Retired: compliance observations do not identify a PDE regularity threshold."""
    raise NotImplementedError("No validated mapping from compliance to a PDE critical constant exists here")


def generate_strogatz_letter() -> str:
    """Return an unsent discussion draft; no clinical observation or proof is asserted."""
    return (
        "Dear Professor Strogatz,\n\n"
        "I would value discussion of whether respiratory-mechanics motivations can "
        "inform precisely formulated questions about geometry and dynamics. Our earlier "
        "outline has unresolved vortex-stretching and boundary-estimate gaps, and its "
        "Sobolev inference and shrinking material sphere construction were invalid. "
        "Our RC-shaped waveforms are synthetic teaching instruments, not Navier-Stokes "
        "solutions or evidence of clinical PDE singularities.\n\n"
        "[Researcher — unsent draft]"
    )
