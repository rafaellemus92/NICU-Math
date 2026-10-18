'use strict';
// Test 4 protocol on fresh seeds, with the soothing cap on or off.
// Usage: node tools/adjudicate.js <tau> <capOff 0|1> <R> <seed0> [out.json] [html]
// Each run copies expSweep in shared_air.html: perceived world, heel stick at 80 s, 220 s session,
// no alarms, no room-mate, 16/8 cells; recoveryTime() with its default 10 bpm band and 15 s hold;
// a run counts as never recovered (censored) when rt >= 124 s.
// capOff=1 sets C.capA = Infinity, which makes cap(Am) = 1 exactly (no loss of soothing capacity).
// stuckHigh counts censored runs whose mom arousal, averaged over the last 80 s, is above 1.
const fs = require('fs');
const path = require('path');
const { loadModel } = require('./load.js');

const [tau, capOff, R, seed0] = [Number(process.argv[2]), process.argv[3] === '1', Number(process.argv[4]), Number(process.argv[5])];
const outFile = process.argv[6], html = process.argv[7];
if (![tau, R, seed0].every(Number.isFinite)) {
  console.error('usage: node tools/adjudicate.js <tau> <capOff 0|1> <R> <seed0> [out.json] [html]');
  process.exit(2);
}
const M = loadModel(html);
if (capOff) M.C.capA = Infinity;
const DUR = 220, TSTICK = 80, CENS = DUR - TSTICK - 16;

function runOne(K, seed) {
  const p = Object.assign({}, M.DEFAULTS, { K, tau, world: 'perceived', presence: 1, awake: true, vent: false, voice: false });
  const s = new M.Session(p, seed, { duration: DUR, heel: [TSTICK], alarms: false, roommate: false, cells: { nSA: 16, nR: 8 } }).run();
  let sum = 0, n = 0;
  for (let i = 0; i < s.rec.t.length; i++) if (s.rec.t[i] >= DUR - 80) { sum += s.rec.aM[i]; n++; }
  return { rt: M.recoveryTime(s, TSTICK), lateAm: sum / n };
}

const t0 = Date.now();
const out = {};
for (const K of [0, 0.5, 1, 1.5, 2, 2.5, 3]) {
  const runs = [];
  for (let i = 0; i < R; i++) runs.push(runOne(K, seed0 + i));
  const rts = runs.map(r => r.rt).sort((a, b) => a - b);
  const cens = runs.filter(r => r.rt >= CENS);
  const q = p => rts[Math.min(R - 1, Math.floor(p * R))];
  out[K] = { median: M.median(rts), q25: q(0.25), q75: q(0.75), censFrac: cens.length / R, stuckHigh: cens.filter(r => r.lateAm > 1).length };
}
const res = { tau, capOff, R, seed0, out };
const line = JSON.stringify(res);
console.log(line);
console.error('time ' + ((Date.now() - t0) / 1000).toFixed(1) + ' s');
if (outFile) fs.writeFileSync(path.resolve(process.cwd(), outFile), line + '\n');
