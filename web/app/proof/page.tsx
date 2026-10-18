'use client'
import { useState } from 'react'
import { Eq } from '@/components/Katex'

type Status = 'standard' | 'conjecture' | 'analogy'

const STATUS: Record<Status, { label: string; color: string; desc: string }> = {
  standard: { label: 'Standard result (cited)', color: '#4ade80', desc: 'a known theorem, in the setting where it was proved' },
  conjecture: { label: 'Conjecture, not proved', color: '#ef4444', desc: 'open; nothing here proves it' },
  analogy: { label: 'Analogy', color: '#6b8afd', desc: 'a clinical comparison, not a mathematical statement' },
}

interface ProofStepData {
  number: number
  title: string
  status: Status
  statementTeX: string[]
  approach: string
  clinical: string
  changed?: string
  refs: string[]
}

const STEPS: ProofStepData[] = [
  {
    number: 1,
    title: 'Energy Balance for a Surface-Tension-Bounded Domain',
    status: 'standard',
    statementTeX: [
      String.raw`\frac{d}{dt}\Big(\frac{\rho}{2}\|u\|_{L^2(\Omega(t))}^2 + \gamma\,|\Gamma(t)|\Big) + 2\mu\|D(u)\|_{L^2}^2 = -\int_{\Gamma(t)} p_{\text{ext}}\,(u\cdot n)\,dS`,
    ],
    approach:
      'Test the equations against u and integrate by parts, using the full stress condition (−pI + 2μD(u))n = −(p_ext + γκ)n on a boundary Γ(t) that moves with the fluid. For constant γ the surface-tension work equals −γ d|Γ|/dt, so it appears as a surface energy γ|Γ| on the left. D(u) is the symmetric gradient and μ = ρν. This identity holds for smooth solutions while they exist. In a fixed domain with no-slip walls, Leray–Hopf weak solutions satisfy the corresponding energy inequality.',
    clinical:
      'Each breath, the work ∫P dV done by the muscles or the ventilator goes partly into resistive (viscous) losses and partly into stretching tissue and the alveolar surface. The term γ|Γ| is the surface-energy part of that work.',
    changed:
      'The earlier version wrote d/dt‖u‖² + 2ν‖∇u‖² = ∫γκ(u·n) dS. With a free boundary the dissipation is 2μ‖D(u)‖², and the surface-tension work is the rate of change of surface energy.',
    refs: [
      'Leray (1934): weak solutions and the energy inequality on ℝ³',
      'Hopf (1951): the same in bounded domains',
      'Solonnikov (1977): viscous fluid bounded by a free surface, local solvability',
      'Beale (1981): free-surface Navier–Stokes without surface tension, local existence',
      'Beale (1984): viscous surface waves with surface tension',
    ],
  },
  {
    number: 2,
    title: 'Surface Tension Work Bound',
    status: 'standard',
    statementTeX: [
      String.raw`\left|\int_\Gamma \gamma\kappa\,(u \cdot n)\,dS\right| \leq C_\Omega\, \gamma\, \kappa_{\max}\, \|u\|_{H^1(\Omega)}`,
    ],
    approach:
      "Hölder's inequality on the boundary integral, then the trace theorem, which bounds ‖u‖ in L²(Γ) by ‖u‖ in H¹(Ω). This is standard for a fixed smooth domain. The constant C_Ω depends on the geometry and degenerates as the domain does, which is exactly the collapsing case.",
    clinical:
      'In the single-bubble picture, the Laplace pressure 2γ/r_min is the largest pressure the surface of the smallest alveolus exerts. It is not measured directly at the bedside: the ventilator measures pressure at the airway opening, which reflects the whole lung.',
    changed:
      'The earlier version bounded the integral by ‖∇u‖ alone and called γ/r_min directly measurable. Without no-slip walls the full H¹ norm is needed, the Laplace pressure is 2γ/r, and it is not a bedside measurement.',
    refs: [
      'Adams & Fournier (2003): Sobolev spaces and the trace theorem',
      'Temam (1977): Navier–Stokes equations, function spaces',
    ],
  },
  {
    number: 3,
    title: 'What the Energy Balance Gives (and Does Not)',
    status: 'standard',
    statementTeX: [
      String.raw`\frac{\rho}{2}\|u(t)\|^2 + \gamma|\Gamma(t)| + 2\mu\!\int_0^t\!\|D(u)\|^2\,ds \;\le\; \frac{\rho}{2}\|u_0\|^2 + \gamma|\Gamma_0| + W_{\text{ext}}(t)`,
    ],
    approach:
      'Integrate Step 1 in time; W_ext is the work done by the external pressure. Surface tension stores energy; it does not create it. Kinetic plus surface energy can only fall, apart from external work, so a large γ·κ_max cannot by itself drive the energy to infinity. No critical threshold comes out of the energy balance.',
    clinical:
      'The decision to give surfactant is made mainly on oxygen need and signs of respiratory distress, not on a computed threshold of a parameter like Λ.',
    changed:
      'The earlier version used Step 2 and Young\'s inequality to claim that the energy stays bounded if and only if γ·κ_max is bounded, and that it becomes unbounded when alveoli collapse. That does not follow: a bound that weakens is not a blow-up, and the identity above shows the energy stays bounded by its initial value plus the external work W_ext.',
    refs: ['Beale (1984): energy identity with surface energy'],
  },
  {
    number: 4,
    title: 'Enstrophy Control Below a Threshold?',
    status: 'conjecture',
    statementTeX: [
      String.raw`\text{known: }\;\frac{d}{dt}\Xi + \nu\|\nabla\omega\|^2 \leq \frac{C}{\nu^3}\,\Xi^3, \qquad \Xi = \|\omega\|_{L^2}^2`,
      String.raw`\text{conjectured, not proved: }\;\frac{d}{dt}\Xi \leq C(\Lambda^*)\,\Xi \quad \text{while } \Lambda(t) < \Lambda^*`,
    ],
    approach:
      'Taking the curl and testing against ω gives the first line, on the periodic cube or all of space (in a bounded domain the same cubic form holds for ‖∇u‖²). It controls Ξ for a short time, or for all time when the data are small compared with the viscosity: low Reynolds number in that sense. A linear bound with a constant depending only on Λ* would remove the central difficulty of the regularity problem. No such bound is known, and nothing here proves it.',
    clinical:
      'Low Reynolds number in the small airways and alveoli plays the role of small data. In the larger airways Re is higher (a few hundred to about a thousand in a newborn\'s trachea), but laminar or not, the physical flow raises no blow-up question; the open problem is about idealised smooth solutions with arbitrary data.',
    changed:
      'The earlier version claimed the linear bound followed from Step 3 by Gronwall. It does not: Step 3 controls energy, not vortex stretching.',
    refs: [
      'Fujita & Kato (1964): global smooth solutions for small data',
      'Doering & Gibbon (1995): the enstrophy inequality',
      'Robinson, Rodrigo & Sadowski (2016): classical theory',
    ],
  },
  {
    number: 5,
    title: 'Regularity from Bounded Enstrophy (Continuation Criteria)',
    status: 'standard',
    statementTeX: [
      String.raw`\sup_{t<T}\|\nabla u(t)\|_{L^2} < \infty \;\Longrightarrow\; \text{the smooth solution continues past } T`,
      String.raw`\int_0^T \|\omega\|_{L^\infty}\,dt < \infty \;\Longrightarrow\; \text{the smooth solution continues past } T \quad \text{(BKM)}`,
    ],
    approach:
      'Both are continuation criteria for smooth solutions in a fixed domain: a smooth solution can only stop being smooth at T if the quantity on the left becomes infinite there. The first follows from local existence in H¹ (Leray\'s lower bound on the blow-up rate). The second is the Beale–Kato–Majda criterion, proved on ℝ³ for the Euler equations; the same criterion holds for Navier–Stokes. This step is conditional: it would give regularity only if Step 4 held. It has not been extended here to the free-boundary problem.',
    clinical:
      'The ventilator measures flow and pressure at the airway opening, one number at each instant. It cannot see vorticity inside the lung, so no bedside signal is a proxy for ‖ω‖∞.',
    changed:
      'The earlier version derived ‖ω‖∞ ≤ C‖ω‖_{H¹} from H¹ ↪ L⁶. In three dimensions H¹ does not embed in L∞, so that bootstrap fails; the first criterion above is the correct route.',
    refs: [
      'Leray (1934): blow-up rate of ‖∇u‖',
      'Beale, Kato & Majda (1984): vorticity continuation criterion',
      'Escauriaza, Seregin & Šverák (2003): bounded L³ norm implies smoothness',
    ],
  },
  {
    number: 6,
    title: 'The Converse Direction: Blow-up Above a Threshold?',
    status: 'conjecture',
    statementTeX: [
      String.raw`\Lambda(t^*) \geq \Lambda^* \;\overset{?}{\Longrightarrow}\; \|\nabla u(t)\|_{L^2} \to \infty \text{ as } t \to t^*`,
    ],
    approach:
      'No construction exists. A closed sphere of incompressible fluid cannot shrink, because its volume is conserved: a collapsing alveolus empties through its duct, so a model needs an open boundary. The 1/r growth in 2γ/r is a property of the formula; a real alveolus closes at finite size. Free surfaces can form genuine singularities, such as the pinch-off of a liquid thread, but those are singularities of the interface, not the Millennium question. Tao (2016) proves blow-up for an averaged equation, not Navier–Stokes, and Luo & Hou (2014) is numerical evidence for the Euler equations.',
    clinical:
      'Atelectasis is real and measurable: falling compliance, rising oxygen need, a ground-glass chest X-ray. It is not a blow-up. The alveolus closes at finite size, pressures stay finite, and nothing becomes infinite. Collapse is governed by surface tension, the Laplace law and tissue mechanics.',
    changed:
      'The earlier version called this a constructive example and said the blow-up is real and measurable. It is neither.',
    refs: [
      'Rayleigh (1917): collapse of a spherical cavity in a liquid',
      'Eggers (1997): free-surface breakup and its singularities',
      'Tao (2016): blow-up for an averaged Navier–Stokes equation',
      'Luo & Hou (2014): potential singularity of 3D axisymmetric Euler with a boundary, numerical',
    ],
  },
  {
    number: 7,
    title: 'Does Lowering γ Restore Smoothness?',
    status: 'conjecture',
    statementTeX: [
      String.raw`\gamma \downarrow \text{ at } t_1,\;\Lambda(t)<\Lambda^*\;\text{for } t>t_1,\;u(t_1)\in L^2 \;\overset{?}{\Longrightarrow}\; u \in C^\infty(\Omega \times (t_1,\infty))`,
    ],
    approach:
      'As stated, this would give smoothness at every later time from L² data, which in three dimensions is the open problem itself. What is known: from L² data, Leray–Hopf weak solutions exist for all time; on all of space with no force they are smooth after some finite time and at almost every time (Leray), and suitable weak solutions have a small singular set (Caffarelli, Kohn & Nirenberg). From data in critical spaces such as L³, smooth solutions exist for a short time, and for all time if the data are small (Kato; Giga & Miyakawa).',
    clinical:
      'This is the clinical miracle of surfactant therapy. Surfactant replacement is one of the best-tested treatments in neonatology. After a dose, oxygen need often falls within minutes, and compliance improves more slowly; many NICU clinicians have watched that change. In the analogy the "singular" regime returns to the "smooth" one. In the lung, alveoli reopen and stay open.',
    changed:
      'The earlier version said standard parabolic regularity smooths L² data instantly. That is not known for 3D Navier–Stokes.',
    refs: [
      'Leray (1934): eventual regularity',
      'Caffarelli, Kohn & Nirenberg (1982): partial regularity',
      'Kato (1984): strong Lᵖ solutions',
      'Giga & Miyakawa (1985): Lʳ solutions in bounded domains',
    ],
  },
]

function Badge({ status }: { status: Status }) {
  const s = STATUS[status]
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
        color: s.color,
        border: `1px solid ${s.color}44`,
        background: `${s.color}11`,
        whiteSpace: 'nowrap',
      }}
    >
      {s.label}
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
        aria-expanded={open}
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
        <span style={{ flex: 1, minWidth: 0 }}>
          <span style={{ display: 'block', fontSize: 16, fontWeight: 500, marginBottom: 6 }}>
            {step.title}
          </span>
          <Badge status={step.status} />
        </span>
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
        <div style={{ padding: '0 20px 20px clamp(20px, 6vw, 62px)' }}>
          {/* Math statement */}
          <div style={{ margin: '0 0 16px' }}>
            {step.statementTeX.map((tex, i) => <Eq key={i}>{tex}</Eq>)}
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
                display: 'flex',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: 8,
                marginBottom: 6,
              }}
            >
              <span
                style={{
                  fontSize: 10,
                  letterSpacing: '0.1em',
                  textTransform: 'uppercase',
                  color: '#c9a96e',
                  fontWeight: 600,
                }}
              >
                Clinical Analog
              </span>
              <Badge status="analogy" />
            </div>
            <p style={{ color: '#b8b8c0', fontSize: 14, fontStyle: 'italic', lineHeight: 1.6, margin: 0 }}>
              {step.clinical}
            </p>
          </div>

          {/* What changed */}
          {step.changed && (
            <p style={{ color: '#888899', fontSize: 13, lineHeight: 1.6, margin: '0 0 12px' }}>
              <span style={{ fontWeight: 600 }}>What changed: </span>
              {step.changed}
            </p>
          )}

          {/* References */}
          <div style={{ fontSize: 13, color: '#888899', lineHeight: 1.6 }}>
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
          The Argument, Step by Step
        </h1>
        <p style={{ color: '#888899', fontSize: 17, lineHeight: 1.6, maxWidth: 680, margin: 0 }}>
          Seven steps from the energy balance to the question on the home page. Every step carries a
          status: four are standard results, cited in the setting where they were proved; three are
          conjectures that nothing here proves. The clinical notes are analogies.
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
        <div style={{ display: 'flex', flexWrap: 'wrap', columnGap: 16, rowGap: 6 }}>
          {(Object.keys(STATUS) as Status[]).map((s) => (
            <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 6 }} title={STATUS[s].desc}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: STATUS[s].color,
                  display: 'inline-block',
                }}
              />
              <span style={{ fontSize: 13, color: '#888899' }}>
                {STATUS[s].label}
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

      {/* Why the lung is a useful model system */}
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
          Why the Lung Is a Useful Model System
        </h2>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {[
            ['Bounded domain', 'Finite lung volume. The Millennium problem is posed on all of space or the periodic cube, so results here would not transfer to it.'],
            ['Reynolds number falls along the airway tree', 'Re is a few hundred to about a thousand in a newborn\'s trachea and falls to well below 1 in the alveoli, where the flow is close to Stokes flow.'],
            ['A dominant collapse mechanism in RDS', 'Surface tension in the alveolar lining, through the Laplace law, together with tissue mechanics. It causes collapse at finite size, not a singularity of the flow.'],
            ['A real intervention', 'Exogenous surfactant lowers γ, and PEEP or CPAP holds alveoli open: the mechanism is well understood.'],
            ['High-resolution clinical data', 'Ventilator waveforms (pressure, flow and volume at the airway opening, sampled for example at 100 Hz) give the compliance of the respiratory system as a whole.'],
            ['A case study', 'One baby\'s recording (N = 1) can show decline and recovery around a surfactant dose: a case to model, not a population result.'],
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
          This is not a regularity result, and not evidence about Navier-Stokes blow-up. The lung picture
          is an analogy and a modelling programme. The steps that would link surface tension to
          regularity or blow-up (4, 6 and 7) are conjectures that nothing here proves. Alveolar collapse
          is a clinical event governed by surface tension, the Laplace law P = 2γ/r and tissue
          mechanics; it happens at finite size and is not a singularity of the Navier-Stokes equations.
          This work does not touch the Millennium problem; its current status is on
          the <a href="/" style={{ color: '#6b8afd', textDecoration: 'none' }}>home page</a>.
        </p>
      </div>
    </div>
  )
}
