// Cross-check of the main study with an independent implementation (Node):
// different language, different primality test (sieve + trial division, complete
// below 26^8; Miller-Rabin bases 2..37 above), different counting method (memoised
// subset DP, rarest-letter-first).  Uses the main study's cluster lists and word
// rule exactly: onset ∈ ONSETS, nucleus = one vowel or an ordered pair of distinct
// vowels, coda ∈ CODAS, letters distinct.  Expected (README.md of the main study):
//   16,243 prime words; 0 perfect pangrams; N0 = 353,750,976,000 pronounceable
//   pangrams; 0 pangrams whose words all end in a letter coprime to 26.
"use strict";
const { execSync } = require("child_process");
const lists = JSON.parse(execSync("python3 -c \"import json,sys; sys.path.insert(0,'" + __dirname + "/..'); from clusters import ONSETS, CODAS, VOWELS; print(json.dumps({'onsets':list(ONSETS),'codas':list(CODAS),'vowels':VOWELS}))\"").toString());
const ALPHA = "abcdefghijklmnopqrstuvwxyz", VOW = new Set(lists.vowels), CONS = [...ALPHA].filter(c => !VOW.has(c));
const FULL = (1 << 26) - 1;

function value(w) { let v = 0; for (const c of w) v = v * 26 + (c.charCodeAt(0) - 96); return v; }
// primality: sieve to sqrt(26^8) for trial division, deterministic Miller-Rabin (BigInt) above
const LIM = 460000, sv = new Uint8Array(LIM + 1), P = []; for (let i = 2; i <= LIM; i++) { if (!sv[i]) { P.push(i); for (let j = i * i; j <= LIM; j += i) sv[j] = 1; } }
function mrBig(n) { const N = BigInt(n); if (N < 2n) return false; for (const p of [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n]) { if (N % p === 0n) return N === p; }
  let d = N - 1n, s = 0; while (d % 2n === 0n) { d /= 2n; s++; }
  const pw = (b, e, m) => { let r = 1n; b %= m; while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return r; };
  for (const a of [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n]) { let x = pw(a, d, N); if (x === 1n || x === N - 1n) continue; let ok = false; for (let i = 0; i < s - 1; i++) { x = x * x % N; if (x === N - 1n) { ok = true; break; } } if (!ok) return false; } return true; }
function isPrime(n) { if (n < 2) return false; if (n < 2.1e11) { for (const p of P) { if (p * p > n) return true; if (n % p === 0) return n === p; } return true; } return mrBig(n); }
function mask(w) { let m = 0; for (const c of w) m |= 1 << (c.charCodeAt(0) - 97); return m; }

// dictionary under the main study's rule
const nuclei = [...VOW]; for (const a of VOW) for (const b of VOW) if (a !== b) nuclei.push(a + b);
const all = [], prime = [];
for (const on of lists.onsets) for (const nu of nuclei) for (const co of lists.codas) {
  const w = on + nu + co; if (new Set(w).size !== w.length) continue;
  all.push(w); if (isPrime(value(w))) prime.push(w);
}
const byLen = {}; for (const w of prime) byLen[w.length] = (byLen[w.length] || 0) + 1;
console.log(`pronounceable words: ${all.length.toLocaleString()}  (main study: 289,404)`);
console.log(`prime words: ${prime.length.toLocaleString()}  (main study: 16,243)   by length: ${Object.entries(byLen).map(([k, v]) => k + ":" + v).join(" ")}`);
const GOOD = new Set("acegikoqsuwy");
console.log(`every prime word ends in a letter coprime to 26: ${prime.every(w => GOOD.has(w[w.length - 1]))}`);

// memoised exact-cover count / first solution
function cover(words, opts) {
  opts = opts || {}; const items = words.map(w => ({ w, m: mask(w) }));
  const byL = Array.from({ length: 26 }, () => []); for (const it of items) for (let i = 0; i < 26; i++) if (it.m >> i & 1) byL[i].push(it);
  const order = [...Array(26).keys()].sort((a, b) => byL[a].length - byL[b].length);
  const memo = new Map(); let first = null, nodes = 0, capped = false;
  function rec(cov, chosen) {
    if (cov === FULL) { if (!first) first = chosen.slice(); return 1; }
    if (memo.has(cov)) return memo.get(cov);
    nodes++; if (opts.nodeCap && nodes > opts.nodeCap) { capped = true; return 0; }
    let L = -1; for (const i of order) if (!(cov >> i & 1)) { L = i; break; }
    let n = 0; for (const it of byL[L]) { if (it.m & cov) continue; chosen.push(it.w); n += rec(cov | it.m, chosen); chosen.pop(); if (opts.firstOnly && first) break; }
    if (memo.size < 15e6) memo.set(cov, n); return n;
  }
  const t0 = Date.now(); const n = rec(0, []); return { count: n, first, states: memo.size, capped, ms: Date.now() - t0 };
}
let r = cover(prime, { firstOnly: true });
console.log(`perfect pangrams of prime words: ${r.first ? "FOUND " + r.first.join(" ") : "0"}  (exhaustive, ${r.states.toLocaleString()} states, ${r.ms} ms)   (main study: 0)`);
const good = all.filter(w => GOOD.has(w[w.length - 1]));
r = cover(good, { firstOnly: true });
console.log(`pronounceable pangrams with every word ending in a coprime letter: ${r.first ? "FOUND " + r.first.join(" ") : "0"}  (${good.length.toLocaleString()} such words, exhaustive, ${r.ms} ms)   (main study: 0, packing bound 17 consonants)`);
// largest number of letters coverable by coprime-ending words = 6 vowels + packing bound
function bestPartialSlack(words) {
  const items = words.map(w => ({ w, m: mask(w) }));
  const byL = Array.from({ length: 26 }, () => []); for (const it of items) for (let i = 0; i < 26; i++) if (it.m >> i & 1) byL[i].push(it);
  const order = [...Array(26).keys()].sort((a, b) => byL[a].length - byL[b].length);
  for (let budget = 1; budget < 26; budget++) {
    const memo = new Set(); let found = null;
    function rec(cov, b, chosen) { if (cov === FULL) { found = chosen.slice(); return true; } const key = cov * 32 + b; if (memo.has(key)) return false;
      let L = -1; for (const i of order) if (!(cov >> i & 1)) { L = i; break; }
      for (const it of byL[L]) { if (it.m & cov) continue; chosen.push(it.w); if (rec(cov | it.m, b, chosen)) return true; chosen.pop(); }
      if (b > 0 && rec(cov | (1 << L), b - 1, chosen)) return true; if (memo.size < 15e6) memo.add(key); return false; }
    if (rec(0, budget, [])) return { n: new Set(found.join("")).size, words: found };
  }
}
const bp = bestPartialSlack(good);
console.log(`most letters coverable by coprime-ending words: ${bp.n}/26 = 6 vowels + ${bp.n - 6} consonants  e.g. ${bp.words.join(" ")}   (main study: 17 consonants)`);
if (process.argv[2] === "count") {
  const c = cover(all, { nodeCap: 2e9 });
  console.log(`N0 = pronounceable perfect pangrams ignoring primality: ${c.count.toLocaleString()}${c.capped ? " (capped)" : " (exact)"}  (${c.states.toLocaleString()} states, ${(c.ms / 1000).toFixed(0)} s)   (main study: 353,750,976,000)`);
}
