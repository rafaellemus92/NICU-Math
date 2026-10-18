'use client'

// Status banner shared by every page of the site. The labels are the ones used
// across math/README.md ("Status labels"): Proved in Lean | Checked numerically |
// Audit | Open. In AGENTS.md's vocabulary these pages are hypotheses and
// synthetic teaching models, never proofs or clinical evidence.

const STATUS_LABELS_URL =
  'https://github.com/rafaellemus92/NICU-Math/blob/main/math/README.md'

type Kind = 'open' | 'synthetic'

const STYLE: Record<Kind, { color: string; badge: string; headline: string }> = {
  open: {
    color: '#ef4444',
    badge: 'Claim audit',
    headline: 'Standard identities, refuted deductions and open gaps.',
  },
  synthetic: {
    color: '#6b8afd',
    badge: 'Synthetic',
    headline: 'A teaching model, not evidence.',
  },
}

export default function StatusBanner({
  kind = 'open',
  children,
}: {
  kind?: Kind
  children?: React.ReactNode
}) {
  const s = STYLE[kind]
  return (
    <div
      role="note"
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'baseline',
        gap: '6px 12px',
        background: `${s.color}0f`,
        border: `1px solid ${s.color}59`,
        borderRadius: 10,
        padding: '12px 16px',
        margin: '0 0 32px',
        fontSize: 14,
        lineHeight: 1.6,
        color: '#c8c8d0',
      }}
    >
      <span
        style={{
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
        {s.badge}
      </span>
      <span>
        <strong style={{ color: '#e8e8ed' }}>{s.headline}</strong>{' '}
        {kind === 'open'
          ? 'The proposed regularity theorem is unproved. Counterexamples refute specific earlier deductions; these are not merely open claims.'
          : 'Synthetic data and prescribed schedules; no patient data and no clinical validation.'}
        {children ? <> {children}</> : null}{' '}
        <a href={STATUS_LABELS_URL} style={{ color: '#6b8afd', textDecoration: 'none' }}>
          Status labels used in this repository →
        </a>
      </span>
    </div>
  )
}
