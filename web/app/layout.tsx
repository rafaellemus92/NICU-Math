import type { Metadata } from 'next'
import './globals.css'
import 'katex/dist/katex.min.css'
import Nav from '@/components/Nav'

export const metadata: Metadata = {
  title: 'Navier-Stokes Regularity in the Neonatal Lung',
  description: 'Conditional regularity of NS solutions in bounded domains with surface-tension boundary conditions — evidence from neonatal respiratory mechanics.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main style={{ maxWidth: 900, margin: '0 auto', padding: '80px 24px 64px' }}>
          {children}
        </main>
      </body>
    </html>
  )
}
