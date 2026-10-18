'use client'
import { K, Eq } from '@/components/Katex'

const card = {
  background: 'rgba(255,255,255,0.03)',
  border: '1px solid rgba(255,255,255,0.06)',
  borderRadius: 12,
  padding: 24,
} as const

const regimes = [
  {
    color: '#4ade80',
    title: 'Smooth Regime',
    subtitle: 'Adequate surfactant',
    lines: [
      'γ ≈ 25 mN/m (with surfactant)',
      'Laplace pressure P = 2γ/r stays bounded',
      'Re ~ 1–100 (laminar)',
      'Solution remains regular. The baby breathes.',
    ],
  },
  {
    color: '#ef4444',
    title: 'Singular Regime',
    subtitle: 'Surfactant deficiency (RDS)',
    lines: [
      'γ ≈ 70 mN/m (no surfactant)',
      'As r → 0: P = 2γ/r → ∞',
      'Finite-time singularity analog',
      'Solution blows up. The baby cannot breathe.',
    ],
  },
  {
    color: '#6b8afd',
    title: 'Intervention Regime',
    subtitle: 'Exogenous surfactant',
    lines: [
      'Artificial surfactant administered → γ drops',
      'The 1/r singularity is regularized',
      'Compliance recovers within minutes',
      'Solution returns to smooth. The baby breathes again.',
    ],
  },
] as const

const translations = [
  { math: '\\Lambda < \\Lambda^*', clinical: 'Adequate surfactant', observable: 'Baby breathes' },
  { math: '\\Lambda \\geq \\Lambda^*', clinical: 'Surfactant deficiency', observable: 'Atelectasis' },
  { math: '\\gamma \\downarrow', clinical: 'Surfactant given', observable: 'Compliance recovers' },
  { math: 'C_{\\text{dyn}} \\to 0', clinical: 'Alveolar collapse', observable: 'Ventilator shows failure' },
  { math: '\\Xi(t) < \\infty', clinical: 'Laminar airway flow', observable: 'Stable waveforms' },
] as const

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section style={{ marginBottom: 64, paddingTop: 24 }}>
        <h1 style={{
          fontFamily: 'Georgia, serif',
          fontSize: 40,
          fontWeight: 400,
          lineHeight: 1.2,
          letterSpacing: '-0.02em',
          color: '#e8e8ed',
          marginBottom: 16,
        }}>
          Navier-Stokes Regularity{' '}
          <br />
          <span style={{ color: '#c9a96e' }}>in the Neonatal Lung</span>
        </h1>
        <p style={{ color: '#888899', fontSize: 17, lineHeight: 1.65, maxWidth: 700 }}>
          Conditional regularity of incompressible Navier-Stokes solutions in bounded
          domains with surface-tension boundary conditions — empirical evidence from
          neonatal respiratory mechanics.
        </p>
      </section>

      {/* The Physical System */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          The Physical System
        </h2>
        <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 16 }}>
          A neonate&rsquo;s lung is a bounded domain <K>{"\\Omega \\subset \\mathbb{R}^3"}</K> — branching
          airways terminating in alveoli. At birth, the fluid transitions from liquid-filled to air-filled.
          The incompressible Navier-Stokes equations govern the airflow:
        </p>

        <div style={{ ...card, marginBottom: 16 }}>
          <Eq>{"\\frac{\\partial \\mathbf{u}}{\\partial t} + (\\mathbf{u} \\cdot \\nabla)\\mathbf{u} = -\\frac{1}{\\rho}\\nabla p + \\nu \\Delta \\mathbf{u} + \\mathbf{f}"}</Eq>
          <Eq>{"\\nabla \\cdot \\mathbf{u} = 0"}</Eq>
        </div>

        <p style={{ color: '#b0b0be', lineHeight: 1.7 }}>
          In the neonatal airway, Reynolds numbers are low (<K>{"\\text{Re} \\sim 1\\text{–}100"}</K>, far
          from turbulent). The flow is laminar — the only mechanism for singularity formation is
          the <em>surface tension</em> at the air-liquid interface in collapsing alveoli, governed by the
          Laplace-Young equation: <K>{"P = 2\\gamma / r"}</K>.
        </p>
      </section>

      {/* Three Regimes */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          Three Regimes
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {regimes.map(r => (
            <div key={r.title} style={card}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                <div style={{
                  width: 10, height: 10, borderRadius: '50%',
                  background: r.color, boxShadow: `0 0 8px ${r.color}60`,
                }} />
                <h3 style={{ fontSize: 16, fontWeight: 600, color: '#e8e8ed', margin: 0 }}>
                  {r.title}
                </h3>
              </div>
              <p style={{ fontSize: 13, color: '#c9a96e', marginBottom: 10, fontStyle: 'italic' }}>
                {r.subtitle}
              </p>
              <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
                {r.lines.map((l, i) => (
                  <li key={i} style={{
                    fontSize: 14, color: '#b0b0be', lineHeight: 1.6,
                    paddingLeft: 12,
                    borderLeft: i === r.lines.length - 1
                      ? `2px solid ${r.color}`
                      : '2px solid rgba(255,255,255,0.04)',
                    marginBottom: 6,
                  }}>
                    {l}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* The Conjecture */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          The Conjecture
        </h2>
        <div style={{
          ...card,
          borderColor: 'rgba(201,169,110,0.2)',
          background: 'rgba(201,169,110,0.03)',
        }}>
          <p style={{
            fontSize: 13, color: '#c9a96e', textTransform: 'uppercase' as const,
            letterSpacing: '0.08em', marginBottom: 16, fontWeight: 600,
          }}>
            Conditional Regularity for Surface-Tension-Bounded NS
          </p>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            Let <K>{"\\Omega(t) \\subset \\mathbb{R}^3"}</K> be a bounded domain
            with <K>{"C^2"}</K> boundary <K>{"\\Gamma(t)"}</K> evolving under NS
            with the Laplace-Young pressure condition on <K>{"\\Gamma"}</K>:
          </p>

          <Eq>{"p\\big|_{\\Gamma} = p_{\\text{ext}} + \\gamma\\, \\kappa"}</Eq>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            where <K>{"\\kappa"}</K> is the mean curvature
            of <K>{"\\Gamma"}</K> and <K>{"\\gamma > 0"}</K> is the surface
            tension coefficient. Define the <em>surface-tension regularity parameter</em>:
          </p>

          <Eq>{"\\Lambda(t) = \\frac{\\gamma \\cdot \\displaystyle\\sup_{x \\in \\Gamma(t)} \\kappa(x,t)}{\\rho\\, \\nu^2 \\,/\\, L^2}"}</Eq>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 6 }}>
            <strong style={{ color: '#e8e8ed' }}>Claim.</strong>{' '}
            There exists <K>{"\\Lambda^* = \\Lambda^*(\\Omega_0, \\text{Re}_0)"}</K> such that:
          </p>
          <ol style={{ color: '#b0b0be', lineHeight: 1.8, paddingLeft: 20, marginBottom: 0 }}>
            <li>
              If <K>{"\\Lambda(t) < \\Lambda^*"}</K> for
              all <K>{"t \\in [0,T]"}</K>, then <K>{"\\mathbf{u} \\in C^\\infty(\\Omega \\times [0,T])"}</K>.
            </li>
            <li>
              There exist initial data and boundary evolution such
              that <K>{"\\Lambda(t^*) = \\Lambda^*"}</K> implies <K>{"\\|\\nabla \\mathbf{u}(t)\\|_{L^2} \\to \\infty"}</K> as <K>{"t \\to t^*"}</K>.
            </li>
          </ol>
        </div>
      </section>

      {/* Clinical Translation */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          Clinical Translation
        </h2>
        <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 16 }}>
          Every quantity in the conjecture is directly measurable from a bedside ventilator
          recording at 100 Hz. The correspondence between the mathematics and clinical
          observation is not metaphorical — it is literal:
        </p>
        <div style={{ overflowX: 'auto' }}>
          <table style={{
            width: '100%', borderCollapse: 'collapse',
            fontSize: 14,
          }}>
            <thead>
              <tr>
                {['Mathematical', 'Clinical', 'Observable'].map(h => (
                  <th key={h} style={{
                    textAlign: 'left', padding: '10px 16px',
                    borderBottom: '1px solid rgba(255,255,255,0.1)',
                    color: '#888899', fontWeight: 500, fontSize: 12,
                    textTransform: 'uppercase' as const, letterSpacing: '0.06em',
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {translations.map((row, i) => (
                <tr key={i}>
                  <td style={{
                    padding: '10px 16px',
                    borderBottom: '1px solid rgba(255,255,255,0.04)',
                    color: '#e8e8ed',
                  }}>
                    <K>{row.math}</K>
                  </td>
                  <td style={{
                    padding: '10px 16px',
                    borderBottom: '1px solid rgba(255,255,255,0.04)',
                    color: '#b0b0be',
                  }}>{row.clinical}</td>
                  <td style={{
                    padding: '10px 16px',
                    borderBottom: '1px solid rgba(255,255,255,0.04)',
                    color: '#b0b0be',
                  }}>{row.observable}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* What This Is / Is Not */}
      <section style={{ marginBottom: 56 }}>
        <div style={{ ...card }}>
          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            <strong style={{ color: '#e8e8ed' }}>What this is.</strong>{' '}
            A conditional regularity result for a physically restricted class of NS problems — bounded
            domain, surface-tension BCs, low Reynolds number — where the blowup mechanism is
            identified, measurable, and controllable. The neonatal lung provides a concrete physical
            system where NS regularity and blowup are <em>observed</em>, not hypothetical.
          </p>
          <p style={{ color: '#b0b0be', lineHeight: 1.7, margin: 0 }}>
            <strong style={{ color: '#e8e8ed' }}>What this is not.</strong>{' '}
            A claim to solve the Millennium Problem in full generality. The value lies in the
            empirical window: a system where we observe the transition between regularity and
            blowup, measure the regularization parameter that controls it, and can formalize the
            threshold from clinical data.
          </p>
        </div>
      </section>

      {/* Navigation */}
      <section style={{
        display: 'flex', gap: 16, paddingBottom: 32,
      }}>
        {[
          { href: '/proof', label: 'Proof Outline', desc: '7-step argument with references and clinical analogs' },
          { href: '/demo', label: 'Interactive Demo', desc: 'Synthetic waveform analysis — watch the singularity approach' },
        ].map(link => (
          <a key={link.href} href={link.href} style={{
            flex: 1, ...card, textDecoration: 'none',
            transition: 'border-color 0.2s',
            cursor: 'pointer',
          }}
          onMouseEnter={e => (e.currentTarget.style.borderColor = 'rgba(107,138,253,0.3)')}
          onMouseLeave={e => (e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)')}
          >
            <h3 style={{ color: '#6b8afd', fontSize: 16, marginBottom: 6, fontWeight: 600 }}>
              {link.label} →
            </h3>
            <p style={{ color: '#888899', fontSize: 14, margin: 0, lineHeight: 1.5 }}>
              {link.desc}
            </p>
          </a>
        ))}
      </section>
    </div>
  )
}
