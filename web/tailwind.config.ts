import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0a0a0f',
        surface: 'rgba(255,255,255,0.03)',
        border: 'rgba(255,255,255,0.06)',
        gold: '#c9a96e',
        blue: '#6b8afd',
        muted: '#888899',
      },
      fontFamily: {
        serif: ['Georgia', 'Times New Roman', 'serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
    },
  },
  plugins: [],
}
export default config
