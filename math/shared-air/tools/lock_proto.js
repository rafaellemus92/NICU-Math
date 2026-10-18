'use strict';
// Exact 2:1 locking range for one forced phase: dth/dt = omega - eps * P(Omega t) * sin(th),
// with the page's pulse shape P(psi) = exp(2(cos psi - 1)) - mean. Same method as locked21/lockRange21
// in the page (web/public/shared-air/index.html), but with the resolution (n steps per drive cycle, G starting phases) as arguments.
// Standalone: needs no HTML. Usage: node tools/lock_proto.js
const TAU = Math.PI * 2;
const PMEAN = (() => { let s = 0; for (let i = 0; i < 720; i++) s += Math.exp(2 * (Math.cos(i / 720 * TAU) - 1)); return s / 720; })();
const pulseShape = psi => Math.exp(2 * (Math.cos(psi) - 1)) - PMEAN;
// second harmonic of P, as pulseHarmonic(2) on the page
const A2 = (() => { let s = 0; for (let i = 0; i < 720; i++) { const p = i / 720 * TAU; s += pulseShape(p) * Math.cos(2 * p); } return 2 * s / 720; })();

// Locked 2:1 when some starting phase advances exactly two turns per drive cycle (RK4 period map).
function locked21(omega, Omega, eps, n, G) {
  n = n || 256; G = G || 64;
  const h = TAU / Omega / n, P = new Float64Array(2 * n + 1);
  for (let k = 0; k <= 2 * n; k++) P[k] = pulseShape(Omega * k * h / 2);
  let lo = Infinity, hi = -Infinity;
  for (let g = 0; g < G; g++) {
    const th0 = g / G * TAU; let x = th0;
    for (let k = 0; k < n; k++) {
      const p0 = P[2 * k], p1 = P[2 * k + 1], p2 = P[2 * k + 2];
      const k1 = omega - eps * p0 * Math.sin(x);
      const k2 = omega - eps * p1 * Math.sin(x + h / 2 * k1);
      const k3 = omega - eps * p1 * Math.sin(x + h / 2 * k2);
      const k4 = omega - eps * p2 * Math.sin(x + h * k3);
      x += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4);
    }
    const d = x - th0 - 2 * TAU;
    if (d < lo) lo = d; if (d > hi) hi = d;
  }
  return lo <= 0 && hi >= 0;
}
// Scan eps upward in 0.25 steps; bisect the first entry into and exit from the locked range.
function lockRange21(omega, Omega, epsMax) {
  epsMax = epsMax || 40; const step = 0.25;
  const bis = (a, b, want) => { for (let i = 0; i < 30; i++) { const m = (a + b) / 2; if (locked21(omega, Omega, m) === want) b = m; else a = m; } return (a + b) / 2; };
  let on = locked21(omega, Omega, 0) ? 0 : null, off = null;
  for (let e = step; e <= epsMax + 1e-9; e += step) {
    const L = locked21(omega, Omega, e);
    if (L && on === null) on = bis(e - step, e, true);
    if (!L && on !== null) { off = bis(e - step, e, false); break; }
  }
  return { on, off };
}
module.exports = { locked21, lockRange21, A2 };

if (require.main === module) {
  // default rates from the stored Test 5b data: infant 149.59 bpm (omega 15.665 rad/s), mom 76.27 bpm
  const wI = 15.665, wM = TAU * 76.27 / 60, d10 = TAU * 10 / 60;
  const time = (label, f) => { const t0 = Date.now(); const r = f(); console.log(label, JSON.stringify(r), (Date.now() - t0) + ' ms'); };
  console.log('detune (rad/s)', (wI - 2 * wM).toFixed(4), ' a2', A2.toFixed(6), ' first-order onset', (Math.abs(wI - 2 * wM) / (A2 / 2)).toFixed(4));
  time('default rates        ', () => lockRange21(wI, wM, 40));
  time('infant +10 bpm of 2:1', () => lockRange21(2 * wM + d10, wM, 40));
  time('infant -10 bpm of 2:1', () => lockRange21(2 * wM - d10, wM, 40));
  time('detuning reversed    ', () => lockRange21(2 * wM + 0.309, wM, 40));
  console.log('first-order onset for 10 bpm off', (d10 / (A2 / 2)).toFixed(4));
  // resolution check on the default onset
  for (const [n, G] of [[128, 32], [256, 64], [512, 128]]) {
    let a = 3, b = 5; for (let i = 0; i < 40; i++) { const m = (a + b) / 2; if (locked21(wI, wM, m, n, G)) b = m; else a = m; }
    console.log('n', n, 'G', G, 'onset', ((a + b) / 2).toFixed(5));
  }
}
