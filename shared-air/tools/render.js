'use strict';
// Optional: open shared_air.html in headless Chromium (Playwright) at desktop and phone width and report
// page errors, horizontal overflow and the rendered Test 4/5 finding text. Google Fonts requests are
// blocked so the check works offline. Screenshots only if a directory is given.
// Usage: node tools/render.js [screenshot-dir]
// Playwright is not bundled. Point NODE_PATH at an existing install, e.g.
//   NODE_PATH=/opt/node22/lib/node_modules node tools/render.js
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const { resolveHtml } = require('./load.js');

const shots = process.argv[2] ? path.resolve(process.cwd(), process.argv[2]) : null;
(async () => {
  const browser = await chromium.launch();
  let problems = 0;
  for (const [name, vp, scheme] of [['desktop', { width: 1100, height: 900 }, 'light'], ['phone', { width: 390, height: 800 }, 'dark']]) {
    const page = await browser.newPage({ viewport: vp, colorScheme: scheme });
    const errs = [];
    page.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED/.test(m.text())) errs.push(m.text()); });
    page.on('pageerror', e => errs.push(String(e)));
    await page.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    await page.goto('file://' + resolveHtml());
    await page.waitForTimeout(1500);
    const info = await page.evaluate(() => ({ f4: document.querySelector('#f4').innerText, f5: document.querySelector('#f5').innerText,
      sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    const bad = /NaN|undefined|Infinity/.test(info.f4 + info.f5);
    if (errs.length || info.sw > info.cw || bad) problems++;
    console.log('=====', name, scheme, '| errors:', JSON.stringify(errs), '| scrollWidth', info.sw, 'clientWidth', info.cw, bad ? '| NaN/undefined in text' : '');
    if (name === 'desktop') { console.log('Test 4 finding:\n' + info.f4); console.log('Test 5 finding:\n' + info.f5); }
    if (shots) {
      fs.mkdirSync(shots, { recursive: true });
      for (const id of ['t4', 't5']) { const el = await page.$('#' + id); if (el) await el.screenshot({ path: path.join(shots, `${name}_${id}.png`) }); }
    }
    await page.close();
  }
  await browser.close();
  process.exit(problems ? 1 : 0);
})();
