// node roots.js english | greek | hebrew
// (1) English real-dictionary best partial cover (prime-valued isograms, base-26).
// (2) Koine Greek: perfect pangram of the 24 letters, each word prime by ISOPSEPHY (native letter values,
//     summed), Greek phonotactics (onset clusters, diphthongs, final letter ∈ {vowel, ν, ρ, ς, ξ, ψ}).
// (3) Hebrew: 22 letters, gematria values summed, words = 1-3-letter roots (abjad: no vowel rule).
"use strict";
const fs = require("fs");
const PART = process.argv[2] || "all";

function makeCover(nLetters) {
  const FULL = (1 << nLetters) - 1;
  return function cover(items, opts) {
    opts = opts || {};
    const byL = Array.from({ length: nLetters }, () => []); for (const it of items) for (let i = 0; i < nLetters; i++) if (it.m >> i & 1) byL[i].push(it);
    const order = [...Array(nLetters).keys()].sort((a, b) => byL[a].length - byL[b].length);
    const memo = new Map(); let first = null, nodes = 0, capped = false, examples = [];
    function rec(cov, chosen) {
      if (cov === FULL) { if (!first) first = chosen.slice(); if (examples.length < (opts.examples || 0)) examples.push(chosen.slice()); return 1; }
      if (memo.has(cov)) return memo.get(cov);
      nodes++; if (opts.nodeCap && nodes > opts.nodeCap) { capped = true; return 0; }
      let L = -1; for (const i of order) if (!(cov >> i & 1)) { L = i; break; }
      let n = 0;
      for (const it of byL[L]) { if (it.m & cov) continue; chosen.push(it.w); n += rec(cov | it.m, chosen); chosen.pop(); if (opts.firstOnly && first) break; }
      if (memo.size < 15e6) memo.set(cov, n); return n;
    }
    const t0 = Date.now(); const n = rec(0, []);
    return { count: n, first, examples, states: memo.size, capped, ms: Date.now() - t0 };
  };
}
// largest cover by disjoint words: full cover with a budget of skipped letters, budget 1, 2, ... (rarest-first; memo on failures)
function bestPartialSlack(items, nLetters) {
  const FULL = (1 << nLetters) - 1;
  const byL = Array.from({ length: nLetters }, () => []); for (const it of items) for (let i = 0; i < nLetters; i++) if (it.m >> i & 1) byL[i].push(it);
  const order = [...Array(nLetters).keys()].sort((a, b) => byL[a].length - byL[b].length);
  for (let budget = 1; budget < nLetters; budget++) {
    const memo = new Set(); let found = null, nodes = 0, capped = false;
    function rec(cov, b, chosen) {
      if (cov === FULL) { found = chosen.slice(); return true; }
      const key = cov * 32 + b; if (memo.has(key)) return false;
      nodes++; if (nodes > 2e8) { capped = true; return false; }
      let L = -1; for (const i of order) if (!(cov >> i & 1)) { L = i; break; }
      for (const it of byL[L]) { if (it.m & cov) continue; chosen.push(it.w); if (rec(cov | it.m, b, chosen)) return true; chosen.pop(); }
      if (b > 0 && rec(cov | (1 << L), b - 1, chosen)) return true;
      if (memo.size < 15e6) memo.add(key); return false;
    }
    if (rec(0, budget, [])) { const covered = new Set(found.join("")).size; return { n: covered, words: found, budget, capped: false }; }
    if (capped) return { n: null, capped: true, budget };
  }
}

if (PART === "english" || PART === "all") {
  const ALPHA = "abcdefghijklmnopqrstuvwxyz";
  const value = w => { let v = 0; for (const c of w) v = v * 26 + (c.charCodeAt(0) - 96); return v; };
  const LIM = 12000000, sv = new Uint8Array(LIM + 1), P = []; for (let i = 2; i <= LIM; i++) { if (!sv[i]) { P.push(i); for (let j = i * i; j <= LIM; j += i) sv[j] = 1; } }   // sqrt(26^10) ≈ 1.19e7: complete for 10-letter words
  const isPrime = n => { if (n < 2) return false; for (const p of P) { if (p * p > n) return true; if (n % p === 0) return n === p; } return true; };
  const words = fs.readFileSync(__dirname + "/words.txt", "utf8").split("\n").filter(w => /^[a-z]{2,10}$/.test(w) && new Set(w).size === w.length && isPrime(value(w)));
  const items = words.map(w => ({ w, m: [...w].reduce((m, c) => m | 1 << (c.charCodeAt(0) - 97), 0) }));
  const t0 = Date.now(); const bp = bestPartialSlack(items, 26);
  if (bp.n) { const cov = bp.words.join(""); console.log(`(1) English (Webster's 2nd): ${words.length.toLocaleString()} prime-valued isograms; best disjoint cover ${bp.n}/26 (exact): ${bp.words.join(" ")}  [${bp.words.map(w => value(w).toLocaleString()).join(", ")}]  uncovered: ${[...ALPHA].filter(c => !cov.includes(c)).join(" ")}  (${((Date.now() - t0) / 1000).toFixed(0)} s)`); }
  else console.log(`(1) English: search capped at budget ${bp.budget}`);
}

if (PART === "greek" || PART === "all") {
  const G = "αβγδεζηθικλμνξοπρστυφχψω";
  const VAL = [1, 2, 3, 4, 5, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500, 600, 700, 800];
  const LAT = ["a", "b", "g", "d", "e", "z", "ē", "th", "i", "k", "l", "m", "n", "x", "o", "p", "r", "s", "t", "u", "ph", "ch", "ps", "ō"];
  const idx = c => G.indexOf(c);
  const VOW = new Set("αεηιουω");
  const CONS = [...G].filter(c => !VOW.has(c));
  const DIPH = ["αι", "ει", "οι", "υι", "αυ", "ευ", "ηυ", "ου"];
  const NUCLEI = [...VOW].concat(DIPH);
  const CL = "βδ βλ βρ γλ γν γρ δμ δρ θλ θν θρ κλ κν κρ κτ μν πλ πν πρ πτ σβ σθ σκ σμ σπ στ σφ σχ τλ τμ τρ φθ φλ φρ χθ χλ χν χρ σκλ σπλ στρ στλ".split(" ");
  const ONSETS = ["", ...CONS, ...CL];
  const CODAS = ["", "ν", "ρ", "σ", "ξ", "ψ"];
  const MEDIAL = [...CONS, ...CL, ..."ντ νθ νδ μπ μβ μφ γκ γγ γχ λπ λκ λφ λχ λμ ρκ ρτ ρμ ρν ρπ ρφ ρχ ρθ ρδ ρβ ργ ρσ νσ".split(" ")];
  const total = VAL.reduce((a, b) => a + b, 0);
  const isPrime = n => { if (n < 2) return false; for (let p = 2; p * p <= n; p++) if (n % p === 0) return false; return true; };
  const value = w => [...w].reduce((s, c) => s + VAL[idx(c)], 0);
  const MAXLEN = +(process.argv[3] || 6);
  const words = new Set();
  const add = w => { if (w.length > MAXLEN || new Set(w).size !== w.length) return; if (isPrime(value(w))) words.add(w); };
  for (const on of ONSETS) for (const nu of NUCLEI) { for (const co of CODAS) add(on + nu + co); for (const me of MEDIAL) for (const nu2 of NUCLEI) for (const co of CODAS) add(on + nu + me + nu2 + co); }
  const list = [...words];
  const items = list.map(w => ({ w, m: [...w].reduce((m, c) => m | 1 << idx(c), 0) }));
  const cover = makeCover(24);
  const r = cover(items, { examples: 6, nodeCap: 3e8 });
  const show = w => { const t = [...w].map(c => LAT[idx(c)]).join(""); return `${w.replace(/σ$/, "ς")} (${t}) = ${value(w)}`; };
  console.log(`\n(2) Koine Greek, isopsephy: sum of all 24 letter values = ${total} (${isPrime(total) ? "prime" : "composite"}, odd ⇒ an odd number of words); ${list.length.toLocaleString()} pronounceable prime words of ≤ ${MAXLEN} letters`);
  console.log(`    perfect Greek pangrams, every word prime by isopsephy: ${r.count.toLocaleString()}${r.capped ? " (node cap hit — lower bound)" : " (exact)"}  (${r.states.toLocaleString()} states, ${(r.ms / 1000).toFixed(0)} s)`);
  for (const ex of r.examples) console.log("      " + ex.map(show).join("  ·  ") + `   Σ = ${ex.reduce((s, w) => s + value(w), 0)}`);
}

if (PART === "hebrew" || PART === "all") {
  const H = "אבגדהוזחטיכלמנסעפצקרשת";
  const VAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400];
  const total = VAL.reduce((a, b) => a + b, 0);
  const isPrime = n => { if (n < 2) return false; for (let p = 2; p * p <= n; p++) if (n % p === 0) return false; return true; };
  const MAXR = +(process.argv[3] || 3);
  const items = [];
  (function gen(start, chosen, m, s) {
    if (chosen.length) if (isPrime(s)) items.push({ w: chosen.join(""), m });
    if (chosen.length === MAXR) return;
    for (let i = start; i < 22; i++) gen(i + 1, chosen.concat(H[i]), m | 1 << i, s + VAL[i]);
  })(0, [], 0, 0);
  const odd = [...H].filter((c, i) => VAL[i] % 2 === 1);
  const cover = makeCover(22);
  const r = cover(items, { examples: 3 });
  const value = w => [...w].reduce((s, c) => s + VAL[H.indexOf(c)], 0);
  console.log(`\n(3) Hebrew, gematria: sum of the 22 letters = ${total}; letters with ODD value: ${odd.join(" ")} (${odd.length}); ${items.length} roots of 1-${MAXR} letters with prime value`);
  console.log(`    perfect Hebrew pangrams of prime roots (letters within a root unordered): ${r.count.toLocaleString()} (exact)  (${r.ms} ms)`);
  for (const ex of r.examples) console.log("      " + ex.map(w => `${w}=${value(w)}`).join("  ") + `   Σ = ${total}`);
}
