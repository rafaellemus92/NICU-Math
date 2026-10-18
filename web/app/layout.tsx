import type { Metadata } from 'next'
import './globals.css'
import 'katex/dist/katex.min.css'
import Nav from '@/components/Nav'

export const metadata: Metadata = {
  title: 'Respiratory Mechanics: Models and Conjectures',
  description: 'Synthetic respiratory teaching models and an incomplete fluid-dynamics conjecture with explicit gaps. Not validated for patient care.',
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
