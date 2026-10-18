'use strict';
// How a run enters Test 4's stuck state, with all arousal noise off. Uses the page's own Session with the
// infant, adult and shared-room noise set to 0, so the arousal equations are deterministic (the cells keep
// their noise, but nothing in the arousal equations reads the cells). Test 4 setting otherwise: perceived
// world, presence 1, mom awake, voice off, no alarms, no room-mate, kick to the infant only at 80 s.
// "Stuck" = mom's mean arousal over the last 80 s of a 220-s session is above 1 (stuckHigh in adjudicate.js);
// "stuck, long run" = mom's arousal still above 1 at 1080 s.
// Usage: node tools/kick_check.js [html]
const { loadModel } = require('./load.js');
const M = loadModel(process.argv[2]);
M.KINDS.infant.sig = 0; M.KINDS.adult.sig = 0; M.C.sigU = 0;
const kick0 = M.C.kickHeel, TSTICK = 80;

function stuck(g, tau, kick, long) {
  M.C.kickHeel = kick;
  const dur = long ? 1080 : 220;
  const p = Object.assign({}, M.DEFAULTS, { K: g, tau, world: 'perceived', presence: 1, awake: true, vent: false, voice: false });
  const s = new M.Session(p, 1, { duration: dur, heel: [TSTICK], alarms: false, roommate: false, cells: { nSA: 1, nR: 1 } }).run();
  M.C.kickHeel = kick0;
  if (long) return s.mom.A > 1;
  let sum = 0, n = 0;
  for (let i = 0; i < s.rec.t.length; i++) if (s.rec.t[i] >= dur - 80) { sum += s.rec.aM[i]; n++; }
  return sum / n > 1;
}
// smallest infant kick that leaves the pair stuck (bisection; null if even kick 12 does not)
function minKick(g, tau, long) {
  let lo = 0, hi = 12;
  if (!stuck(g, tau, hi, long)) return null;
  for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (stuck(g, tau, m, long)) hi = m; else lo = m; }
  return hi;
}

const t0 = Date.now();
const gs = Array.from({ length: 13 }, (_, i) => i / 4);
for (const tau of [0.02, 1.5]) {
  const hit = gs.filter(g => stuck(g, tau, kick0, false) || stuck(g, tau, kick0, true));
  console.log('tau', tau, ': heel stick ' + kick0 + ', g = 0, 0.25, ..., 3: stuck at', hit.length ? hit.join(', ') : 'none');
}
for (const g of [2.5, 3]) for (const tau of [0.02, 1.5]) {
  const a = minKick(g, tau, false), b = minKick(g, tau, true);
  console.log('g', g, 'tau', tau, ': smallest infant kick that sticks:', a === null ? 'none up to 12' : a.toFixed(3),
    '(in the Test 4 window),', b === null ? 'none up to 12' : b.toFixed(3), '(long run)');
}
console.log('time', ((Date.now() - t0) / 1000).toFixed(1) + ' s');
