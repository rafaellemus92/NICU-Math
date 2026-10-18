'use client'
import { useState } from 'react'
import { Eq } from '@/components/Katex'
import StatusBanner from '@/components/StatusBanner'

// Step labels, as introduced in PR #16. The whole page carries the repository-wide
// label "Open: a conjecture, not checked" (math/README.md, "Status labels");
// the per-step labels say what kind of statement each step is.
type StepStatus = 'identity' | 'gap' | 'refuted'

const STATUS_COLORS: Record<StepStatus, string> = {
  identity: '#6b8afd',
  gap: '#facc15',
  refuted: '#ef4444',
}

const STATUS_MEANING: Record<StepStatus, string> = {
  identity: 'An elementary analytical identity under stated assumptions. Repository label: standard.',
  gap: 'A step the earlier outline needed and never supplied. Repository label: open.',
  refuted: 'A deduction of the earlier outline shown to be false.',
}

interface StepData {
  number: number
  title: string
  status: StepStatus
  statementTeX: string
  approach: string
  scope: string
  refs: string[]
}

// The mathematics only. Clinical motivation is in CLINICAL_MOTIVATION below.
const STEPS: StepData[] = [
  {
    number: 1,
    title: 'Specify the free-boundary problem',
    status: 'gap',
    statementTeX: String.raw`T=-pI+2\mu D(u),\quad (T_{in}-T_{out})n=-\gamma\kappa n`,
    approach:
      'A pressure-only boundary condition omits viscous traction. Specify the material kinematic condition, stress convention, forcing, initial compatibility, domain regularity and solution class before proposing a continuation theorem.',
    scope: 'Respiratory observations motivate a model; they do not supply these PDE hypotheses.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 2,
    title: 'Energy and trace estimates need hypotheses',
    status: 'gap',
    statementTeX: String.raw`E=\frac{\rho}{2}\int_{\Omega(t)}|u|^2\,dx+\gamma|\Gamma(t)|`,
    approach:
      'For a smooth closed material interface with constant gamma, no body force and constant exterior pressure, surface work is accounted for by surface energy. A trace bound needs controlled geometry and the full H1 norm; dropping the L2 part requires extra conditions. Energy control alone does not establish the proposed regularity conclusion.',
    scope: 'Scalar pressure-volume work cannot replace a three-dimensional energy or gradient estimate.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 3,
    title: 'Vortex stretching remains uncontrolled',
    status: 'gap',
    statementTeX: String.raw`\int_\Omega ((\omega\cdot\nabla)u)\cdot\omega\,dx`,
    approach:
      'The earlier linear enstrophy inequality assumed a bound on this term that was never proved. Gronwall applies only after its coefficient is shown integrable, with the boundary terms also controlled. A bulk Reynolds number does not close this gap. In three dimensions the term needs control such as ∇u in L¹(0,T;L^∞) or ω in L^p with p ≥ 3; an energy estimate gives ∇u in L²(0,T;L²) only. This is the obstruction of the general problem.',
    scope: 'No compliance threshold in this repository supplies the missing estimate.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 4,
    title: 'The Sobolev deduction was false',
    status: 'refuted',
    statementTeX: String.raw`H^1(\Omega)\hookrightarrow L^6(\Omega)\quad\not\Longrightarrow\quad H^1(\Omega)\hookrightarrow L^\infty(\Omega)`,
    approach:
      'In three dimensions, take a nonzero smooth compactly supported bump phi and f_epsilon(x)=epsilon^(-1/2) phi((x-x0)/epsilon), inside a fixed domain. Its L2 norm scales as epsilon, its gradient L2 norm stays constant, and its supremum grows as epsilon^(-1/2). Thus bounded H1 does not give the claimed Linfinity bound. A continuation criterion also needs its own domain and boundary assumptions.',
    scope: 'A temporal scalar-flow derivative is not spatial vorticity or enstrophy.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 5,
    title: 'A closed incompressible material sphere cannot shrink',
    status: 'identity',
    statementTeX: String.raw`\frac{d|\Omega(t)|}{dt}=\int_{\Gamma(t)}u\cdot n\,dS=\int_{\Omega(t)}\nabla\cdot u\,dx=0`,
    approach:
      'For a sphere this gives 4*pi*r^2*r_dot=0, hence r_dot=0 at positive radius. The former shrinking-sphere construction violated incompressibility plus the material boundary condition for a closed domain. An open domain with an airway outlet, a compressible gas, or a multiphase model requires different equations and assumptions.',
    scope: 'Atelectasis is not thereby identified with a singularity of this closed incompressible model.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 6,
    title: 'Static spheres defeat a universal threshold claim',
    status: 'identity',
    statementTeX: String.raw`u=0,\quad p=p_{ext}+\gamma\kappa,\quad\kappa=2/r`,
    approach:
      'With outward normal, stress T=-pI+2muD(u), and traction jump (T_in-T_out)n=-gamma*kappa*n, a stationary sphere satisfies the unforced equations for every positive constant gamma and radius. Its pressure is spatially constant. Arbitrarily large pressure-scale ratios therefore do not force every solution to blow up. This does not disprove an existential conjecture about other initial data.',
    scope: 'A pressure-scale ratio is not a clinical risk or intervention score.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
  {
    number: 7,
    title: 'Positive gamma reduction does not remove the radius limit',
    status: 'identity',
    statementTeX: String.raw`\gamma>0\text{ fixed}:\quad\lim_{r\to0^+}2\gamma/r=+\infty`,
    approach:
      'Replacing gamma by a smaller positive constant changes the coefficient, not the divergence. Boundedness along a prescribed vanishing-radius path would require gamma(r)=O(r), or a radius bounded away from zero. Neither is proved here. No post-intervention smoothing theorem follows: in three dimensions, restarting from L² data gives Leray–Hopf weak solutions whose smoothness is the open problem itself.',
    scope: 'No dose-response, patient-specific prediction or validated clinical tool is provided.',
    refs: ['In-repository analytical derivation; see navier_stokes/README.md'],
  },
]

// Not part of the mathematics. These are the bedside observations that motivated the
// conjecture. They are real; they are not evidence that any Navier–Stokes solution
// loses or regains regularity. That identification is the conjecture, and it is open.
const CLINICAL_MOTIVATION: string[] = [
  'Without surfactant, alveolar surface tension is about 70 mN/m instead of about 25 mN/m, and the Laplace pressure 2γ/r rises as alveoli shrink.',
  'On the ventilator this appears as falling compliance, rising pressures and a degenerating pressure–volume loop.',
  'Exogenous surfactant reverses the picture within minutes: compliance improves and gas exchange recovers.',
  'Neonatal airway flow is laminar, with Reynolds numbers of order 1 to 100, far from the turbulent range.',
  'The air in a collapsing alveolus leaves through the airway; the domain is open, which is why the closed-sphere identity in step 5 does not describe it.',
]

function Badge({ status }: { status: StepStatus }) {
  return (
    <span
      title={STATUS_MEANING[status]}
      style={{
        display: 'inline-block',
        fontSize: 11,
        fontWeight: 600,
        textTransform: 'uppercase',
        letterSpacing: '0.06em',
        padding: '2px 10px',
        borderRadius: 999,
        color: STATUS_COLORS[status],
        border: `1px solid ${STATUS_COLORS[status]}44`,
        background: `${STATUS_COLORS[status]}11`,
      }}
    >
      {status}
    </span>
  )
}

function StepCard({ step, open, onToggle }: { step: StepData; open: boolean; onToggle: () => void }) {
  return (
    <div
      style={{
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.06)',
        borderRadius: 12,
        marginBottom: 12,
        overflow: 'hidden',
        transition: 'border-color 0.2s',
        ...(open ? { borderColor: 'rgba(255,255,255,0.12)' } : {}),
      }}
    >
      <button
        onClick={onToggle}
        style={{
          display: 'flex',
          width: '100%',
          alignItems: 'center',
          gap: 14,
          padding: '16px 20px',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          color: '#e8e8ed',
          textAlign: 'left',
        }}
      >
        <span style={{ fontFamily: 'Georgia, serif', fontSize: 22, fontWeight: 700, color: '#c9a96e', minWidth: 28 }}>
          {step.number}
        </span>
        <span style={{ flex: 1, fontSize: 16, fontWeight: 500 }}>{step.title}</span>
        <Badge status={step.status} />
        <span
          style={{
            fontSize: 18,
            color: '#888899',
            transform: open ? 'rotate(90deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s',
          }}
        >
          ▸
        </span>
      </button>

      {open && (
        <div style={{ padding: '0 20px 20px 62px' }}>
          <div style={{ margin: '0 0 16px' }}>
            <Eq>{step.statementTeX}</Eq>
          </div>
          <p style={{ color: '#c8c8d0', fontSize: 15, lineHeight: 1.7, margin: '0 0 16px' }}>{step.approach}</p>
          <div
            style={{
              background: 'rgba(201,169,110,0.06)',
              borderLeft: '3px solid #c9a96e',
              padding: '12px 16px',
              borderRadius: '0 8px 8px 0',
              marginBottom: 16,
            }}
          >
            <div
              style={{
                fontSize: 10,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: '#c9a96e',
                marginBottom: 6,
                fontWeight: 600,
              }}
            >
              Scope limit
            </div>
            <p style={{ color: '#b8b8c0', fontSize: 14, fontStyle: 'italic', lineHeight: 1.6, margin: 0 }}>{step.scope}</p>
          </div>
          <div style={{ fontSize: 13, color: '#888899' }}>
            <span style={{ fontWeight: 600 }}>Refs: </span>
            {step.refs.join(' · ')}
          </div>
        </div>
      )}
    </div>
  )
}

export default function OutlinePage() {
  const [openSteps, setOpenSteps] = useState<Set<number>>(new Set())

  const toggle = (n: number) => {
    setOpenSteps((prev) => {
      const next = new Set(prev)
      if (next.has(n)) next.delete(n)
      else next.add(n)
      return next
    })
  }

  const expandAll = () => setOpenSteps(new Set(STEPS.map((s) => s.number)))
  const collapseAll = () => setOpenSteps(new Set())

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h1
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 40,
            fontWeight: 700,
            color: '#e8e8ed',
            marginBottom: 12,
            letterSpacing: '-0.02em',
          }}
        >
          Conjecture and Gaps
        </h1>
        <p style={{ color: '#888899', fontSize: 17, lineHeight: 1.6, maxWidth: 680, margin: 0 }}>
          An incomplete research proposal with invalid deductions corrected. No conditional regularity
          theorem is established here.
        </p>
      </div>

      <StatusBanner>
        The step labels below say what kind of statement each step is: three elementary identities,
        three missing steps, one refuted deduction.
      </StatusBanner>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: 24,
          flexWrap: 'wrap',
          gap: 12,
        }}
      >
        <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
          {(['identity', 'gap', 'refuted'] as const).map((s) => (
            <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{ width: 8, height: 8, borderRadius: '50%', background: STATUS_COLORS[s], display: 'inline-block' }}
              />
              <span style={{ fontSize: 13, color: '#888899' }}>
                <span style={{ textTransform: 'capitalize', color: '#c8c8d0' }}>{s}</span>
                {' — '}
                {STATUS_MEANING[s]}
              </span>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <button
            onClick={expandAll}
            style={{
              background: 'none',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#888899',
              fontSize: 12,
              padding: '4px 12px',
              borderRadius: 6,
              cursor: 'pointer',
            }}
          >
            Expand all
          </button>
          <button
            onClick={collapseAll}
            style={{
              background: 'none',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#888899',
              fontSize: 12,
              padding: '4px 12px',
              borderRadius: 6,
              cursor: 'pointer',
            }}
          >
            Collapse all
          </button>
        </div>
      </div>

      {STEPS.map((step) => (
        <StepCard key={step.number} step={step} open={openSteps.has(step.number)} onToggle={() => toggle(step.number)} />
      ))}

      <div
        style={{
          marginTop: 48,
          marginBottom: 32,
          background: 'rgba(201,169,110,0.05)',
          border: '1px solid rgba(201,169,110,0.25)',
          borderLeft: '3px solid #c9a96e',
          borderRadius: 12,
          padding: '24px 28px',
        }}
      >
        <div
          style={{
            fontSize: 10,
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            color: '#c9a96e',
            marginBottom: 8,
            fontWeight: 600,
          }}
        >
          Not part of the mathematics
        </div>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, color: '#e8e8ed', marginBottom: 12, letterSpacing: '-0.01em' }}>
          Clinical Motivation
        </h2>
        <p style={{ color: '#b8b8c0', fontSize: 15, lineHeight: 1.7, margin: '0 0 16px' }}>
          These are the bedside observations that motivated the conjecture. They are real clinical
          phenomena. They are not evidence that any Navier–Stokes solution loses or regains regularity;
          that identification is the conjecture, and it is open.
        </p>
        <ul style={{ margin: 0, paddingLeft: 20 }}>
          {CLINICAL_MOTIVATION.map((text, i) => (
            <li key={i} style={{ color: '#b8b8c0', fontSize: 14, fontStyle: 'italic', lineHeight: 1.6, marginBottom: 8 }}>
              {text}
            </li>
          ))}
        </ul>
      </div>

      <p style={{ color: '#b8b8c0', lineHeight: 1.7, marginTop: 32 }}>
        The analytical identities above have explicit assumptions. Numerical samples check their
        implementation only. This page does not assess the current status of a general Navier–Stokes
        problem. Synthetic teaching use only; not validated for patient care.
      </p>
    </div>
  )
}
