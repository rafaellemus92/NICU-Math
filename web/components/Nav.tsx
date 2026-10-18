'use client'

const links = [
  { href: '/', label: 'Conjecture' },
  { href: '/proof', label: 'Proof' },
  { href: '/demo', label: 'Demo' },
]

export default function Nav() {
  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 50,
      background: 'rgba(10,10,15,0.85)', backdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(255,255,255,0.06)',
    }}>
      <div style={{
        maxWidth: 900, margin: '0 auto', padding: '12px 24px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <a href="/" style={{
          color: '#c9a96e', textDecoration: 'none', fontFamily: 'Georgia, serif',
          fontSize: 18, fontWeight: 600, letterSpacing: '-0.02em',
        }}>
          NS ; Regularity
        </a>
        <div style={{ display: 'flex', gap: 24 }}>
          {links.map(l => (
            <a key={l.href} href={l.href} style={{
              color: '#888899', textDecoration: 'none', fontSize: 14,
              letterSpacing: '0.04em', textTransform: 'uppercase',
              transition: 'color 0.2s',
            }}
            onMouseEnter={e => (e.currentTarget.style.color = '#e8e8ed')}
            onMouseLeave={e => (e.currentTarget.style.color = '#888899')}
            >{l.label}</a>
          ))}
        </div>
      </div>
    </nav>
  )
}
