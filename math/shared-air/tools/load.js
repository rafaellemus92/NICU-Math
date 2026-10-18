'use strict';
// Load the Model core that is embedded in the Shared Air page, without a browser.
// The page lives in web/public/shared-air/index.html (served at /shared-air). By default it is found
// from this script's own folder: tools/ -> math/shared-air/ -> ../../web/public/shared-air/index.html.
// An HTML path given as an argument is resolved relative to math/shared-air/ (absolute paths also work).
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const START = '// Shared Air model core';
const END = "if (typeof module !== 'undefined') module.exports = Model;";
const DEF_RE = /  const DEF = (\{.*\});\n/;

const PAGE = path.join('..', '..', 'web', 'public', 'shared-air', 'index.html'); // relative to ROOT
const resolveHtml = p => path.resolve(ROOT, p || PAGE);
const readSource = p => fs.readFileSync(resolveHtml(p), 'utf8');

function loadModel(p) {
  const src = readSource(p);
  const a = src.indexOf(START), b = src.indexOf(END, a);
  if (a < 0 || b < 0) throw new Error('model core markers not found in ' + resolveHtml(p));
  const mod = { exports: null };
  new Function('module', src.slice(a, b + END.length))(mod);
  return mod.exports;
}

// The stored results the page shows before anyone presses Run.
function readDEF(p) {
  const m = readSource(p).match(DEF_RE);
  if (!m) throw new Error('DEF line not found in ' + resolveHtml(p));
  return JSON.parse(m[1]);
}

// Round every number to 3 decimals, as the stored DEF values are.
const r3 = v => Array.isArray(v) ? v.map(r3)
  : (v && typeof v === 'object') ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, r3(x)]))
  : (typeof v === 'number' ? Math.round(v * 1000) / 1000 : v);

module.exports = { ROOT, PAGE, DEF_RE, resolveHtml, readSource, loadModel, readDEF, r3 };
