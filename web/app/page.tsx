import Link from 'next/link'
import { Eq } from '@/components/Katex'
import StatusBanner from '@/components/StatusBanner'

const card = { background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 12, padding: 24, marginBottom: 24 }

export default function Home() {
  return <div style={{ lineHeight: 1.7, color: '#b8b8c0' }}>
    <h1 style={{ fontFamily: 'Georgia, serif', color: '#e8e8ed', fontSize: 36 }}>Respiratory Mechanics and Fluid-Dynamics Questions</h1>
    <p>Clinical observations motivate questions about geometry, surface tension and distributed time constants.
      They do not establish a correspondence between respiratory failure and a Navier–Stokes singularity.</p>
    <StatusBanner>
      In the labels used across this repository the conjecture below is Open, the identities on the
      outline page are standard, and the demos are synthetic teaching models.
    </StatusBanner>
    <div style={card}>
      <h2>Incomplete conjecture</h2>
      <p>The earlier surface-tension threshold argument does not establish a conditional regularity theorem.
        Vortex stretching and boundary estimates remain uncontrolled. The inference from H¹ to L∞ in three
        dimensions was false. The proposed shrinking closed material sphere violates incompressible volume
        conservation (a collapsing alveolus empties through an open airway, which that closed model does not describe).
        The clinical observations that motivated the conjecture are listed on the outline page, apart from the mathematics.</p>
      <Link href="/outline">Read the conjecture, its gaps and the analytical sanity checks →</Link>
    </div>
    <div style={card}>
      <h2>Static spherical equilibrium</h2>
      <Eq>{String.raw`u=0,\quad p=p_{ext}+2\gamma/r,\quad r>0`}</Eq>
      <p>With outward normal and traction jump (T_in − T_out)n = −γκn, this unforced stationary
        sphere is an equilibrium for any positive constant surface tension. Large pressure-scale ratios
        therefore do not force every solution to blow up. This does not refute an existential conjecture
        about other data. Reducing γ to a smaller positive constant does not remove the 1/r divergence
        along a prescribed path toward zero radius.</p>
    </div>
    <div style={card}>
      <h2>Synthetic teaching instruments</h2>
      <p>The interactive demo prescribes and floors compliance, then draws RC-shaped waveforms.
        Its recovery schedule is an arbitrary input, not surfactant pharmacology. Scalar flow derivatives
        measure temporal changes, not spatial vorticity or enstrophy.</p>
      <Link href="/demo">Explore descriptive compliance trajectories →</Link>
      <p>The separate two-compartment calculation shows how equal total compliance and initial excess
        volume can yield different passive-emptying trajectories. That exact linear-model result does
        not supply a clinical-to-PDE bridge. Shared Air remains an exploratory demonstration with placeholder coupling parameters.</p>
      <Link href="/shared-air">Explore Shared Air →</Link>
    </div>
    <p>Evidence tiers remain distinct: motivation, incomplete conjecture, analytical identities,
      closed-form teaching models and numerical implementation checks. No patient-specific prediction,
      treatment recommendation or validated clinical tool is provided. Use synthetic data only.</p>
  </div>
}
