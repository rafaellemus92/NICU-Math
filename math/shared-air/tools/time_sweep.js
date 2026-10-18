'use strict';
// How long Test 4 (expSweep) takes at a few run counts, and what it returns.
// Usage: node tools/time_sweep.js [R list, default 14,30,40] [html]
const { loadModel } = require('./load.js');
const Rs = (process.argv[2] || '14,30,40').split(',').map(Number);
const M = loadModel(process.argv[3]);
const r3 = a => a.map(x => Math.round(x * 1000) / 1000);
for (const R of Rs) {
  const t0 = Date.now();
  const res = M.runToEnd(M.expSweep(Object.assign({}, M.DEFAULTS), { R }));
  console.log('R', R, 'time', ((Date.now() - t0) / 1000).toFixed(1), 's');
  for (const c of res.curves) console.log('  tau', c.tau, 'median', JSON.stringify(r3(c.rec)), 'never recover', JSON.stringify(c.censored));
}
