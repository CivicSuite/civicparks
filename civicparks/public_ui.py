"""HTML landing surface for the CivicParks runtime."""


def render_public_lookup_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CivicParks v0.1.0</title>
  <style>
    :root{--ink:#162415;--muted:#536b51;--line:#c8dfc0;--paper:#f8fff4;--card:#ffffff;--accent:#397046;--sun:#d9972b}
    *{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:radial-gradient(circle at top right,#fff1bf,transparent 32rem),linear-gradient(135deg,#f8fff4,#edf8ff);color:var(--ink)}
    main{max-width:1120px;margin:0 auto;padding:3rem 1.25rem}.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:2rem;align-items:center}
    h1{font-size:clamp(2.5rem,7vw,5rem);line-height:.92;margin:.25rem 0}.eyebrow{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    p{font-size:1.08rem;line-height:1.65;color:var(--muted)}.panel,.card{background:rgba(255,255,255,.9);border:1px solid var(--line);border-radius:28px;box-shadow:0 20px 60px rgba(22,36,21,.1)}
    .panel{padding:1.5rem}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2rem 0}.card{padding:1.2rem}.card h2{margin-top:0;color:var(--accent)}
    code{background:#eaf5e4;padding:.15rem .35rem;border-radius:.35rem}.boundary{border-left:6px solid var(--sun);padding-left:1rem}
    a{color:var(--accent);font-weight:700}@media(max-width:760px){.hero,.cards{grid-template-columns:1fr}main{padding:2rem 1rem}h1{font-size:3rem}}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <div>
      <p class="eyebrow">CivicSuite / CivicParks</p>
      <h1>Parks and recreation answers without replacing registration systems.</h1>
      <p>CivicParks v0.1.0 helps staff answer facility, program, rental, league, and park-rule questions while keeping payments, registration records, and work orders in existing systems.</p>
    </div>
    <div class="panel">
      <h2>v0.1.0 boundary</h2>
      <p class="boundary">No payments, no registrations, no participant records, no reservation writes, no crew dispatch, no live LLM calls, and no connector runtime ship in this release.</p>
    </div>
  </section>
  <section class="cards">
    <article class="card"><h2>Facility Rules</h2><p>Cited drafts over park rules, rental terms, fee schedules, and league policies.</p></article>
    <article class="card"><h2>Program Help</h2><p>Plain-English program descriptions with accessibility review and registration links.</p></article>
    <article class="card"><h2>Civic311 Ready</h2><p>Maintenance triage prepares a staff-reviewed handoff category without creating work orders.</p></article>
  </section>
  <section class="panel">
    <h2>Architecture</h2>
    <p><strong>Resident or staff question</strong> -> CivicParks deterministic API -> CivicCore foundation. Registration and Civic311 adapters are future read-only or handoff designs, not v0.1.0 write paths.</p>
    <p>Dependency: <code>civiccore==0.2.0</code>. Repo: <a href="https://github.com/CivicSuite/civicparks">CivicSuite/civicparks</a>.</p>
  </section>
</main>
</body>
</html>"""
