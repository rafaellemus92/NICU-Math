"""Dependency-free information page for the API entrypoint."""


def render_homepage(offline: bool) -> str:
    mode = 'Offline mode' if offline else 'Evidence mode · unvalidated'
    evidence = ('Evidence search and generated answers are disabled in this mode.'
                if offline else 'Legacy evidence services are enabled but not integration-validated.')
    return _PAGE.replace('{{MODE}}', mode).replace('{{EVIDENCE}}', evidence)


_PAGE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="NICU-Math: synthetic research and education. API documentation, service health, and project scope.">
  <title>NICU-Math · Synthetic research</title>
  <style>
    :root { color-scheme: light; --ink:#173b38; --muted:#4d625e; --line:#cbd7d0; --paper:#f5f6ef; --accent:#16594c; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--paper); color:var(--ink); font:17px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    a { color:var(--accent); text-underline-offset:.2em; }
    a:focus-visible { outline:3px solid #9c4f18; outline-offset:5px; }
    .skip { position:absolute; left:1rem; top:-5rem; padding:.6rem; background:white; }
    .skip:focus { top:1rem; }
    .wrap { width:min(1080px,100% - 48px); margin:auto; }
    header { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:28px 0; border-bottom:1px solid var(--line); }
    .brand { font-weight:750; letter-spacing:-.04em; font-size:24px; }
    .mode { border:1px solid #adc8b8; background:#e4eee2; padding:5px 12px; border-radius:99px; font-size:13px; font-weight:650; }
    main { padding:64px 0 48px; }
    .eyebrow { margin:0 0 14px; font-size:12px; font-weight:750; letter-spacing:.14em; text-transform:uppercase; }
    h1 { max-width:800px; font-size:clamp(36px,5.5vw,62px); line-height:1.08; letter-spacing:-.055em; margin:0 0 24px; }
    .intro { max-width:680px; color:var(--muted); font-size:20px; margin:0; }
    nav { display:flex; flex-wrap:wrap; gap:12px; margin:30px 0; }
    .button { display:inline-flex; min-height:48px; align-items:center; justify-content:center; padding:10px 20px; border:1px solid var(--accent); border-radius:8px; font-weight:650; text-decoration:none; }
    .primary { background:var(--accent); color:white; }
    .button:hover { box-shadow:0 2px 0 var(--ink); }
    .scope { padding:16px 20px; border-left:3px solid #977046; background:#ede9dc; font-size:15px; margin:0 0 40px; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
    section { border-top:1px solid var(--line); padding-top:22px; }
    h2 { font-size:23px; letter-spacing:-.025em; margin:0 0 14px; }
    p { margin:0 0 14px; }
    ul { margin:0; padding-left:22px; }
    li { margin:9px 0; }
    code { font-size:.85em; padding:2px 5px; border-radius:4px; background:#e5e9e0; overflow-wrap:anywhere; }
    .separate { margin-top:32px; background:white; border:1px solid var(--line); border-radius:12px; padding:24px; }
    .separate p { max-width:830px; color:var(--muted); }
    footer { border-top:1px solid var(--line); padding:24px 0 36px; color:var(--muted); font-size:13px; }
    @media(max-width:600px) { .wrap { width:calc(100% - 32px); } header { padding:20px 0; align-items:flex-start; flex-wrap:wrap; } main { padding-top:40px; } .intro { font-size:18px; } .grid { grid-template-columns:1fr; gap:28px; } nav .button { flex:1 1 180px; } .separate { padding:20px; } }
  </style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="wrap">
  <header><span class="brand">NICU-Math</span><span class="mode">{{MODE}}</span></header>
  <main id="content">
    <p class="eyebrow">Research &amp; education</p>
    <h1>Explore the mathematics.<br>Keep the limits in view.</h1>
    <p class="intro">A workspace for synthetic scenarios and mathematical research. Respiratory mechanics and neonatal hemodynamics are the intended research scope, not a delivered clinical model.</p>
    <nav aria-label="API resources">
      <a class="button primary" href="/docs">Open API documentation</a>
      <a class="button" href="/healthz">Check API health</a>
    </nav>
    <p class="scope"><strong>Synthetic research and education only.</strong> Models are unvalidated and must not guide patient-specific treatment. Do not enter patient data.</p>
    <div class="grid">
      <section aria-labelledby="available">
        <h2 id="available">Available through this API</h2>
        <ul>
          <li>Interactive endpoint documentation at <code>/docs</code>. That page is Swagger UI and loads its script and stylesheet from a public CDN, so it needs internet access even when the API runs offline; the schema at <code>/openapi.json</code> is served locally.</li>
          <li>Service status and configured mode at <code>/healthz</code>.</li>
          <li>Seeded toy simulations of acidosis, NEC and extubation, using synthetic inputs. These are software demonstrations, not calibrated predictions.</li>
        </ul>
      </section>
      <section aria-labelledby="limits">
        <h2 id="limits">Current limits</h2>
        <ul>
          <li>{{EVIDENCE}}</li>
          <li>No patient-data uploads or document hosting.</li>
          <li>No validated respiratory-mechanics or neonatal-hemodynamics model is provided here. The repository's two-compartment passive-emptying model is a closed-form teaching instrument in <code>physiology/</code>; this API does not serve it.</li>
          <li>No patient-specific treatment recommendations.</li>
        </ul>
      </section>
    </div>
    <section class="separate" aria-labelledby="interface">
      <h2 id="interface">Looking for the research interface?</h2>
      <p>The Streamlit research interface runs separately and is not hosted at this endpoint. This page introduces the FastAPI service; it does not launch the Streamlit application.</p>
      <p>For local development, follow the repository README to start both services. The Streamlit entrypoint is <code>ui/app.py</code>.</p>
    </section>
  </main>
  <footer>NICU-Math · Hypotheses, proofs and numerical evidence are distinct. Clinical finite-time transitions are not PDE singularities.</footer>
</div>
</body>
</html>
'''
