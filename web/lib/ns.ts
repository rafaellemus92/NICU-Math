// Core Navier-Stokes calculations for client-side demo
// Simplified TypeScript port of navier_stokes/formulation.py + analysis.py

export const CONST = {
  rho_air: 1.2,
  nu_air: 1.5e-5,
  gamma_surfactant: 0.025,
  gamma_no_surfactant: 0.070,
  alveolar_radius_preterm: 30e-6,
  airway_diameter_trachea: 3.5e-3,
  respiratory_rate: 40.0,
} as const

export type Classification = 'smooth' | 'approaching' | 'critical' | 'singular'

export interface BreathResult {
  index: number
  compliance: number
  resistance: number
  timeConstant: number
  pvArea: number
  peakPressure: number
  tidalVolume: number
  classification: Classification
}

export interface SimulationParams {
  nBreaths: number
  compliance0: number      // initial compliance (mL/cmH2O)
  complianceDecay: number  // per-breath fractional decay
  resistance: number       // cmH2O/(L/s)
  peep: number            // cmH2O
  pip: number             // cmH2O
  noiseLevel: number
  surfactantAtBreath: number | null  // null = no surfactant
  surfactantEffect: number           // fractional compliance recovery
}

export const DEFAULT_PARAMS: SimulationParams = {
  nBreaths: 100,
  compliance0: 1.0,
  complianceDecay: 0.008,
  resistance: 80.0,
  peep: 5.0,
  pip: 20.0,
  noiseLevel: 0.03,
  surfactantAtBreath: null,
  surfactantEffect: 0.6,
}

export function classifyRegularity(
  compliance: number,
  trend: number,
  cLow = 0.3,
  cHigh = 1.0,
): Classification {
  if (compliance < cLow) return trend <= 0 ? 'singular' : 'critical'
  if (compliance < cHigh) return trend < -0.1 ? 'critical' : 'approaching'
  return 'smooth'
}

export function laplacePressure(gamma: number, radius: number): number {
  if (radius <= 0) return Infinity
  return 2.0 * gamma / radius
}

function mulberry32(seed: number) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed)
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t
    return ((t ^ t >>> 14) >>> 0) / 4294967296
  }
}

function gaussianRandom(rng: () => number): number {
  let u = 0, v = 0
  while (u === 0) u = rng()
  while (v === 0) v = rng()
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v)
}

export function simulate(params: SimulationParams): BreathResult[] {
  const rng = mulberry32(42)
  const results: BreathResult[] = []
  const dP = params.pip - params.peep

  for (let b = 0; b < params.nBreaths; b++) {
    let cEff = params.compliance0 * (1.0 - params.complianceDecay * b)
    cEff = Math.max(cEff, 0.05)

    // Surfactant rescue
    if (params.surfactantAtBreath !== null && b >= params.surfactantAtBreath) {
      const recovery = params.compliance0 * params.surfactantEffect
      const breathsSince = b - params.surfactantAtBreath
      const rampup = 1 - Math.exp(-breathsSince / 5)
      cEff = cEff + recovery * rampup
    }

    // Add noise
    const noise = gaussianRandom(rng) * params.noiseLevel * cEff
    cEff = Math.max(cEff + noise, 0.02)

    const tau = params.resistance * cEff * 1e-3
    const tidalVolume = cEff * dP
    const qPeak = dP / (params.resistance * 1e-3)

    // PV loop area estimate (hysteresis from RC model)
    const pvArea = tidalVolume * dP * (1 - Math.exp(-1 / (tau * 2 + 0.01)))

    // Trend from recent history
    let trend = 0
    if (results.length >= 3) {
      const recent = results.slice(-5)
      const n = recent.length
      const xm = (n - 1) / 2
      let num = 0, den = 0
      for (let i = 0; i < n; i++) {
        num += (i - xm) * recent[i].compliance
        den += (i - xm) * (i - xm)
      }
      trend = den > 0 ? num / den : 0
    }

    results.push({
      index: b,
      compliance: cEff,
      resistance: dP / qPeak,
      timeConstant: tau,
      pvArea,
      peakPressure: params.pip + gaussianRandom(rng) * params.noiseLevel * dP,
      tidalVolume,
      classification: classifyRegularity(cEff, trend),
    })
  }

  return results
}

// Generate a single P-V loop for visualization
export function generatePVLoop(
  compliance: number,
  resistance: number,
  pip: number,
  peep: number,
  sampleRate = 100,
  breathPeriod = 1.5,
): { p: number[]; v: number[] } {
  const n = Math.floor(sampleRate * breathPeriod)
  const tiRatio = 0.35
  const dt = breathPeriod / n
  const tau = resistance * compliance * 1e-3
  const dP = pip - peep

  const p: number[] = []
  const v: number[] = []
  let vol = 0

  for (let i = 0; i < n; i++) {
    const t = i * dt
    const inInsp = t < breathPeriod * tiRatio

    // Pressure
    let pVal: number
    if (inInsp) {
      const rise = Math.min(1, t / 0.05)
      pVal = peep + dP * rise
    } else {
      pVal = peep
    }

    // Flow from RC model
    let flow: number
    if (inInsp) {
      flow = (dP / (resistance * 1e-3)) * Math.exp(-t / Math.max(tau, 0.01))
    } else {
      const tExp = t - breathPeriod * tiRatio
      flow = -(dP / (resistance * 1e-3)) * Math.exp(-tExp / Math.max(tau, 0.01))
    }

    vol += flow * dt * 1e-3 // rough mL
    p.push(pVal)
    v.push(vol)
  }

  // Normalize volume to start at 0
  const vMin = Math.min(...v)
  return { p, v: v.map(x => x - vMin) }
}

export const CLASSIFICATION_COLORS: Record<Classification, string> = {
  smooth: '#4ade80',
  approaching: '#facc15',
  critical: '#f97316',
  singular: '#ef4444',
}
