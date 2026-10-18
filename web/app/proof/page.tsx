'use client'
import { useState } from 'react'
import { K, Eq } from '@/components/Katex'

const STATUS_COLORS: Record<string, string> = {
  established: '#4ade80',
  proposed: '#facc15',
  open: '#ef4444',
}

interface ProofStepData {
  number: number
  title: string
  status: 'established' | 'proposed' | 'open'
  statementTeX: string
  approach: string
  clinical: string
  refs: string[]
}

const STEPS: ProofStepData[] = [
  {
    number: 1,
    title: 'Energy Inequality for Surface-Tension-Bounded Domains',
    status: 'established',
    statementTeX: String.raw`\frac{d}{dt}\|u\|^2 + 2\nu\|\nabla u\|^2 = \int_\Gamma \gamma\kappa(u \cdot n)\,dS`,
    approach:
      'Standard energy estimate by testing against u. The boundary integral arises from integration by parts with the dynamic pressure BC p|_Γ = p_ext + γκ (Laplace-Young). Classical when Γ is smooth.',
    clinical:
      'Energy inequality = total work of breathing must be balanced by viscous dissipation + surface tension work. Measurable: W_breathing = ∫P dV per cycle.',
    refs: ['Leray (1934)', 'Solonnikov (1977)', 'Beale (1981)'],
  },
  {
    number: 2,
    title: 'Surface Tension Work Bound',
    status: 'established',
    statementTeX: String.raw`\left|\int_\Gamma \gamma\kappa(u \cdot n)\,dS\right| \leq C \cdot \gamma \cdot \kappa_{\max} \cdot \|\nabla u\|_{L^2(\Omega)}`,
    approach:
      "Apply Hölder's inequality on the boundary integral, then the trace theorem to bound ||u||_{L²(Γ)} by ||u||_{H¹(Ω)}. The constant C depends on domain geometry.",
    clinical:
      'The maximum pressure a collapsing alveolus can exert on the airflow is bounded by γ/r_min (Laplace pressure). This is directly measurable on the ventilator.',
    refs: ['Adams & Fournier (2003)', 'Temam (1977)'],
  },
  {
    number: 3,
    title: 'Critical Threshold from the Energy Balance',
    status: 'proposed',
    statementTeX: String.raw`\frac{d}{dt}\|u\|^2 + \nu\|\nabla u\|^2 \leq \frac{C^2\gamma^2\kappa_{\max}^2}{4\nu}`,
    approach:
      "Substitute Step 2 into Step 1. Apply Young's inequality to absorb the gradient term. The RHS is bounded iff γ·κ_max < ∞, i.e., iff Λ < ∞. When γ·κ_max is bounded, energy dissipation dominates surface tension forcing. When γ·κ_max → ∞ (alveolar collapse), forcing overwhelms dissipation.",
    clinical:
      'This IS the clinical observation: when surfactant is present (γ low), the lung maintains stable breathing (energy bounded). When surfactant is absent and alveoli collapse (r→0, κ→∞), breathing fails (energy unbounded). The critical Λ* corresponds to the compliance threshold below which the baby needs surfactant.',
    refs: ['Constantin & Foias (1988)', 'Caffarelli, Kohn & Nirenberg (1982)'],
  },
  {
    number: 4,
    title: 'Enstrophy Control Under the Critical Threshold',
    status: 'proposed',
    statementTeX: String.raw`\frac{d}{dt}\Xi + \nu\|\nabla\omega\|^2 \leq C(\Lambda^*)\,\Xi`,
    approach:
      'Take the curl of NS, test against ω. The vortex stretching term (ω·∇)u is bounded using the energy estimate from Step 3. Low Re helps: stretching is weak relative to viscous damping. By Gronwall: Ξ(t) ≤ Ξ(0)·exp(C·t), hence bounded.',
    clinical:
      'Enstrophy bounded = flow gradients stay smooth = no turbulent transition in the airway. Clinically Re ~ 1–100 in neonatal airways, far from turbulent (Re ~ 4000). The only blowup mechanism is the surface tension singularity, not turbulence.',
    refs: ['Beale, Kato & Majda (1984)', 'Constantin (1990)'],
  },
  {
    number: 5,
    title: 'Regularity from Bounded Enstrophy (BKM Extension)',
    status: 'proposed',
    statementTeX: String.raw`\int_0^T \|\omega\|_\infty\,dt < \infty \;\Longrightarrow\; u \in C^\infty(\Omega \times [0,T])`,
    approach:
      'By the Beale-Kato-Majda criterion, bounded time-integrated vorticity implies smoothness. Bounded enstrophy (Step 4) combined with Sobolev embedding H¹ ↪ L⁶ (3D) gives ||ω||_∞ ≤ C·||ω||_{H¹}. The bootstrap: energy control → enstrophy control → L^∞ vorticity control → regularity.',
    clinical:
      'If the peak flow acceleration (proxy for vorticity) stays bounded across all breaths, the baby maintains stable respiration. This is what the enstrophy proxy monitors from the flow signal.',
    refs: ['Beale, Kato & Majda (1984)', 'Escauriaza, Seregin & Šverák (2003)'],
  },
  {
    number: 6,
    title: 'Blowup Construction (Converse Direction)',
    status: 'open',
    statementTeX: String.raw`\Lambda(t^*) \geq \Lambda^* \;\Longrightarrow\; \|\nabla u(t)\|_{L^2} \to \infty \text{ as } t \to t^*`,
    approach:
      'Model a single collapsing alveolus as a shrinking sphere with Laplace-Young BC. As r(t) → 0, boundary velocity diverges ∝ 1/r² and the pressure field diverges ∝ 1/r. This is a constructive example, not abstract existence.',
    clinical:
      'This IS atelectasis. The alveolus collapses, pressure diverges, the baby cannot exchange gas. Clinically observable: compliance → 0, peak pressure → ∞ (ventilator limits), volume → 0. The "blowup" is real and measurable.',
    refs: ['Tao (2016)', 'Hou & Luo (2014)'],
  },
  {
    number: 7,
    title: 'Regularization Restores Smoothness',
    status: 'proposed',
    statementTeX: String.raw`\gamma \downarrow \text{ at } t_1,\;\Lambda(t)<\Lambda^*\;\text{for } t>t_1,\;u(t_1)\in L^2 \;\Longrightarrow\; u \in C^\infty(\Omega \times (t_1,\infty))`,
    approach:
      'Use the energy inequality from Step 3 with the reduced γ. Energy dissipates faster than it is forced. Standard parabolic regularity gives instantaneous smoothing of L² data under NS when the forcing is subcritical. Key: u(t₁) need not be smooth — the NS operator itself smooths it.',
    clinical:
      'This is the clinical miracle of surfactant therapy. A baby in respiratory failure (singular regime) receives surfactant → within minutes, compliance improves, gas exchange restores, the baby breathes. The "singular solution" is regularized. Every NICU clinician has witnessed this transition.',
    refs: ['Kato (1984)', 'Giga & Miyakawa (1985)'],
  },
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
              Clinical Analog
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
          Proof Outline
        </h1>
        <p style={{ color: '#888899', fontSize: 17, lineHeight: 1.6, maxWidth: 680, margin: 0 }}>
          Seven steps toward conditional regularity for Navier-Stokes with
          surface-tension boundary conditions
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
          {(['established', 'proposed', 'open'] as const).map((s) => (
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

      {/* What Makes This Tractable */}
      <div style={{ marginTop: 56, marginBottom: 40 }}>
        <h2
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 24,
            color: '#e8e8ed',
            marginBottom: 20,
            letterSpacing: '-0.01em',
          }}
        >
          What Makes This Tractable
        </h2>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {[
            ['Bounded domain', 'Finite lung volume — no infinite-domain complications'],
            ['Low Reynolds number', 'Re ~ 1–100 in neonatal airways, far from turbulence (Re ~ 4000)'],
            ['Single blowup mechanism', 'Laplace pressure singularity at collapsing interfaces — identified and isolated'],
            ['Measurable regularization', 'Exogenous surfactant is a tunable parameter that controls γ directly'],
            ['High-resolution clinical data', 'Ventilator waveforms at 100 Hz with pressure, flow, and volume'],
            ['Complete trajectory', 'N = 1 time series capturing approach to and retreat from the singularity'],
          ].map(([title, desc], i) => (
            <li
              key={i}
              style={{
                display: 'flex',
                gap: 14,
                marginBottom: 14,
                alignItems: 'flex-start',
              }}
            >
              <span style={{ color: '#6b8afd', fontSize: 14, marginTop: 3, flexShrink: 0 }}>●</span>
              <div>
                <span style={{ color: '#e8e8ed', fontWeight: 600, fontSize: 15 }}>{title}</span>
                <span style={{ color: '#888899', fontSize: 14 }}> — {desc}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* What This Is Not */}
      <div
        style={{
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid rgba(255,255,255,0.06)',
          borderRadius: 12,
          padding: '24px 28px',
          marginBottom: 48,
        }}
      >
        <h2
          style={{
            fontFamily: 'Georgia, serif',
            fontSize: 20,
            color: '#888899',
            marginBottom: 12,
          }}
        >
          What This Is Not
        </h2>
        <p style={{ color: '#888899', fontSize: 15, lineHeight: 1.7, margin: 0 }}>
          This is not a claim to solve the Millennium Problem in full generality.
          It is a conditional regularity result for a physically restricted class
          of NS problems where the blowup mechanism is identified, measurable,
          and controllable. The value: it provides a concrete physical system where
          NS regularity and blowup are <em>observed</em>, not hypothetical. The mathematics
          of the observation may illuminate the general case.
        </p>
      </div>
    </div>
  )
}
