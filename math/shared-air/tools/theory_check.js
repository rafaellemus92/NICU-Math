'use strict';
// Facts about the page's arousal equations with noise off, shared noise U = 0, voice off, mom awake,
// perceived world, presence 1 (so g = K). Constants are read from the Model in shared_air.html.
// Usage: node tools/theory_check.js [html]
const { loadModel } = require('./load.js');
const M = loadModel(process.argv[2]);
const C = M.C;
const Ti = M.KINDS.infant.T, Ta = M.KINDS.adult.T / M.DEFAULTS.selfReg, Tc = C.Tc;
const a = 1 / Ti, b = 1 / Ta, d = 1 / Tc;
const r = C.cMir, q = C.cCont, h = C.cCare / Tc, c = r * q; // per-unit-gain coefficients
const f = (x, n) => x.toFixed(n == null ? 6 : n);

// ---------- complex helpers ----------
const Z = (re, im) => ({ re, im });
const add = (x, y) => Z(x.re + y.re, x.im + y.im), sub = (x, y) => Z(x.re - y.re, x.im - y.im);
const mul = (x, y) => Z(x.re * y.re - x.im * y.im, x.re * y.im + x.im * y.re), sc = (x, s) => Z(x.re * s, x.im * s);
const div = (x, y) => { const m = y.re * y.re + y.im * y.im; return Z((x.re * y.re + x.im * y.im) / m, (x.im * y.re - x.re * y.im) / m); };
const cexp = x => Z(Math.exp(x.re) * Math.cos(x.im), Math.exp(x.re) * Math.sin(x.im));

// Linearization at rest: x' = -a x - z + r g y(t-tau), y' = -b y + q g x(t-tau), z' = -d z + h g x(t-tau)
// D(s) = (s+a)(s+b)(s+d) + h g (s+b) e^{-s tau} - c g^2 (s+d) e^{-2 s tau}
function D(s, g, tau) {
  const E = cexp(sc(s, -tau)), E2 = mul(E, E);
  const sa = add(s, Z(a, 0)), sb = add(s, Z(b, 0)), sd = add(s, Z(d, 0));
  return add(sub(mul(mul(sa, sb), sd), sc(mul(E2, sd), c * g * g)), sc(mul(E, sb), h * g));
}
// roots of s^3 + A2 s^2 + A1 s + A0 (real root by bisection, then the quadratic)
function cubicRoots(A2, A1, A0) {
  const p = s => ((s + A2) * s + A1) * s + A0;
  let lo = -1 - Math.abs(A2) - Math.abs(A1) - Math.abs(A0), hi = -lo;
  for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (p(m) > 0) hi = m; else lo = m; }
  const r1 = (lo + hi) / 2, B1 = A2 + r1, B0 = A1 + r1 * B1, disc = B1 * B1 - 4 * B0;
  return disc >= 0 ? [Z(r1, 0), Z((-B1 + Math.sqrt(disc)) / 2, 0), Z((-B1 - Math.sqrt(disc)) / 2, 0)]
    : [Z(r1, 0), Z(-B1 / 2, Math.sqrt(-disc) / 2), Z(-B1 / 2, -Math.sqrt(-disc) / 2)];
}
// rightmost root: exact cubic at tau = 0; Newton from a grid of starts for tau > 0
function rightmost(g, tau) {
  if (tau === 0) return cubicRoots(a + b + d, a * b + a * d + b * d + h * g - c * g * g, a * b * d + h * g * b - c * g * g * d).sort((x, y) => y.re - x.re)[0];
  let best = null;
  for (let re = -0.6; re <= 0.3; re += 0.05) for (let im = 0; im <= 4; im += 0.1) {
    let s = Z(re, im), ok = false;
    for (let it = 0; it < 80; it++) {
      const F = D(s, g, tau), e = 1e-7, dF = div(sub(D(add(s, Z(e, 0)), g, tau), F), Z(e, 0)), st = div(F, dF);
      s = sub(s, st);
      if (Math.hypot(st.re, st.im) < 1e-12) { ok = true; break; }
      if (!isFinite(s.re) || Math.abs(s.re) > 5) break;
    }
    if (ok && (!best || s.re > best.re)) best = Z(s.re, Math.abs(s.im));
  }
  return best;
}
const rho = (g, tau) => -rightmost(g, tau || 0).re; // slowest decay rate of the linearization
const golden = (fn, lo, hi) => { for (let i = 0; i < 80; i++) { const m1 = lo + (hi - lo) / 3, m2 = hi - (hi - lo) / 3; if (fn(m1) < fn(m2)) lo = m1; else hi = m2; } return (lo + hi) / 2; };

console.log('constants: a=1/' + Ti, 'b=1/' + Ta, 'd=1/' + Tc, 'r=' + r, 'q=' + q, 'h=' + h, 'c=' + f(c));
console.log('\n1. No delay (tau = 0): slowest decay rate rho(g)');
console.log('   rho at g = 0, 1, 3, 4:', [0, 1, 3, 4].map(g => f(rho(g))).join(', '));
// closed form: s* is the root in (-b, -a) of H(s) = (s+a)(s+d)^2 + h^2/(4c) (s+b); g* = (h/2c)(s*+b)/(s*+d)
const H = s => (s + a) * (s + d) * (s + d) + h * h / (4 * c) * (s + b);
let lo = -b, hi = -a; for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (H(m) < 0) lo = m; else hi = m; }
const sStar = (lo + hi) / 2, gStar = h / (2 * c) * (sStar + b) / (sStar + d);
const gNum = golden(g => rho(g), 0, 0.5);
console.log('   g* closed form', f(gStar, 10), ' rho(g*) = -s*', f(-sStar, 10), ' | numerical maximum at', f(gNum, 6), 'rho', f(rho(gNum), 10));
const gc = (h * b + Math.sqrt(h * h * b * b + 4 * c * a * b * d * d)) / (2 * c * d);
console.log('   g_c closed form', f(gc, 10), ' 15/8 + sqrt(2265)/24 =', f(15 / 8 + Math.sqrt(2265) / 24, 10), ' rho just below/above:', rho(gc - 1e-6).toExponential(2), rho(gc + 1e-6).toExponential(2));
let maxRho = 0; for (let g = 0.001; g < gc; g += 0.001) maxRho = Math.max(maxRho, rho(g));
console.log('   max rho over 0 < g < g_c:', f(maxRho), ' mom alone (b = 1/20):', f(b), ' ratio to rho(0):', f(maxRho / a, 4));
console.log('   rho(g) < rho(0) for g > h(b-a)/(c(d-a)) =', f(h * (b - a) / (c * (d - a)), 4), '; check rho(1.44), rho(1.45):', f(rho(1.44)), f(rho(1.45)));

console.log('\n2. With delay: rightmost root of D(s, g, tau)');
for (const tau of [1.5, 3]) {
  const gPk = golden(g => rho(g, tau), 0, 0.3);
  console.log('   tau', tau, ': slowest rate peaks at g =', f(gPk, 4), 'rate', f(rho(gPk, tau), 5), '; rho(1) =', f(rho(1, tau), 5));
  let l = 0.05, u = 5; for (let i = 0; i < 50; i++) { const m = (l + u) / 2; if (rightmost(m, tau).re > 0) u = m; else l = m; }
  const gs = (l + u) / 2, w = rightmost(gs + 1e-6, tau).im;
  console.log('   tau', tau, ': rest state first loses stability at g =', f(gs, 4), w > 1e-4 ? '(oscillatory: omega ' + f(w, 4) + ' rad/s, period ' + f(2 * Math.PI / w, 1) + ' s)' : '(real root through 0, the static limit g_c)');
}

// ---------- equilibria of the noise-free nonlinear model (do not depend on tau) ----------
const capOf = (Am, on) => { if (!on) return 1; const p = Math.max(Am, 0); return 1 / (1 + (p / C.capA) ** 2); };
function equilibria(g, capOn) {
  // dAm/dt = 0 gives Ai(Am); then dAi/dt = 0 is one equation in Am
  const AiOf = Am => (Am / Ta + C.k3 * Am ** 3) / (g * q);
  const F = Am => { const Ai = AiOf(Am); return -Ai / Ti - g * C.cCare * Ai * capOf(Am, capOn) + g * r * Am - C.k3 * Ai ** 3; };
  const out = [], step = 0.0005, x0 = -5.00013; let prev = F(x0); // offset grid, so rest (Am = 0) shows as a sign change
  for (let i = 1; x0 + i * step <= 8; i++) {
    const x = x0 + i * step, v = F(x);
    if (prev * v < 0) { let lo2 = x - step, hi2 = x; for (let k = 0; k < 60; k++) { const m = (lo2 + hi2) / 2; if (F(lo2) * F(m) <= 0) hi2 = m; else lo2 = m; } const Am = (lo2 + hi2) / 2; out.push({ Ai: AiOf(Am), Am }); }
    prev = v;
  }
  return out;
}
function stableNoDelay(g, e, capOn) {
  const cp = capOf(e.Am, capOn), dcap = capOn && e.Am > 0 ? -2 * e.Am / C.capA ** 2 * cp * cp : 0;
  const J = [[-1 / Ti - 3 * C.k3 * e.Ai ** 2, g * r, -1], [g * q, -1 / Ta - 3 * C.k3 * e.Am ** 2, 0], [g * C.cCare * cp / Tc, g * C.cCare * e.Ai * dcap / Tc, -1 / Tc]];
  const tr = J[0][0] + J[1][1] + J[2][2];
  const m2 = J[0][0] * J[1][1] - J[0][1] * J[1][0] + J[0][0] * J[2][2] - J[0][2] * J[2][0] + J[1][1] * J[2][2] - J[1][2] * J[2][1];
  const det = J[0][0] * (J[1][1] * J[2][2] - J[1][2] * J[2][1]) - J[0][1] * (J[1][0] * J[2][2] - J[1][2] * J[2][0]) + J[0][2] * (J[1][0] * J[2][1] - J[1][1] * J[2][0]);
  return Math.max(...cubicRoots(-tr, m2, -det).map(z => z.re)) < 0;
}
console.log('\n3. Equilibria of the noise-free model (rest is Ai = Am = 0)');
let gl = 1.5, gu = 3; for (let i = 0; i < 40; i++) { const m = (gl + gu) / 2; if (equilibria(m, true).length > 1) gu = m; else gl = m; }
console.log('   with the soothing cap: a second pair of equilibria appears at g =', f((gl + gu) / 2, 4), '(saddle-node)');
for (const g of [2.5, 3]) console.log('   g', g + ':', equilibria(g, true).map(e => '(Ai ' + f(Math.abs(e.Ai) < 1e-9 ? 0 : e.Ai, 3) + ', Am ' + f(Math.abs(e.Am) < 1e-9 ? 0 : e.Am, 3) + ', cap ' + f(capOf(e.Am, true), 3) + ', ' + (stableNoDelay(g, e, true) ? 'stable' : 'unstable') + ')').join(' '));
console.log('   with cap = 1: equilibria other than rest for g < g_c:', [1, 2, 3, 3.8].map(g => 'g ' + g + ': ' + (equilibria(g, false).length - 1)).join(', '));

// ---------- deterministic recovery, two observables ----------
// Euler, dt 0.02, delay line as in Session.prototype.step; kick at t = 0 from rest; last time the
// observable is outside its band within 600 s. Bands: infant arousal -0.3794..0.2232 (about 10 bpm of
// heart rate, from the page's HR map as worked out by an earlier verifier); pair norm |(Ai, Am)| < 0.2232.
function lastExit(g, tau, kickI, kickM, outside) {
  const dt = 0.02, lag = Math.max(1, Math.round(tau / dt)), N = lag + 2, bI = new Float64Array(N), bM = new Float64Array(N);
  let Ai = kickI, Am = kickM, Cf = 0, pos = 0, last = 0;
  bI[0] = 0; bM[0] = 0; // history at rest; the kick lands at t = 0
  for (let k = 1; k * dt <= 600; k++) {
    const j = (pos - lag + N) % N, AiD = bI[j], AmD = bM[j], cp = capOf(Am, true);
    const dAi = -Ai / Ti - Cf + g * r * AmD - C.k3 * Ai ** 3, dAm = -Am / Ta + g * q * AiD - C.k3 * Am ** 3;
    Ai += dAi * dt; Am += dAm * dt; Cf += (g * C.cCare * AiD * cp - Cf) / Tc * dt;
    pos = (pos + 1) % N; bI[pos] = Ai; bM[pos] = Am;
    if (outside(Ai, Am)) last = k * dt;
  }
  return last;
}
const argmin = (fn, gs) => gs.reduce((best, g) => { const v = fn(g); return v < best.v ? { g, v } : best; }, { g: null, v: Infinity });
const grid = Array.from({ length: 301 }, (_, i) => i / 100);
console.log('\n4. Deterministic recovery (last exit from the band), g = 0 .. 3 in steps of 0.01');
const heelOut = x => x > 0.2232 || x < -0.3794, pairOut = eps => (x, y) => Math.hypot(x, y) > eps;
for (const tau of [0.02, 1.5]) {
  const heel = argmin(g => lastExit(g, tau, 1, 0, heelOut), grid);
  console.log('   tau', tau, ': heel stick, infant band: fastest at g =', heel.g, '(' + f(heel.v, 2) + ' s);', 'times at g = 0, 1, 2, 3:',
    [0, 1, 2, 3].map(g => f(lastExit(g, tau, 1, 0, heelOut), 2)).join(', '));
  for (const eps of [0.2232, 0.1, 0.03]) {
    const al = argmin(g => lastExit(g, tau, C.kickAlarmInfant, C.kickAlarmAdult, pairOut(eps)), grid);
    console.log('   tau', tau, ': alarm, pair norm below', eps + ': fastest at g =', al.g, '(' + f(al.v, 2) + ' s);', 'times at g = 0, 0.08, 0.5, 1, 2:',
      [0, 0.08, 0.5, 1, 2].map(g => f(lastExit(g, tau, C.kickAlarmInfant, C.kickAlarmAdult, pairOut(eps)), 2)).join(', '));
  }
}
