'use client'
import { useState } from 'react'
import { K, Eq } from '@/components/Katex'

const STATUS_COLORS: Record<string, string> = {
  identity: '#4ade80',
  gap: '#facc15',
  refuted: '#ef4444',
}

interface ProofStepData {
  number: number
  title: string
  status: 'identity' | 'gap' | 'refuted'
  statementTeX: string
  approach: string
  clinical: string
  refs: string[]
}

const STEPS: ProofStepData[] = [
  {
    "number": 1,
    "title": "Specify the free-boundary problem",
    "status": "gap",
    "statementTeX": "T=-pI+2\\mu D(u),\\quad (T_{in}-T_{out})n=-\\gamma\\kappa n",
    "approach": "A pressure-only boundary condition omits viscous traction. Specify the material kinematic condition, stress convention, forcing, initial compatibility, domain regularity and solution class before proposing a continuation theorem.",
    "clinical": "Respiratory observations motivate a model; they do not supply these PDE hypotheses.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 2,
    "title": "Energy and trace estimates need hypotheses",
    "status": "gap",
    "statementTeX": "E=\\frac{\\rho}{2}\\int_{\\Omega(t)}|u|^2\\,dx+\\gamma|\\Gamma(t)|",
    "approach": "For a smooth closed material interface with constant gamma, no body force and constant exterior pressure, surface work is accounted for by surface energy. A trace bound needs controlled geometry and the full H1 norm; dropping the L2 part requires extra conditions. Energy control alone does not establish the proposed regularity conclusion.",
    "clinical": "Scalar pressure-volume work cannot replace a three-dimensional energy or gradient estimate.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 3,
    "title": "Vortex stretching remains uncontrolled",
    "status": "gap",
    "statementTeX": "\\int_\\Omega ((\\omega\\cdot\\nabla)u)\\cdot\\omega\\,dx",
    "approach": "The earlier linear enstrophy inequality assumed a bound on this term that was never proved. Gronwall applies only after its coefficient is shown integrable, with the boundary terms also controlled. A bulk Reynolds number does not close this gap.",
    "clinical": "No compliance threshold in this repository supplies the missing estimate.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 4,
    "title": "The Sobolev deduction was false",
    "status": "refuted",
    "statementTeX": "H^1(\\Omega)\\hookrightarrow L^6(\\Omega)\\quad\\not\\Longrightarrow\\quad H^1(\\Omega)\\hookrightarrow L^\\infty(\\Omega)",
    "approach": "In three dimensions, take a nonzero smooth compactly supported bump phi and f_epsilon(x)=epsilon^(-1/2) phi((x-x0)/epsilon), inside a fixed domain. Its L2 norm scales as epsilon, its gradient L2 norm stays constant, and its supremum grows as epsilon^(-1/2). Thus bounded H1 does not give the claimed Linfinity bound. A continuation criterion also needs its own domain and boundary assumptions.",
    "clinical": "A temporal scalar-flow derivative is not spatial vorticity or enstrophy.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 5,
    "title": "A closed incompressible material sphere cannot shrink",
    "status": "identity",
    "statementTeX": "\\frac{d|\\Omega(t)|}{dt}=\\int_{\\Gamma(t)}u\\cdot n\\,dS=\\int_{\\Omega(t)}\\nabla\\cdot u\\,dx=0",
    "approach": "For a sphere this gives 4*pi*r^2*r_dot=0, hence r_dot=0 at positive radius. The former shrinking-sphere construction violated incompressibility plus the material boundary condition. An open, compressible or multiphase model requires different equations and assumptions.",
    "clinical": "Atelectasis is not thereby identified with a singularity of this closed incompressible model.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 6,
    "title": "Static spheres defeat a universal threshold claim",
    "status": "identity",
    "statementTeX": "u=0,\\quad p=p_{ext}+\\gamma\\kappa,\\quad\\kappa=2/r",
    "approach": "With outward normal, stress T=-pI+2muD(u), and traction jump (T_in-T_out)n=-gamma*kappa*n, a stationary sphere satisfies the unforced equations for every positive constant gamma and radius. Its pressure is spatially constant. Arbitrarily large pressure-scale ratios therefore do not force every solution to blow up. This does not disprove an existential conjecture about other initial data.",
    "clinical": "A pressure-scale ratio is not a clinical risk or intervention score.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  },
  {
    "number": 7,
    "title": "Positive gamma reduction does not remove the radius limit",
    "status": "identity",
    "statementTeX": "\\gamma>0\\text{ fixed}:\\quad\\lim_{r\\to0^+}2\\gamma/r=+\\infty",
    "approach": "Replacing gamma by a smaller positive constant changes the coefficient, not the divergence. Boundedness along a prescribed vanishing-radius path would require gamma(r)=O(r), or a radius bounded away from zero. Neither is proved here. No post-intervention smoothing theorem follows.",
    "clinical": "No dose-response, patient-specific prediction or validated clinical tool is provided.",
    "refs": [
      "In-repository analytical derivation; see navier_stokes/README.md"
    ]
  }
]

function Badge({ status }: { status: string }) {
  return (
    <span
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

function StepCard({
  step,
  open,
  onToggle,
}: {
  step: ProofStepData
  open: boolean
  onToggle: () => void
}) {
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
      {/* Header */}
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
        <span
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 22,
            fontWeight: 700,
            color: '#c9a96e',
            minWidth: 28,
          }}
        >
          {step.number}
        </span>
        <span style={{ flex: 1, fontSize: 16, fontWeight: 500 }}>
          {step.title}
        </span>
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

      {/* Expanded content */}
      {open && (
        <div style={{ padding: '0 20px 20px 62px' }}>
          {/* Math statement */}
          <div style={{ margin: '0 0 16px' }}>
            <Eq>{step.statementTeX}</Eq>
          </div>

          {/* Approach */}
          <p style={{ color: '#c8c8d0', fontSize: 15, lineHeight: 1.7, margin: '0 0 16px' }}>
            {step.approach}
          </p>

          {/* Clinical analog */}
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
            <p style={{ color: '#b8b8c0', fontSize: 14, fontStyle: 'italic', lineHeight: 1.6, margin: 0 }}>
              {step.clinical}
            </p>
          </div>

          {/* References */}
          <div style={{ fontSize: 13, color: '#888899' }}>
            <span style={{ fontWeight: 600 }}>Refs: </span>
            {step.refs.join(' · ')}
          </div>
        </div>
      )}
    </div>
  )
}

export default function ProofPage() {
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
      {/* Header */}
      <div style={{ marginBottom: 48 }}>
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
          An incomplete research proposal with invalid deductions corrected. No conditional regularity theorem is established here.
        </p>
      </div>

      {/* Legend + controls */}
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
        <div style={{ display: 'flex', gap: 16 }}>
          {(['identity', 'gap', 'refuted'] as const).map((s) => (
            <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: STATUS_COLORS[s],
                  display: 'inline-block',
                }}
              />
              <span style={{ fontSize: 13, color: '#888899', textTransform: 'capitalize' }}>
                {s}
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

      {/* Steps */}
      {STEPS.map((step) => (
        <StepCard
          key={step.number}
          step={step}
          open={openSteps.has(step.number)}
          onToggle={() => toggle(step.number)}
        />
      ))}

      <p style={{ color: '#b8b8c0', lineHeight: 1.7, marginTop: 32 }}>
        Clinical observations are motivation, not evidence of PDE singularities.
        The analytical identities above have explicit assumptions. Numerical samples check
        their implementation only. This page does not assess the current status of a general
        Navier–Stokes problem. Synthetic teaching use only; not validated for patient care.
      </p>
    </div>
  )
}
