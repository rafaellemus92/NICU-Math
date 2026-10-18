'use strict';
// Recompute the stored Test 4 (DEF.sweep) and Test 5b (DEF.pulse) results from the page's own code.
// Default: check only (compare with what is stored, change nothing). --write: store the new values in the HTML.
// Usage: node tools/regen_def.js [html] [--R n] [--only sweep|pulse] [--write]
// The stored sweep uses R = 200 runs per point (about 3 minutes). A smaller --R runs faster but cannot match.
const fs = require('fs');
const { loadModel, readDEF, readSource, resolveHtml, DEF_RE, r3 } = require('./load.js');

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i < 0 ? def : args[i + 1]; };
const flagVals = new Set([opt('--R'), opt('--only')].filter(Boolean));
const html = args.find(a => !a.startsWith('--') && !flagVals.has(a));
const write = args.includes('--write'), only = opt('--only', null);
const M = loadModel(html), DEF = readDEF(html);
const R = Number(opt('--R', DEF.sweep.R));
const P = Object.assign({}, M.DEFAULTS);
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
let bad = 0;

if (only !== 'sweep') {
  const t0 = Date.now();
  const np = r3(M.runToEnd(M.expPulse(P, { eps: DEF.pulse.eps })));
  console.log('pulse', ((Date.now() - t0) / 1000).toFixed(1), 's');
  for (const k of new Set([...Object.keys(np), ...Object.keys(DEF.pulse)]))
    if (!same(np[k], DEF.pulse[k])) { bad++; console.log('PULSE MISMATCH', k, JSON.stringify(np[k]), 'stored', JSON.stringify(DEF.pulse[k])); }
  console.log(same(np, DEF.pulse) ? 'DEF.pulse reproduced exactly' : 'DEF.pulse differs');
  DEF.pulse = np;
}
if (only !== 'pulse') {
  const t0 = Date.now();
  const ns = r3(M.runToEnd(M.expSweep(P, { R })));
  console.log('sweep R =', R, ((Date.now() - t0) / 1000).toFixed(1), 's');
  for (const c of ns.curves) console.log('tau', c.tau, 'median', JSON.stringify(c.rec), 'never recover', JSON.stringify(c.censored));
  if (R === readDEF(html).sweep.R) {
    const ok = same(ns, readDEF(html).sweep);
    if (!ok) bad++;
    console.log(ok ? 'DEF.sweep reproduced exactly (every field, both curves)' : 'DEF.sweep differs');
  } else console.log('R differs from the stored R =', readDEF(html).sweep.R, '- no comparison made');
  DEF.sweep = ns;
}
if (write) {
  fs.writeFileSync(resolveHtml(html), readSource(html).replace(DEF_RE, '  const DEF = ' + JSON.stringify(DEF) + ';\n'));
  console.log('DEF written to', resolveHtml(html));
}
process.exit(bad ? 1 : 0);
