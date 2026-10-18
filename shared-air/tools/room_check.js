'use strict';
// The room-subtraction caveat. In the alike world there is no bond at all, so the Test 1 contrast
// peakSync(infant, mom) - peakSync(infant, other parent) should average zero. It does when mom and the
// other parent are treated alike (awake, in the room), and turns negative when mom is asleep (half the
// alarm kick, lower set point) or out of the room (misses alarms).
// Sessions: 300 s, default alarms, room-mate present, 16/8 cells, as in Test 1.
// Usage: node tools/room_check.js [N=60] [seed0=1000] [html]
const { loadModel } = require('./load.js');
const N = Number(process.argv[2] || 60), seed0 = Number(process.argv[3] || 1000);
const M = loadModel(process.argv[4]);
const conds = [
  ['mom awake, skin-to-skin (Test 1 protocol)', { presence: 1, awake: true }],
  ['mom asleep, skin-to-skin', { presence: 1, awake: false }],
  ['mom out of the room', { presence: 0, awake: true }],
];
for (const [label, c] of conds) {
  const t0 = Date.now(), diff = [];
  for (let i = 0; i < N; i++) {
    const s = new M.Session(Object.assign({}, M.DEFAULTS, c, { world: 'alike', vent: false, voice: false }), seed0 + i,
      { duration: 300, cells: { nSA: 16, nR: 8 } }).run();
    const I = M.series(s, 'hrI');
    diff.push(M.peakSync(I, M.series(s, 'hrM')) - M.peakSync(I, M.series(s, 'hrR')));
  }
  const m = M.mean(diff), se = M.sem(diff);
  console.log(label.padEnd(42), 'N', N, 'mean', m.toFixed(3), '+/-', se.toFixed(3), 'SEM', '(z', (m / se).toFixed(1) + ')', ((Date.now() - t0) / 1000).toFixed(1) + ' s');
}
