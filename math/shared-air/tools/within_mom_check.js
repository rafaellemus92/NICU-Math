'use strict';
// Same mother across conditions, in the alike world (no bond at all). The v2 model text (Test 1 bedside)
// says comparing the same mother awake and asleep, holding and not, avoids the matched-control problem.
// Here the infant's and the other parent's series are the same in every condition (same seed; the alike
// world has g = 0), so any change in infant-mom synchrony between conditions is not a bond.
// Sessions: 300 s, default alarms, other parent present, 16/8 cells, as in Test 1 and tools/room_check.js.
// Usage: node tools/within_mom_check.js [N=60] [seed0=1000] [html]
const { loadModel } = require('./load.js');
const N = Number(process.argv[2] || 60), seed0 = Number(process.argv[3] || 1000);
const M = loadModel(process.argv[4]);
const conds = [
  ['skin', 'mom awake, skin-to-skin', { presence: 1, awake: true }],
  ['asleep', 'mom asleep, skin-to-skin', { presence: 1, awake: false }],
  ['bedside', 'mom awake, at the bedside', { presence: 0.35, awake: true }],
];
const t0 = Date.now(), res = {};
for (const [key, label, c] of conds) {
  const im = [], ir = [];
  for (let i = 0; i < N; i++) {
    const s = new M.Session(Object.assign({}, M.DEFAULTS, c, { world: 'alike', vent: false, voice: false }), seed0 + i,
      { duration: 300, cells: { nSA: 16, nR: 8 } }).run();
    const I = M.series(s, 'hrI');
    im.push(M.peakSync(I, M.series(s, 'hrM'))); ir.push(M.peakSync(I, M.series(s, 'hrR')));
  }
  res[key] = { im, ir };
  console.log(label.padEnd(27), 'N', N, ' infant-mom', M.mean(im).toFixed(3), '+/-', M.sem(im).toFixed(3),
    ' infant-other parent', M.mean(ir).toFixed(3), '+/-', M.sem(ir).toFixed(3));
}
const paired = (label, a, b) => {
  const d = a.map((x, i) => x - b[i]), m = M.mean(d), se = M.sem(d);
  console.log(label.padEnd(46), m >= 0 ? '+' + m.toFixed(3) : m.toFixed(3), '+/-', se.toFixed(3), 'SEM', se > 0 ? '(z ' + (m / se).toFixed(1) + ')' : '(all differences 0)');
};
console.log('paired differences in infant-mom synchrony, same seeds, no bond:');
paired('  awake minus asleep (skin-to-skin)', res.skin.im, res.asleep.im);
paired('  holding minus not (skin-to-skin vs bedside)', res.skin.im, res.bedside.im);
let maxR = 0;
for (const k of ['asleep', 'bedside']) res[k].ir.forEach((x, i) => { maxR = Math.max(maxR, Math.abs(x - res.skin.ir[i])); });
console.log('largest change in infant-other parent synchrony across conditions:', maxR);
console.log('time', ((Date.now() - t0) / 1000).toFixed(1) + ' s');
