// Independent implementation (Node): prime-valued perfect pangrams under fixed
// numeration (A=1..Z=26, bijective base-26) and stated phonotactics.
// (a) reproduce the English-cluster impossibility, (b) relaxation lattice,
// (c) first-moment estimates, (d) count solutions under free CC·V·CC.
"use strict";
const ALPHA = "abcdefghijklmnopqrstuvwxyz";
const VOW = new Set("aeiouy");
const CONS = [...ALPHA].filter(c => !VOW.has(c));
const ONSETS = new Set(("b c d f g h j k l m n p q r s t v w x z bl br ch cl cr dr dw fl fr gl gr gw kl kn kr kw ph pl pr qu sc sch scr sh shr sk sl sm sn sp sph spl spr st str sw th thr tr tw wh wr zh").split(" ").concat([""]));
const CODAS = new Set(("b c d f g h k l m n p q r s t v w x z ch ck ct ft ld lf lk lm lp lt mp nd ng nk ns nt nx ph pt rb rd rf rk rl rm rn rp rs rt sh sk sm sp st th ts xt sm lsh mph nch ngs nks nth rch rld rst rth ght lch ltz tz ltz nz rz").split(" ").concat([""]));

// ---- numeration and primality (sieve + trial division; values < 26^8 = 2.09e11 < 2^53) ----
function value(w) { let v = 0; for (const c of w) v = v * 26 + (c.charCodeAt(0) - 96); return v; }
const LIM = Math.ceil(Math.sqrt(Math.pow(26, 8))) + 1;
const sieve = new Uint8Array(LIM + 1); const PRIMES = [];
for (let i = 2; i <= LIM; i++) { if (!sieve[i]) { PRIMES.push(i); for (let j = i * i; j <= LIM; j += i) sieve[j] = 1; } }
function isPrime(n) { if (n < 2) return false; for (const p of PRIMES) { if (p * p > n) return true; if (n % p === 0) return n === p; } return true; }
const GOOD_LAST = new Set("acegikoqsuwy");   // positions coprime to 26: a value can be prime only if it ends here

// ---- word shape rule, exactly as stated: onset + nucleus(1-2 vowels) + coda, distinct letters,
//      vowel runs ≤ 2, consonant runs ≤ 3, leading run ∈ onsets, trailing run ∈ codas ----
function runs(w) { const r = []; let i = 0; while (i < w.length) { let j = i; while (j < w.length && VOW.has(w[j]) === VOW.has(w[i])) j++; r.push(w.slice(i, j)); i = j; } return r; }
function pronounceable(w, onsets, codas) {
  const r = runs(w); if (!r.some(x => VOW.has(x[0]))) return false;
  for (const x of r) { if (VOW.has(x[0]) && x.length > 2) return false; if (!VOW.has(x[0]) && x.length > 3) return false; }
  const on = VOW.has(r[0][0]) ? "" : r[0], co = VOW.has(r[r.length - 1][0]) ? "" : r[r.length - 1];
  return onsets.has(on) && codas.has(co);
}
function distinct(w) { return new Set(w).size === w.length; }
function freeClusters(maxLen) { const out = [""]; for (const a of CONS) { out.push(a); if (maxLen >= 2) for (const b of CONS) if (b !== a) out.push(a + b); } return new Set(out); }
function nucleiList(maxV) { const out = [...VOW]; if (maxV >= 2) for (const a of VOW) for (const b of VOW) if (a !== b) out.push(a + b); return out; }
function buildDict(onsets, codas, maxV, primeOnly) {
  const words = new Set();
  for (const on of onsets) for (const nu of nucleiList(maxV)) for (const co of codas) {
    const w = on + nu + co; if (!distinct(w)) continue; if (!pronounceable(w, onsets, codas)) continue;
    if (primeOnly && !isPrime(value(w))) continue; words.add(w);
  }
  return [...words];
}

// ---- exact cover with memoized subset DP (count + weighted sum); branching letter chosen by a static rarity order ----
function mask(w) { let m = 0; for (const c of w) m |= 1 << (c.charCodeAt(0) - 97); return m; }
const FULL = (1 << 26) - 1;
function cover(words, weight, opts) {
  opts = opts || {}; const items = words.map(w => ({ w, m: mask(w), p: weight ? weight(w) : 1 }));
  const byL = Array.from({ length: 26 }, () => []); for (const it of items) for (let i = 0; i < 26; i++) if (it.m >> i & 1) byL[i].push(it);
  const order = [...Array(26).keys()].sort((a, b) => byL[a].length - byL[b].length);
  const memo = new Map(); let nodes = 0, first = null, capped = false;
  function rec(cov, chosen) {
    if (cov === FULL) { if (!first) first = chosen.slice(); return [1, 1]; }
    if (memo.has(cov)) return memo.get(cov);
    nodes++; if (opts.nodeCap && nodes > opts.nodeCap) { capped = true; return [0, 0]; }
    let L = -1; for (const i of order) if (!(cov >> i & 1)) { L = i; break; }
    let n = 0, e = 0;
    for (const it of byL[L]) { if (it.m & cov) continue; chosen.push(it.w); const [cn, ce] = rec(cov | it.m, chosen); chosen.pop(); n += cn; e += it.p * ce; if (opts.firstOnly && first) break; }
    if (memo.size < (opts.memoCap || 30e6)) memo.set(cov, [n, e]);
    return [n, e];
  }
  const t0 = Date.now(); const [n, e] = rec(0, []);
  return { count: n, weighted: e, first, nodes, states: memo.size, capped, ms: Date.now() - t0 };
}
const fmt = n => n >= 1e15 ? n.toExponential(3) : Math.round(n).toLocaleString("en-US");

// ======================= (a) reproduce result (1) =======================
console.log("== (a) English clusters, nucleus 1-2 vowels, prime-valued words ==");
let dictEE = buildDict(ONSETS, CODAS, 2, true);
console.log(`dictionary: ${dictEE.length.toLocaleString()} prime words (Python implementation reported 4,644)`);
let r = cover(dictEE, null, { firstOnly: true });
console.log(`exact cover: ${r.first ? "SOLUTION " + r.first.join(" ") : "no perfect pangram"}  (${r.nodes.toLocaleString()} nodes, ${r.states.toLocaleString()} states, ${r.ms} ms, exhaustive)`);

// ======================= (b) relaxation lattice =======================
console.log("\n== (b) minimal relaxation: onset rule × coda rule (nucleus 1-2 vowels) ==");
const F2 = freeClusters(2), F1 = freeClusters(1);
const regimes = [["English", ONSETS, "English", CODAS], ["English", ONSETS, "free ≤1", F1], ["free ≤1", F1, "English", CODAS], ["English", ONSETS, "free ≤2", F2], ["free ≤2", F2, "English", CODAS], ["free ≤2", F2, "free ≤2", F2]];
const found = {};
for (const [on, O, cn, C] of regimes) {
  const d = buildDict(O, C, 2, true); const rr = cover(d, null, { firstOnly: true });
  found[on + "/" + cn] = rr;
  console.log(`onset ${on.padEnd(8)} coda ${cn.padEnd(8)}: ${d.length.toLocaleString().padStart(7)} prime words -> ${rr.first ? "SOLUTION: " + rr.first.map(w => w.toUpperCase()).join(" ") + "   " + rr.first.map(w => value(w).toLocaleString()).join(" / ") : "none"}  (${rr.ms} ms)`);
}

// ======================= (c) first-moment estimates =======================
console.log("\n== (c) first-moment estimate: N0 = pronounceable perfect pangrams ignoring primality; E = Σ Π p(word) ==");
// p(w): a value is prime only if its last letter is coprime to 26 (12 of 26 letters); among such numbers the prime density is (26/φ(26))/ln N = (13/6)/ln N.
const pw = w => GOOD_LAST.has(w[w.length - 1]) ? (13 / 6) / Math.log(value(w)) : 0;
const allEE = buildDict(ONSETS, CODAS, 2, false);
console.log(`English/English: ${allEE.length.toLocaleString()} pronounceable words (no prime filter); ${dictEE.length.toLocaleString()} of them prime = ${(100 * dictEE.length / allEE.length).toFixed(2)}%; model predicts ${(100 * allEE.reduce((s, w) => s + pw(w), 0) / allEE.length).toFixed(2)}%`);
let c = cover(allEE, pw, { nodeCap: 4e8 });
console.log(`  N0 = ${fmt(c.count)} pangrams${c.capped ? " (node cap hit — lower bound)" : ""}; expected prime pangrams E = ${c.weighted.toExponential(3)}; observed 0.   (${c.states.toLocaleString()} states, ${c.ms} ms)`);
// free CC·V·CC with a single vowel, analytically: words = (onset ≤2)(vowel)(coda ≤2); the 6 vowels label the 6 words;
// N0 = 20! × [x^20](1+x+x^2)^12 (12 ordered slots of size 0..2 holding the 20 consonants in order)
function poly() { let p = [1]; for (let k = 0; k < 12; k++) { const q = new Array(p.length + 2).fill(0); for (let i = 0; i < p.length; i++) { q[i] += p[i]; q[i + 1] += p[i]; q[i + 2] += p[i]; } p = q; } return p; }
const coef = poly()[20]; let f20 = 1; for (let i = 2; i <= 20; i++) f20 *= i;
const N0free = coef * f20;
// E_free: sum over size profiles (a_i, b_i); word i has length a_i+b_i+1; if b_i>0 its last letter must be one of the 6 prime-compatible consonants c g k q s w
// (injective choice P(6,k) for the k words with a coda), the rest arranged freely: (20-k)!; p_i ≈ (13/6)/ln(value) with ln(value) ≈ (len-0.5)·ln 26
let Efree = 0; const sizes = [0, 1, 2];
function profiles(i, rem, acc) {
  if (i === 6) { if (rem !== 0) return; let k = 0, prod = 1; for (const [a, b] of acc) { const len = a + b + 1; prod *= (13 / 6) / ((len - 0.5) * Math.log(26)); if (b > 0) k++; }
    let ways = 1; for (let j = 0; j < k; j++) ways *= (6 - j); let fact = 1; for (let j = 2; j <= 20 - k; j++) fact *= j; Efree += prod * ways * fact; return; }
  for (const a of sizes) for (const b of sizes) if (a + b <= rem) profiles(i + 1, rem - a - b, acc.concat([[a, b]]));
}
profiles(0, 20, []);
console.log(`free ≤2 / free ≤2, single vowel: N0 = 20!·[x^20](1+x+x²)^12 = ${fmt(N0free)} pangrams; expected prime pangrams E ≈ ${Efree.toExponential(3)} (analytic)`);

// ======================= (d) count solutions under free CC·V·CC (single vowel, prime words) =======================
console.log("\n== (d) solutions under free ≤2 / free ≤2 with a single vowel ==");
const dictFF1 = buildDict(F2, F2, 1, true);
console.log(`dictionary: ${dictFF1.length.toLocaleString()} prime words (Python implementation reported 34,587)`);
const d = cover(dictFF1, null, { nodeCap: 6e8, memoCap: 40e6 });
console.log(`exact count of perfect prime pangrams: ${fmt(d.count)}${d.capped ? " (node cap hit — lower bound)" : " (exact)"}   first: ${d.first ? d.first.map(w => w.toUpperCase()).join(" ") : "-"}   (${d.states.toLocaleString()} states, ${(d.ms / 1000).toFixed(0)} s)`);
console.log(`compare: analytic first-moment E ≈ ${Efree.toExponential(3)}  vs  exact ${fmt(d.count)}  -> ratio ${(d.count / Efree).toFixed(2)}`);
