import test from 'node:test'
import assert from 'node:assert/strict'
import { classifyCompliance, simulate, DEFAULT_PARAMS, laplacePressure, generatePVLoop } from '../lib/ns.ts'

test('descriptors and missing-data labels imply no regularity class', () => {
  assert.equal(classifyCompliance(NaN, 0), 'insufficient_data')
  assert.equal(classifyCompliance(Infinity, 0), 'insufficient_data')
  assert.equal(classifyCompliance(-1, 0), 'insufficient_data')
  assert.equal(classifyCompliance(0, 0), 'low_compliance')
  assert.equal(classifyCompliance(.3, 0), 'intermediate_compliance')
  assert.equal(classifyCompliance(.5, -.2), 'declining_compliance')
  assert.equal(classifyCompliance(1, 0), 'higher_compliance')
  assert.deepEqual(simulate({...DEFAULT_PARAMS, nBreaths: 0}), [])
})
test('prescribed floors, RC units, reproducibility and recovery', () => {
  const params = {...DEFAULT_PARAMS, nBreaths: 100, complianceDecay: .1, noiseLevel: 0}
  const result = simulate(params)
  assert.deepEqual(simulate(params), result)
  assert.equal(result.at(-1).compliance, .05)
  assert.equal(result[0].timeConstant, .08)
  assert.equal(result[0].tidalVolume, 15)
  assert.equal(result[0].resistance, .08) // cmH2O/(mL/s)
  assert.ok(simulate({...params, recoveryAtBreath: 50}).at(-1).compliance > .05)
  assert.throws(() => simulate({...params, resistance: 0}), RangeError)
})
test('positive gamma retains inverse-radius scaling', () => {
  assert.equal(laplacePressure(.025, .01), 5)
  assert.equal(laplacePressure(.025, .001), 50)
  assert.throws(() => laplacePressure(.025, 0), RangeError)
})
test('schematic flow integration reports mL without an extra litre conversion', () => {
  const {v} = generatePVLoop(1, 80, 20, 5, 1000)
  assert.ok(Math.max(...v) > 14 && Math.max(...v) < 16)
})
