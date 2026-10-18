import type { Metadata } from 'next'
import './globals.css'
import 'katex/dist/katex.min.css'
import Nav from '@/components/Nav'

export const metadata: Metadata = {
  title: 'Navier-Stokes and the Neonatal Lung',
  description: 'An analogy and a modelling programme: the language of Navier-Stokes regularity read against surfactant, surface tension and the Laplace law in the newborn lung. Not a regularity result; alveolar collapse is a clinical event, not a Navier-Stokes singularity.',
  // An inline icon, so browsers do not request a missing /favicon.ico.
  icons: {
    icon: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%230a0a0f'/%3E%3Ctext x='16' y='23' font-family='Georgia,serif' font-size='20' text-anchor='middle' fill='%23c9a96e'%3E;%3C/text%3E%3C/svg%3E",
  },
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
