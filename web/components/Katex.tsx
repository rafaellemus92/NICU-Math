'use client'
import katex from 'katex'

export function K({ children, display = false }: { children: string; display?: boolean }) {
  const html = katex.renderToString(children, {
    displayMode: display,
    throwOnError: false,
    trust: true,
  })
  return display
    ? <div className="katex-display" dangerouslySetInnerHTML={{ __html: html }} />
    : <span dangerouslySetInnerHTML={{ __html: html }} />
}

export function Eq({ children }: { children: string }) {
  return <K display>{children}</K>
}
