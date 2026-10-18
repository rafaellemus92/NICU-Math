'use strict';
// Fast check (about 5 s): load the Model from the HTML, rerun Test 5b (expPulse) with the stored
// pulse strengths, and compare every field with the stored DEF.pulse. Prints the locking numbers.
// Usage: node tools/quick_check.js [html]
const crypto = require('crypto');
const path = require('path');
const { ROOT, loadModel, readDEF, readSource, resolveHtml, r3 } = require('./load.js');

const html = process.argv[2];
console.log('page', path.relative(ROOT, resolveHtml(html)).split(path.sep).join('/'));
console.log('sha256', crypto.createHash('sha256').update(readSource(html)).digest('hex'));
const M = loadModel(html), DEF = readDEF(html);
console.log('Model exports', Object.keys(M).length + ':', Object.keys(M).join(' '));

const t0 = Date.now();
const p = r3(M.runToEnd(M.expPulse(Object.assign({}, M.DEFAULTS), { eps: DEF.pulse.eps })));
console.log('expPulse', ((Date.now() - t0) / 1000).toFixed(1), 's');
let bad = 0;
for (const k of new Set([...Object.keys(p), ...Object.keys(DEF.pulse)])) {
  const same = JSON.stringify(p[k]) === JSON.stringify(DEF.pulse[k]);
  if (!same) { bad++; console.log('MISMATCH', k, JSON.stringify(p[k]), 'stored', JSON.stringify(DEF.pulse[k])); }
}
console.log(bad ? bad + ' DEF.pulse fields differ' : 'all ' + Object.keys(DEF.pulse).length + ' DEF.pulse fields match');
const bpm = x => (x * 60 / M.TAU).toFixed(2);
console.log('infant ' + p.hrI[0] + ' bpm, mom ' + p.hrM[0] + ' bpm; infant minus twice mom: ' + bpm(p.detuneSigned) + ' bpm (' + p.detuneSigned + ' rad/s)');
console.log('2:1 onset, first-order formula:', p.epsLock, '| exact single phase:', p.epsLockExact, '| range closes at:', p.epsLockOff);
console.log('infant 10 bpm above 2:1 locks from:', p.eps10Above, '| 10 bpm below:', p.eps10Below === null ? 'never (eps <= 40)' : p.eps10Below);
console.log('locking index at eps', p.eps[p.eps.length - 1] + ':', p.real[p.real.length - 1], '(other parent', p.room[p.room.length - 1] + ')');
process.exit(bad ? 1 : 0);
