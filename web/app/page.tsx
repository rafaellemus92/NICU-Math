'use client'
import { K, Eq } from '@/components/Katex'

const card = {
  background: 'rgba(255,255,255,0.03)',
  border: '1px solid rgba(255,255,255,0.06)',
  borderRadius: 12,
  padding: 24,
} as const

const REPO = 'https://github.com/rafaellemus92/nicu-math/blob/main/math'

const link = { color: '#6b8afd', textDecoration: 'none' } as const

const regimes = [
  {
    color: '#4ade80',
    title: 'Stable Regime',
    subtitle: 'Adequate surfactant',
    lines: [
      'γ ≈ 25 mN/m at equilibrium, near 0 when the surface is compressed on expiration',
      'Laplace pressure P = 2γ/r stays small as r shrinks',
      'Alveolar flow: Re ≪ 1 (Stokes regime)',
      'Alveoli stay open. The baby breathes.',
    ],
  },
  {
    color: '#ef4444',
    title: 'Collapse Regime',
    subtitle: 'Surfactant deficiency (RDS)',
    lines: [
      'γ stays high, up to about 70 mN/m (a bare water–air surface)',
      'As r shrinks on expiration, 2γ/r rises and alveoli tend to collapse',
      'Collapse happens at finite size: a clinical event, not a PDE singularity',
      'Atelectasis. The baby struggles to breathe.',
    ],
  },
  {
    color: '#6b8afd',
    title: 'Intervention Regime',
    subtitle: 'Exogenous surfactant',
    lines: [
      'Surfactant given into the trachea → γ falls',
      'With PEEP or CPAP, collapsed alveoli reopen and stay open',
      'Oxygenation often improves within minutes; compliance more slowly',
      'The baby breathes more easily again.',
    ],
  },
] as const

const translations = [
  { math: '\\Lambda < \\Lambda^*', clinical: 'Adequate surfactant', observable: 'Stable breathing, low oxygen need' },
  { math: '\\Lambda \\geq \\Lambda^*', clinical: 'Surfactant deficiency (RDS)', observable: 'Atelectasis, with grunting, recession and rising oxygen need' },
  { math: '\\gamma \\downarrow', clinical: 'Surfactant given', observable: 'Oxygen need falls; compliance follows' },
  { math: 'C_{\\text{dyn}} \\downarrow', clinical: 'Alveolar collapse', observable: 'Falling compliance on the ventilator' },
  { math: '\\Xi(t) < \\infty', clinical: 'Smooth airflow', observable: 'Not measured: the flow inside the lung is not seen at the bedside' },
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
          Navier-Stokes{' '}
          <br />
          <span style={{ color: '#c9a96e' }}>and the Neonatal Lung</span>
        </h1>
        <p style={{ color: '#888899', fontSize: 17, lineHeight: 1.65, maxWidth: 700 }}>
          An analogy and a modelling programme. The language of Navier-Stokes regularity
          (smooth, singular, regularized) is read against the way surfactant keeps a
          newborn&rsquo;s alveoli open. It is not a regularity result: alveolar collapse is a
          clinical event governed by surface tension, not a Navier-Stokes singularity.
        </p>
      </section>

      {/* The Physical System */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          The Physical System
        </h2>
        <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 16 }}>
          A neonate&rsquo;s lung is a bounded domain <K>{"\\Omega \\subset \\mathbb{R}^3"}</K>: branching
          airways ending in alveoli (in very preterm babies, their precursors, the saccules). At birth
          the airspaces clear of fetal lung fluid and fill with air. The airflow is well described by
          the incompressible Navier-Stokes equations:
        </p>

        <div style={{ ...card, marginBottom: 16 }}>
          <Eq>{"\\frac{\\partial \\mathbf{u}}{\\partial t} + (\\mathbf{u} \\cdot \\nabla)\\mathbf{u} = -\\frac{1}{\\rho}\\nabla p + \\nu \\Delta \\mathbf{u} + \\mathbf{f}"}</Eq>
          <Eq>{"\\nabla \\cdot \\mathbf{u} = 0"}</Eq>
        </div>

        <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 16 }}>
          The Reynolds number <K>{"\\text{Re} = UD/\\nu"}</K> compares inertia with viscosity. In a
          newborn&rsquo;s trachea during quiet breathing it is of order a few hundred to about a
          thousand. It falls with each airway generation, because the flow divides among more and more
          branches whose total cross-section grows, to well below 1 in the alveolar region. There the
          inertial term <K>{"(\\mathbf{u} \\cdot \\nabla)\\mathbf{u}"}</K> is negligible and the flow is
          Stokes flow, governed by linear equations that do not blow up. That is exactly why
          Navier-Stokes blow-up questions do not arise in the alveoli.
        </p>
        <p style={{ color: '#b0b0be', lineHeight: 1.7 }}>
          What closes an alveolus is surface tension in the thin liquid layer that lines it. In the
          classic picture, the pressure needed to hold an alveolus of radius <K>{"r"}</K> open is given
          by the Laplace law <K>{"P = 2\\gamma / r"}</K>. If <K>{"\\gamma"}</K> stays fixed, that pressure
          rises as <K>{"r"}</K> shrinks on expiration, and small alveoli tend to empty and collapse.
          Surfactant lowers <K>{"\\gamma"}</K>, and lowers it further as the surface is compressed, so
          the pressure stays small. Real alveoli are polyhedral and share walls, so the single-bubble
          law is a simplification.
        </p>
      </section>

      {/* Three Regimes */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          Three Regimes
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16 }}>
          {regimes.map(r => (
            <div key={r.title} style={{ ...card, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                <div style={{
                  width: 10, height: 10, borderRadius: '50%', flexShrink: 0,
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

      {/* The Question */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          The Question
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
            A free-boundary model and an open question
          </p>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            Model the gas in an alveolus as an incompressible viscous fluid in a
            domain <K>{"\\Omega(t) \\subset \\mathbb{R}^3"}</K> whose boundary <K>{"\\Gamma(t)"}</K> is
            an air&ndash;liquid interface with surface tension <K>{"\\gamma > 0"}</K>. For fluid at rest,
            the normal-stress balance on <K>{"\\Gamma"}</K> is the Young&ndash;Laplace condition:
          </p>

          <Eq>{"p\\big|_{\\Gamma} = p_{\\text{ext}} + \\gamma\\, \\kappa"}</Eq>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            where <K>{"p_{\\text{ext}}"}</K> is the pressure in the liquid lining and <K>{"\\kappa"}</K> is
            the curvature of <K>{"\\Gamma"}</K>, the sum of its principal curvatures
            (so <K>{"\\kappa = 2/r"}</K> on a sphere of radius <K>{"r"}</K>, which gives <K>{"P = 2\\gamma/r"}</K>).
            For moving fluid the condition also includes the viscous normal stress. Define
            the <em>surface-tension parameter</em>, the largest Laplace pressure measured against the
            viscous pressure scale <K>{"\\rho\\nu^2/L^2"}</K>:
          </p>

          <Eq>{"\\Lambda(t) = \\frac{\\gamma \\cdot \\displaystyle\\sup_{x \\in \\Gamma(t)} \\kappa(x,t)}{\\rho\\, \\nu^2 \\,/\\, L^2}"}</Eq>

          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 6 }}>
            <strong style={{ color: '#e8e8ed' }}>Question (conjecture, not proved).</strong>{' '}
            Is there a <K>{"\\Lambda^* = \\Lambda^*(\\Omega_0, \\text{Re}_0)"}</K> such that:
          </p>
          <ol style={{ color: '#b0b0be', lineHeight: 1.8, paddingLeft: 20, marginBottom: 12, listStyleType: 'decimal' }}>
            <li>
              if <K>{"\\Lambda(t) < \\Lambda^*"}</K> for
              all <K>{"t \\in [0,T]"}</K>, then <K>{"\\mathbf{u} \\in C^\\infty(\\Omega \\times [0,T])"}</K>;
            </li>
            <li>
              there are initial data and a boundary evolution for
              which <K>{"\\Lambda(t^*) = \\Lambda^*"}</K> and <K>{"\\|\\nabla \\mathbf{u}(t)\\|_{L^2} \\to \\infty"}</K> as <K>{"t \\to t^*"}</K>?
            </li>
          </ol>
          <p style={{ color: '#b0b0be', lineHeight: 1.7, margin: 0 }}>
            Neither part is proved, and the hypotheses are not yet precise enough to be a theorem.
            Viscous free-boundary flow with surface tension is a real research field, with local
            existence results and global results for small data near equilibrium (for example Beale, 1984, for a fluid layer).
            Physically, part 2 is not expected in the lung: a collapsing alveolus closes at finite size,
            its walls are elastic tissue, and the air inside moves at <K>{"\\text{Re} \\ll 1"}</K>.
          </p>
        </div>
      </section>

      {/* Clinical Translation */}
      <section style={{ marginBottom: 56 }}>
        <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, marginBottom: 20, color: '#e8e8ed' }}>
          Clinical Translation
        </h2>
        <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 16 }}>
          Each symbol in the question has a clinical counterpart. The correspondence is an analogy, not
          an identity. A bedside ventilator recording (pressure, flow and volume at the airway opening,
          sampled for example at 100 Hz) gives compliance and resistance for the respiratory system as a whole. It does
          not measure surface tension, alveolar curvature or the flow inside the lung,
          so <K>{"\\Lambda"}</K> and <K>{"\\Xi"}</K> cannot be read off it.
        </p>
        <div style={{ overflowX: 'auto' }}>
          <table style={{
            width: '100%', borderCollapse: 'collapse',
            fontSize: 14,
          }}>
            <thead>
              <tr>
                {['Symbol', 'Clinical idea', 'What the bedside shows'].map(h => (
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
                    color: '#e8e8ed', whiteSpace: 'nowrap',
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
            An analogy and a modelling programme. The vocabulary of PDE regularity is used to think
            about how surfactant keeps alveoli open, and the free-boundary model above is one way to
            state that picture in mathematics. Its questions are conjectures; none is proved here.
          </p>
          <p style={{ color: '#b0b0be', lineHeight: 1.7, marginBottom: 12 }}>
            <strong style={{ color: '#e8e8ed' }}>What this is not.</strong>{' '}
            A regularity result, or evidence about Navier-Stokes blow-up. Alveolar collapse is a
            clinical event governed by surface tension and the Laplace law <K>{"P = 2\\gamma/r"}</K>; it
            happens at finite size and is not a singularity of the Navier-Stokes equations. The alveolar
            flow is at <K>{"\\text{Re} \\ll 1"}</K> (the Stokes regime), which is exactly why blow-up
            questions do not arise there. This work does not touch the Millennium problem.
          </p>
          <p style={{ color: '#888899', fontSize: 14, lineHeight: 1.7, margin: 0 }}>
            <strong style={{ color: '#b0b0be' }}>The Millennium problem, briefly.</strong>{' '}
            On 8 September 2026 OpenAI posted a paper, with a proof formalized in the Lean proof
            checker, of finite-time blow-up for 3D Navier-Stokes driven by a smooth external force; the
            paper says this establishes Clay&rsquo;s statement (C). On 11 September the Clay Institute
            spoke of the problem having &ldquo;apparently been settled&rdquo; and said its prize process
            &ldquo;is deliberately unhurried&rdquo;; its problem page still lists the problem as
            &ldquo;Active&rdquo;. The unforced question remains open. Sourced wording and links:{' '}
            <a href={`${REPO}/ns-phase-audit/enstrophy-jet/RESULTS.md`} style={link}>RESULTS.md &sect;8</a>.
          </p>
        </div>
      </section>

      {/* Where the mathematics lives */}
      <section style={{ marginBottom: 40 }}>
        <p style={{ color: '#b0b0be', lineHeight: 1.7, margin: 0 }}>
          The mathematics done for this project, each item labelled by status (proved in Lean, checked
          numerically, audit, open), is listed in{' '}
          <a href={`${REPO}/README.md`} style={link}>math/README.md on GitHub</a>. The Shared Air
          model, an interactive mother&ndash;infant breathing model with its own audit, is
          at <a href="/shared-air" style={link}>/shared-air</a>.
        </p>
      </section>

      {/* Navigation */}
      <section style={{
        display: 'flex', flexWrap: 'wrap', gap: 16, paddingBottom: 32,
      }}>
        {[
          { href: '/proof', label: 'The Argument', desc: '7 steps, each labelled: standard result, conjecture or analogy' },
          { href: '/demo', label: 'Interactive Demo', desc: 'A toy model of ventilator waveforms, sorted into clinical categories' },
          { href: '/shared-air', label: 'Shared Air', desc: 'The mother–infant breathing model' },
        ].map(l => (
          <a key={l.href} href={l.href} style={{
            flex: '1 1 220px', minWidth: 0, ...card, textDecoration: 'none',
            transition: 'border-color 0.2s',
            cursor: 'pointer',
          }}
          onMouseEnter={e => (e.currentTarget.style.borderColor = 'rgba(107,138,253,0.3)')}
          onMouseLeave={e => (e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)')}
          >
            <h3 style={{ color: '#6b8afd', fontSize: 16, marginBottom: 6, fontWeight: 600 }}>
              {l.label} →
            </h3>
            <p style={{ color: '#888899', fontSize: 14, margin: 0, lineHeight: 1.5 }}>
              {l.desc}
            </p>
          </a>
        ))}
      </section>
    </div>
  )
}
