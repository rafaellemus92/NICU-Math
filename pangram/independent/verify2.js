// Structural check: under English clusters, can a pronounceable perfect pangram have EVERY word
// ending in a letter coprime to 26 (a c e g i k o q s u w y)?  If not, every such pangram contains
// a word whose value is even or divisible by 13 — composite — and the impossibility is a theorem.
const src = require("fs").readFileSync(__dirname + "/verify.js", "utf8");
// reuse definitions by evaluating only the header (everything before the "(a)" section);
// sloppy-mode direct eval with var declarations so the bindings land in this scope
eval(src.split("// ======================= (a)")[0].replace('"use strict";', "").replace(/\bconst\b/g, "var").replace(/\blet\b/g, "var"));
const GOOD = new Set("acegikoqsuwy");
const BAD_CONS = CONS.filter(c => !GOOD.has(c));
console.log("letters coprime to 26 (a value can be prime only if its word ends here):", [...GOOD].join(" "));
console.log("consonants that can never end a prime-valued word:", BAD_CONS.join(" "), `(${BAD_CONS.length} of 20)`);
const all = buildDict(ONSETS, CODAS, 2, false);
const good = all.filter(w => GOOD.has(w[w.length - 1]));
console.log(`English/English pronounceable words: ${all.length.toLocaleString()}; ending in a coprime letter: ${good.length.toLocaleString()}`);
let r = cover(good, null, { nodeCap: 4e8 });
console.log(`perfect pangrams using only such words: ${r.count.toLocaleString()}${r.capped ? " (capped)" : " (exact)"}  -> ${r.count === 0 ? "NONE: every English-cluster pangram contains a word ending in b d f h j l m n p r t v x z, hence a composite value. Impossibility is structural, not probabilistic." : "some exist; the earlier E=0 was numerical"}  (${r.states.toLocaleString()} states, ${r.ms} ms)`);
// where does it break? the largest number of letters coverable by good-ending words alone
function bestPartial(words) {
  const items = words.map(w => ({ w, m: mask(w) })); let best = [0, []];
  function rec(i, cov, chosen) { const n = popcount(cov); if (n > best[0]) best = [n, chosen.slice()]; if (i === 26 || n + (26 - i) <= best[0]) return; if (cov >> i & 1) { rec(i + 1, cov, chosen); return; }
    for (const it of items) if (it.m >> i & 1 && !(it.m & cov)) { chosen.push(it.w); rec(i + 1, cov | it.m, chosen); chosen.pop(); } rec(i + 1, cov, chosen); }
  rec(0, 0, []); return best;
}
function popcount(x) { let c = 0; while (x) { x &= x - 1; c++; } return c; }
const [n, ch] = bestPartial(good);
console.log(`best partial cover with good-ending words: ${n}/26 -> ${ch.join(" ")}; uncovered: ${[...ALPHA].filter(c => !ch.join("").includes(c)).join(" ")}`);
// the same question under the relaxations that DID admit solutions
for (const [name, O, C] of [["English onset / free ≤2 coda", ONSETS, freeClusters(2)], ["free ≤2 onset / English coda", freeClusters(2), CODAS]]) {
  const g = buildDict(O, C, 2, false).filter(w => GOOD.has(w[w.length - 1]));
  const rr = cover(g, null, { firstOnly: true });
  console.log(`${name}: good-ending pangrams ${rr.first ? "exist, e.g. " + rr.first.join(" ") : "none"}`);
}
// corrected model percentage (value 1 gets weight 0)
const pw = w => value(w) < 2 || !GOOD.has(w[w.length - 1]) ? 0 : (13 / 6) / Math.log(value(w));
console.log(`prime-density model check: predicted ${(100 * all.reduce((s, w) => s + pw(w), 0) / all.length).toFixed(2)}% of pronounceable words prime, observed ${(100 * all.filter(w => isPrime(value(w))).length / all.length).toFixed(2)}%`);
