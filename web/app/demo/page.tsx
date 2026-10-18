'use client'

import { useState, useMemo, useCallback } from 'react'
import {
  simulate,
  generatePVLoop,
  DEFAULT_PARAMS,
  CLASSIFICATION_COLORS,
  type SimulationParams,
  type BreathResult,
  type Classification,
} from '@/lib/ns'

const card = {
  background: 'rgba(255,255,255,0.03)',
  border: '1px solid rgba(255,255,255,0.06)',
  borderRadius: 12,
  padding: 24,
}

// Display names for the toy model's four waveform categories. The keys come from lib/ns.ts;
// they are clinical waveform categories, not distances from a PDE singularity.
const LABELS: Record<Classification, string> = {
  smooth: 'Normal',
  approaching: 'Stiffening',
  critical: 'Critical',
  singular: 'Collapse',
}

const LEGEND: { key: Classification; desc: string }[] = [
  { key: 'smooth', desc: 'C_dyn at or above 1.0 mL/cmH₂O: the lung inflates easily at the set pressure.' },
  { key: 'approaching', desc: 'C_dyn between 0.3 and 1.0 mL/cmH₂O and not falling fast: a stiffer lung, a smaller tidal volume at the same pressure.' },
  { key: 'critical', desc: 'C_dyn between 0.3 and 1.0 and falling by more than 0.1 mL/cmH₂O per breath, or below 0.3 but recovering: the point where a clinician would act.' },
  { key: 'singular', desc: 'C_dyn below 0.3 mL/cmH₂O and not recovering: the waveform pattern of widespread alveolar collapse (atelectasis). Pressures stay finite; nothing diverges.' },
]

export default function DemoPage() {
  const [decay, setDecay] = useState(DEFAULT_PARAMS.complianceDecay)
  const [nBreaths, setNBreaths] = useState(DEFAULT_PARAMS.nBreaths)
  const [giveSurfactant, setGiveSurfactant] = useState(false)
  const [surfBreath, setSurfBreath] = useState(60)
  const [selectedBreath, setSelectedBreath] = useState<number | null>(null)

  const params: SimulationParams = useMemo(() => ({
    ...DEFAULT_PARAMS,
    complianceDecay: decay,
    nBreaths,
    surfactantAtBreath: giveSurfactant ? surfBreath : null,
  }), [decay, nBreaths, giveSurfactant, surfBreath])

  const results = useMemo(() => simulate(params), [params])

  const activeIdx = selectedBreath !== null
    ? Math.min(selectedBreath, results.length - 1)
    : results.length - 1
  const activeBreath = results[activeIdx]

  const pvLoop = useMemo(() => {
    if (!activeBreath) return { p: [], v: [] }
    return generatePVLoop(
      activeBreath.compliance,
      params.resistance,
      params.pip,
      params.peep,
    )
  }, [activeBreath, params.resistance, params.pip, params.peep])

  // --- Analysis summary ---
  const summary = useMemo(() => {
    if (results.length === 0) return null
    const first10 = results.slice(0, Math.min(10, results.length))
    const last10 = results.slice(-Math.min(10, results.length))
    const meanFirst = first10.reduce((s, r) => s + r.compliance, 0) / first10.length
    const meanLast = last10.reduce((s, r) => s + r.compliance, 0) / last10.length

    const n = results.length
    const xm = (n - 1) / 2
    let num = 0, den = 0
    for (let i = 0; i < n; i++) {
      num += (i - xm) * results[i].compliance
      den += (i - xm) * (i - xm)
    }
    const slope = den > 0 ? num / den : 0

    const counts: Record<Classification, number> = { smooth: 0, approaching: 0, critical: 0, singular: 0 }
    results.forEach(r => counts[r.classification]++)

    return { meanFirst, meanLast, slope, counts, final: results[results.length - 1].classification }
  }, [results])

  return (
    <div>
      <h1 style={{ fontFamily: 'Georgia, serif', fontSize: 32, fontWeight: 600, color: '#e8e8ed', marginBottom: 8 }}>
        Interactive Demonstration
      </h1>
      <p style={{ color: '#888899', fontSize: 15, marginBottom: 32, lineHeight: 1.6, maxWidth: 640 }}>
        A toy model of ventilator waveforms. Compliance falls breath by breath, surfactant can be given,
        and each breath is sorted into one of four clinical waveform categories. The data are synthetic,
        from a simple resistance&ndash;compliance model: not patient data, and not a Navier-Stokes
        simulation. The categories say nothing about how close any PDE solution is to a singularity.
        Adjust parameters below. Click on the compliance chart to inspect any breath.
      </p>

      {/* Controls */}
      <div style={{ ...card, marginBottom: 24 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20 }}>
          <SliderControl
            label="Compliance decay rate"
            value={decay}
            min={0} max={0.02} step={0.001}
            format={v => v.toFixed(3)}
            onChange={setDecay}
          />
          <SliderControl
            label="Number of breaths"
            value={nBreaths}
            min={20} max={200} step={10}
            format={v => String(v)}
            onChange={setNBreaths}
          />
          <div>
            <label style={{ display: 'flex', alignItems: 'center', gap: 8, color: '#888899', fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 8 }}>
              <input
                type="checkbox"
                checked={giveSurfactant}
                onChange={e => setGiveSurfactant(e.target.checked)}
                style={{ accentColor: '#c9a96e' }}
              />
              Give surfactant at breath:
            </label>
            <input
              type="number"
              value={surfBreath}
              min={1}
              max={nBreaths - 1}
              disabled={!giveSurfactant}
              onChange={e => setSurfBreath(Number(e.target.value))}
              style={{
                width: 72, padding: '4px 8px', borderRadius: 6,
                background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                color: giveSurfactant ? '#e8e8ed' : '#555', fontSize: 14,
                outline: 'none',
              }}
            />
          </div>
        </div>
      </div>

      {/* Charts */}
      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', marginBottom: 24 }}>
        <div style={{ ...card, flex: '2 1 480px', minWidth: 0 }}>
          <div style={{ color: '#888899', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 12 }}>
            Compliance Trajectory
          </div>
          <ComplianceChart
            results={results}
            surfactantBreath={giveSurfactant ? surfBreath : null}
            selectedBreath={activeIdx}
            onSelectBreath={setSelectedBreath}
          />
        </div>
        <div style={{ ...card, flex: '1 1 280px', minWidth: 0 }}>
          <div style={{ color: '#888899', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 12 }}>
            P–V Loop · Breath {activeIdx}
          </div>
          <PVLoopChart
            pv={pvLoop}
            classification={activeBreath?.classification ?? 'smooth'}
            compliance={activeBreath?.compliance ?? 0}
          />
        </div>
      </div>

      {/* Analysis summary */}
      {summary && (
        <div style={{ ...card, marginBottom: 24 }}>
          <div style={{ color: '#888899', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 16 }}>
            Analysis Summary
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16 }}>
            <StatTile label="Final category" value={LABELS[summary.final]} color={CLASSIFICATION_COLORS[summary.final]} />
            <StatTile label="C̄ (first 10)" value={summary.meanFirst.toFixed(3)} unit="mL/cmH₂O" />
            <StatTile label="C̄ (last 10)" value={summary.meanLast.toFixed(3)} unit="mL/cmH₂O" />
            <StatTile label="Slope" value={summary.slope.toFixed(5)} unit="per breath" />
          </div>
          <div style={{ display: 'flex', gap: 16, marginTop: 16, flexWrap: 'wrap' }}>
            {(Object.keys(summary.counts) as Classification[]).map(k => (
              <span key={k} style={{ fontSize: 13, color: '#888899' }}>
                <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: 4, background: CLASSIFICATION_COLORS[k], marginRight: 6 }} />
                {LABELS[k]}: <span style={{ color: '#e8e8ed' }}>{summary.counts[k]}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Legend */}
      <div style={{ ...card }}>
        <div style={{ color: '#888899', fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 16 }}>
          Waveform Categories (toy model)
        </div>
        <div style={{ display: 'grid', gap: 12 }}>
          {LEGEND.map(l => (
            <div key={l.key} style={{ display: 'flex', alignItems: 'flex-start', gap: 10 }}>
              <span style={{
                display: 'inline-block', width: 10, height: 10, borderRadius: 5,
                background: CLASSIFICATION_COLORS[l.key], marginTop: 4, flexShrink: 0,
              }} />
              <div>
                <span style={{ color: '#e8e8ed', fontSize: 14, fontWeight: 500 }}>{LABELS[l.key]}</span>
                <span style={{ color: '#888899', fontSize: 13, marginLeft: 8 }}>{l.desc}</span>
              </div>
            </div>
          ))}
        </div>
        <p style={{ color: '#888899', fontSize: 13, lineHeight: 1.6, margin: '16px 0 0' }}>
          The thresholds are illustrative, not clinical cut-offs. In the toy model surfactant restores
          compliance within about 15 breaths; in real babies oxygen need often falls within minutes,
          and compliance improves more slowly.
        </p>
      </div>
    </div>
  )
}

// ---------- Sub-components ----------

function SliderControl({ label, value, min, max, step, format, onChange }: {
  label: string; value: number; min: number; max: number; step: number
  format: (v: number) => string; onChange: (v: number) => void
}) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ color: '#888899', fontSize: 13, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</span>
        <span style={{ color: '#6b8afd', fontSize: 14, fontFamily: 'monospace' }}>{format(value)}</span>
      </div>
      <input
        type="range" min={min} max={max} step={step} value={value}
        onChange={e => onChange(Number(e.target.value))}
        style={{ width: '100%', accentColor: '#6b8afd' }}
      />
    </div>
  )
}

function StatTile({ label, value, unit, color }: { label: string; value: string; unit?: string; color?: string }) {
  return (
    <div>
      <div style={{ color: '#888899', fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 20, fontWeight: 600, color: color ?? '#e8e8ed', fontFamily: 'monospace' }}>
        {value}
        {unit && <span style={{ fontSize: 12, color: '#888899', fontWeight: 400, marginLeft: 4 }}>{unit}</span>}
      </div>
    </div>
  )
}

// ---------- Charts ----------

const MARGIN = { top: 20, right: 20, bottom: 36, left: 52 }

function ComplianceChart({ results, surfactantBreath, selectedBreath, onSelectBreath }: {
  results: BreathResult[]
  surfactantBreath: number | null
  selectedBreath: number
  onSelectBreath: (i: number) => void
}) {
  const W = 560, H = 300
  const iw = W - MARGIN.left - MARGIN.right
  const ih = H - MARGIN.top - MARGIN.bottom

  const maxC = Math.max(1.2, ...results.map(r => r.compliance)) * 1.1
  const xScale = (i: number) => MARGIN.left + (i / Math.max(results.length - 1, 1)) * iw
  const yScale = (c: number) => MARGIN.top + ih - (c / maxC) * ih

  const handleClick = useCallback((e: React.MouseEvent<SVGSVGElement>) => {
    const svg = e.currentTarget
    const rect = svg.getBoundingClientRect()
    const x = (e.clientX - rect.left) / rect.width * W
    const idx = Math.round(((x - MARGIN.left) / iw) * (results.length - 1))
    if (idx >= 0 && idx < results.length) onSelectBreath(idx)
  }, [results.length, onSelectBreath])

  // Grid lines
  const yTicks = [0, 0.3, 0.5, 1.0, Math.round(maxC * 10) / 10].filter(v => v <= maxC)

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto', cursor: 'crosshair' }} onClick={handleClick}>
      {/* Grid */}
      {yTicks.map(v => (
        <g key={v}>
          <line x1={MARGIN.left} x2={W - MARGIN.right} y1={yScale(v)} y2={yScale(v)}
            stroke="rgba(255,255,255,0.06)" strokeWidth={1} />
          <text x={MARGIN.left - 6} y={yScale(v) + 4} fill="#888899" fontSize={10} textAnchor="end">{v}</text>
        </g>
      ))}

      {/* Threshold lines */}
      <line x1={MARGIN.left} x2={W - MARGIN.right} y1={yScale(0.3)} y2={yScale(0.3)}
        stroke="#ef4444" strokeWidth={1} strokeDasharray="4 4" opacity={0.4} />
      <line x1={MARGIN.left} x2={W - MARGIN.right} y1={yScale(1.0)} y2={yScale(1.0)}
        stroke="#4ade80" strokeWidth={1} strokeDasharray="4 4" opacity={0.4} />

      {/* Surfactant line */}
      {surfactantBreath !== null && surfactantBreath < results.length && (
        <>
          <line x1={xScale(surfactantBreath)} x2={xScale(surfactantBreath)}
            y1={MARGIN.top} y2={H - MARGIN.bottom}
            stroke="#c9a96e" strokeWidth={1} strokeDasharray="4 4" opacity={0.6} />
          <text x={xScale(surfactantBreath) + 4} y={MARGIN.top + 12} fill="#c9a96e" fontSize={9}>
            surfactant
          </text>
        </>
      )}

      {/* Compliance line segments colored by classification */}
      {results.map((r, i) => {
        if (i === 0) return null
        const prev = results[i - 1]
        return (
          <line key={i}
            x1={xScale(i - 1)} y1={yScale(prev.compliance)}
            x2={xScale(i)} y2={yScale(r.compliance)}
            stroke={CLASSIFICATION_COLORS[r.classification]}
            strokeWidth={1.5} opacity={0.85}
          />
        )
      })}

      {/* Selected breath marker */}
      {activeBreathMarker(selectedBreath, results, xScale, yScale)}

      {/* Axes */}
      <line x1={MARGIN.left} x2={MARGIN.left} y1={MARGIN.top} y2={H - MARGIN.bottom} stroke="rgba(255,255,255,0.12)" />
      <line x1={MARGIN.left} x2={W - MARGIN.right} y1={H - MARGIN.bottom} y2={H - MARGIN.bottom} stroke="rgba(255,255,255,0.12)" />
      <text x={W / 2} y={H - 4} fill="#888899" fontSize={11} textAnchor="middle">breath index</text>
      <text x={12} y={H / 2} fill="#888899" fontSize={11} textAnchor="middle" transform={`rotate(-90, 12, ${H / 2})`}>
        C_dyn (mL/cmH₂O)
      </text>
    </svg>
  )
}

function activeBreathMarker(
  idx: number,
  results: BreathResult[],
  xScale: (i: number) => number,
  yScale: (c: number) => number,
) {
  if (idx < 0 || idx >= results.length) return null
  const r = results[idx]
  return (
    <circle
      cx={xScale(idx)} cy={yScale(r.compliance)} r={4}
      fill={CLASSIFICATION_COLORS[r.classification]}
      stroke="#0a0a0f" strokeWidth={2}
    />
  )
}

function PVLoopChart({ pv, classification, compliance }: {
  pv: { p: number[]; v: number[] }
  classification: Classification
  compliance: number
}) {
  const W = 300, H = 300
  const M = { top: 20, right: 20, bottom: 36, left: 48 }
  const iw = W - M.left - M.right
  const ih = H - M.top - M.bottom

  if (pv.p.length === 0) {
    return <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto' }}>
      <text x={W / 2} y={H / 2} fill="#888899" fontSize={12} textAnchor="middle">No data</text>
    </svg>
  }

  const pMin = Math.min(...pv.p), pMax = Math.max(...pv.p)
  const vMin = Math.min(...pv.v), vMax = Math.max(...pv.v)
  const pRange = pMax - pMin || 1
  const vRange = vMax - vMin || 1

  const xScale = (v: number) => M.left + ((v - vMin) / vRange) * iw
  const yScale = (p: number) => M.top + ih - ((p - pMin) / pRange) * ih

  const points = pv.p.map((p, i) => `${xScale(pv.v[i])},${yScale(p)}`).join(' ')
  const color = CLASSIFICATION_COLORS[classification]

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto' }}>
      {/* Grid */}
      {[0, 0.25, 0.5, 0.75, 1].map(f => {
        const py = M.top + ih * (1 - f)
        const px = M.left + iw * f
        return <g key={f}>
          <line x1={M.left} x2={W - M.right} y1={py} y2={py} stroke="rgba(255,255,255,0.04)" />
          <line x1={px} x2={px} y1={M.top} y2={H - M.bottom} stroke="rgba(255,255,255,0.04)" />
        </g>
      })}

      {/* Loop */}
      <polyline points={points} fill="none" stroke={color} strokeWidth={1.5} opacity={0.8} />

      {/* Start marker */}
      {pv.p.length > 0 && (
        <circle cx={xScale(pv.v[0])} cy={yScale(pv.p[0])} r={3} fill={color} />
      )}

      {/* Compliance label */}
      <text x={W - M.right - 4} y={M.top + 14} fill={color} fontSize={12} textAnchor="end" fontFamily="monospace">
        C = {compliance.toFixed(3)}
      </text>

      {/* Axes */}
      <line x1={M.left} x2={M.left} y1={M.top} y2={H - M.bottom} stroke="rgba(255,255,255,0.12)" />
      <line x1={M.left} x2={W - M.right} y1={H - M.bottom} y2={H - M.bottom} stroke="rgba(255,255,255,0.12)" />
      <text x={W / 2} y={H - 4} fill="#888899" fontSize={10} textAnchor="middle">Volume (mL)</text>
      <text x={10} y={H / 2} fill="#888899" fontSize={10} textAnchor="middle" transform={`rotate(-90, 10, ${H / 2})`}>
        Pressure (cmH₂O)
      </text>
    </svg>
  )
}
