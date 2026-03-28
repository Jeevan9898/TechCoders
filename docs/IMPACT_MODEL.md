<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AutonomIQ — Business Impact Model</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

  :root {
    --bg: #0b0f1a;
    --bg2: #111827;
    --bg3: #1a2235;
    --border: rgba(255,255,255,0.07);
    --text: #e8eaf0;
    --muted: #7b859e;
    --accent: #3b82f6;
    --accent2: #6366f1;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --teal: #14b8a6;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 0;
  }

  /* ─── HEADER ─── */
  .header {
    background: linear-gradient(135deg, #0d1421 0%, #111827 60%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 48px 60px 40px;
    position: relative;
    overflow: hidden;
  }
  .header::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
  }
  .header-meta {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
  }
  .header h1 {
    font-size: 38px;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.15;
  }
  .header h1 span { color: var(--accent2); }
  .header-sub {
    font-size: 15px;
    color: var(--muted);
    margin-top: 8px;
    font-weight: 400;
  }

  /* ─── MAIN LAYOUT ─── */
  .main { padding: 40px 60px; }

  /* ─── SUMMARY KPIs ─── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 36px;
  }
  .kpi-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 18px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
  }
  .kpi-card.blue::after { background: var(--accent); }
  .kpi-card.indigo::after { background: var(--accent2); }
  .kpi-card.green::after { background: var(--success); }
  .kpi-card.amber::after { background: var(--warning); }
  .kpi-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 8px; }
  .kpi-value { font-size: 26px; font-weight: 600; letter-spacing: -0.02em; }
  .kpi-sub { font-size: 11px; color: var(--muted); margin-top: 4px; }
  .kpi-card.blue .kpi-value { color: #60a5fa; }
  .kpi-card.indigo .kpi-value { color: #818cf8; }
  .kpi-card.green .kpi-value { color: #34d399; }
  .kpi-card.amber .kpi-value { color: #fbbf24; }

  /* ─── SECTION HEADERS ─── */
  .section-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ─── IMPACT BARS ─── */
  .impact-list { display: flex; flex-direction: column; gap: 14px; margin-bottom: 36px; }
  .impact-row {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
  }
  .impact-row:hover { border-color: rgba(255,255,255,0.15); background: var(--bg3); }
  .impact-row.expanded { border-color: rgba(99,102,241,0.3); }
  .impact-row-header {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .impact-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .impact-name {
    flex: 1;
    font-size: 14px;
    font-weight: 500;
  }
  .impact-monthly {
    font-size: 12px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-right: 16px;
  }
  .impact-annual {
    font-size: 15px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    min-width: 90px;
    text-align: right;
  }
  .impact-chevron {
    color: var(--muted);
    font-size: 12px;
    transition: transform 0.2s;
    margin-left: 8px;
  }
  .impact-row.expanded .impact-chevron { transform: rotate(90deg); }
  .bar-outer {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    margin-top: 12px;
    overflow: hidden;
  }
  .bar-inner {
    height: 100%;
    border-radius: 2px;
    transition: width 1s cubic-bezier(0.34,1.56,0.64,1);
    width: 0;
  }
  .impact-detail {
    display: none;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--border);
    font-size: 13px;
    color: var(--muted);
    line-height: 1.7;
  }
  .impact-row.expanded .impact-detail { display: block; }
  .calc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
  }
  .calc-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
  }
  .calc-box-title { color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
  .calc-line { color: var(--text); line-height: 1.8; }

  /* ─── ASSUMPTIONS SLIDER ─── */
  .simulator-box {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 36px;
  }
  .sim-title {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 20px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .sim-badge {
    font-size: 10px;
    background: rgba(99,102,241,0.2);
    color: #818cf8;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .slider-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .slider-row { display: flex; flex-direction: column; gap: 8px; }
  .slider-label {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
  }
  .slider-name { color: var(--muted); }
  .slider-val {
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-weight: 500;
  }
  input[type=range] {
    -webkit-appearance: none;
    width: 100%;
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 2px;
    outline: none;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px; height: 16px;
    border-radius: 50%;
    background: var(--accent2);
    cursor: pointer;
    transition: transform 0.15s;
  }
  input[type=range]::-webkit-slider-thumb:hover { transform: scale(1.2); }
  .sim-total {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .sim-total-label { font-size: 13px; color: var(--muted); }
  .sim-total-val {
    font-size: 24px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    color: #818cf8;
    transition: color 0.3s;
  }

  /* ─── SENSITIVITY TABLE ─── */
  .sensitivity-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-bottom: 36px;
  }
  .sensitivity-table th {
    text-align: left;
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
  }
  .sensitivity-table td {
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
  }
  .sensitivity-table tr:last-child td { border-bottom: none; }
  .sensitivity-table tr:hover td { background: var(--bg3); }
  .scenario-pill {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 500;
  }
  .pill-green { background: rgba(16,185,129,0.15); color: #34d399; }
  .pill-amber { background: rgba(245,158,11,0.15); color: #fbbf24; }
  .pill-red { background: rgba(239,68,68,0.15); color: #f87171; }
  .pill-gray { background: rgba(255,255,255,0.06); color: var(--muted); }

  /* ─── FOOTER ─── */
  .footer {
    border-top: 1px solid var(--border);
    padding: 20px 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--muted);
  }

  /* ─── PRINT / PDF ─── */
  @media print {
    body { background: #fff; color: #000; }
    .header { background: #0f172a; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .kpi-card, .impact-row, .simulator-box { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .impact-detail { display: block !important; }
    .impact-chevron { display: none; }
    input[type=range] { display: none; }
    .page-break { page-break-before: always; }
  }
</style>
</head>
<body>

<div class="header">
  <div class="header-meta">ET Gen AI Hackathon 2026 &nbsp;·&nbsp; Team TechCoders &nbsp;·&nbsp; v2.0</div>
  <h1>Autono<span>IQ</span> — Business Impact Model</h1>
  <div class="header-sub">Quantified annual value for a mid-size IT services firm responding to 40 RFPs/month</div>
</div>

<div class="main">

  <!-- KPIs -->
  <div class="kpi-grid">
    <div class="kpi-card blue">
      <div class="kpi-label">Total annual impact</div>
      <div class="kpi-value" id="kpi-total">$10.7M</div>
      <div class="kpi-sub">Across 4 impact areas</div>
    </div>
    <div class="kpi-card indigo">
      <div class="kpi-label">Autonomy rate</div>
      <div class="kpi-value">94.2%</div>
      <div class="kpi-sub">Steps without human input</div>
    </div>
    <div class="kpi-card green">
      <div class="kpi-label">FTEs freed per year</div>
      <div class="kpi-value">~8</div>
      <div class="kpi-sub">Redeployable analysts</div>
    </div>
    <div class="kpi-card amber">
      <div class="kpi-label">Monthly impact</div>
      <div class="kpi-value" id="kpi-monthly">$897K</div>
      <div class="kpi-sub">Rolling average</div>
    </div>
  </div>

  <!-- Impact Breakdown -->
  <div class="section-title">Impact breakdown — click to expand</div>
  <div class="impact-list">

    <div class="impact-row" id="row-0" onclick="toggleRow(0)">
      <div class="impact-row-header">
        <div class="impact-dot" style="background:#3b82f6"></div>
        <div class="impact-name">Labour cost reduction</div>
        <div class="impact-monthly">$81,600 / mo</div>
        <div class="impact-annual" style="color:#60a5fa">$979K / yr</div>
        <div class="impact-chevron">▶</div>
      </div>
      <div class="bar-outer"><div class="bar-inner" id="bar-0" style="background:#3b82f6;width:0%"></div></div>
      <div class="impact-detail">
        Reducing per-RFP effort from 36 person-hours (3 people × 12 hrs) to just 2 hours of human review. At $60/hr fully-loaded cost, this represents a 94.4% reduction in labour cost per RFP.
        <div class="calc-grid">
          <div class="calc-box">
            <div class="calc-box-title">Before</div>
            <div class="calc-line">12 hrs × 3 people = 36 ph/RFP</div>
            <div class="calc-line">36 × $60 = $2,160/RFP</div>
            <div class="calc-line">× 40 RFPs = $86,400/mo</div>
          </div>
          <div class="calc-box">
            <div class="calc-box-title">After</div>
            <div class="calc-line">2 hrs × 1 reviewer = 2 ph/RFP</div>
            <div class="calc-line">2 × $60 = $120/RFP</div>
            <div class="calc-line">× 40 RFPs = $4,800/mo</div>
          </div>
        </div>
      </div>
    </div>

    <div class="impact-row" id="row-1" onclick="toggleRow(1)">
      <div class="impact-row-header">
        <div class="impact-dot" style="background:#6366f1"></div>
        <div class="impact-name">Missed RFPs recovered</div>
        <div class="impact-monthly">$392,000 / mo</div>
        <div class="impact-annual" style="color:#818cf8">$4.7M / yr</div>
        <div class="impact-chevron">▶</div>
      </div>
      <div class="bar-outer"><div class="bar-inner" id="bar-1" style="background:#6366f1;width:0%"></div></div>
      <div class="impact-detail">
        The single largest driver. 4 RFPs/month are currently missed due to bandwidth limits. AutonomIQ handles detection and processing autonomously, recovering this lost pipeline.
        <div class="calc-grid">
          <div class="calc-box">
            <div class="calc-box-title">Recovery math</div>
            <div class="calc-line">4 missed RFPs × 28% win rate</div>
            <div class="calc-line">= 1.12 additional wins/mo</div>
            <div class="calc-line">× $350K ACV = $392K/mo</div>
          </div>
          <div class="calc-box">
            <div class="calc-box-title">Conservative case (50%)</div>
            <div class="calc-line">2 RFPs recovered/mo</div>
            <div class="calc-line">0.56 additional wins/mo</div>
            <div class="calc-line">= ~$2.35M/yr</div>
          </div>
        </div>
      </div>
    </div>

    <div class="impact-row" id="row-2" onclick="toggleRow(2)">
      <div class="impact-row-header">
        <div class="impact-dot" style="background:#10b981"></div>
        <div class="impact-name">Win rate improvement (+3%)</div>
        <div class="impact-monthly">$420,000 / mo</div>
        <div class="impact-annual" style="color:#34d399">$5.0M / yr</div>
        <div class="impact-chevron">▶</div>
      </div>
      <div class="bar-outer"><div class="bar-inner" id="bar-2" style="background:#10b981;width:0%"></div></div>
      <div class="impact-detail">
        Faster turnaround, accurate requirement matching, and competitive pricing directly improve proposal quality. A conservative +3pp win rate improvement (28% → 31%) is assumed. Note: 1% improvement alone = $1.68M/yr.
        <div class="calc-grid">
          <div class="calc-box">
            <div class="calc-box-title">Uplift math</div>
            <div class="calc-line">40 RFPs × 3% uplift = 1.2 wins</div>
            <div class="calc-line">× $350K ACV = $420K/mo</div>
            <div class="calc-line">× 12 = $5.04M/yr</div>
          </div>
          <div class="calc-box">
            <div class="calc-box-title">Sensitivity</div>
            <div class="calc-line">+1% win rate = $1.68M/yr</div>
            <div class="calc-line">+2% win rate = $3.36M/yr</div>
            <div class="calc-line">+3% win rate = $5.04M/yr</div>
          </div>
        </div>
      </div>
    </div>

    <div class="impact-row" id="row-3" onclick="toggleRow(3)">
      <div class="impact-row-header">
        <div class="impact-dot" style="background:#f59e0b"></div>
        <div class="impact-name">Rework &amp; error reduction</div>
        <div class="impact-monthly">$3,648 / mo</div>
        <div class="impact-annual" style="color:#fbbf24">$44K / yr</div>
        <div class="impact-chevron">▶</div>
      </div>
      <div class="bar-outer"><div class="bar-inner" id="bar-3" style="background:#f59e0b;width:0%"></div></div>
      <div class="impact-detail">
        Manual pricing error rate drops from 22% to ~3% with AutonomIQ's structured pricing model and live market data validation. Each rework event costs 8 person-hours.
        <div class="calc-grid">
          <div class="calc-box">
            <div class="calc-box-title">Before</div>
            <div class="calc-line">22% error × 40 RFPs = 8.8 reworks</div>
            <div class="calc-line">8.8 × $480 = $4,224/mo</div>
          </div>
          <div class="calc-box">
            <div class="calc-box-title">After</div>
            <div class="calc-line">3% error × 40 RFPs = 1.2 reworks</div>
            <div class="calc-line">1.2 × $480 = $576/mo</div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Interactive Simulator -->
  <div class="section-title">Scenario simulator</div>
  <div class="simulator-box">
    <div class="sim-title">Adjust assumptions to model your firm <span class="sim-badge">Interactive</span></div>
    <div class="slider-grid">
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">RFPs per month</span>
          <span class="slider-val" id="sv-rfps">40</span>
        </div>
        <input type="range" min="10" max="120" value="40" oninput="updateSim('rfps',this.value)">
      </div>
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">Average contract value ($K)</span>
          <span class="slider-val" id="sv-acv">$350K</span>
        </div>
        <input type="range" min="50" max="2000" step="50" value="350" oninput="updateSim('acv',this.value)">
      </div>
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">Current win rate (%)</span>
          <span class="slider-val" id="sv-wr">28%</span>
        </div>
        <input type="range" min="10" max="60" value="28" oninput="updateSim('wr',this.value)">
      </div>
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">Win rate improvement (pp)</span>
          <span class="slider-val" id="sv-wri">3pp</span>
        </div>
        <input type="range" min="1" max="10" value="3" oninput="updateSim('wri',this.value)">
      </div>
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">RFPs missed per month</span>
          <span class="slider-val" id="sv-missed">4</span>
        </div>
        <input type="range" min="0" max="20" value="4" oninput="updateSim('missed',this.value)">
      </div>
      <div class="slider-row">
        <div class="slider-label">
          <span class="slider-name">Hourly cost per person ($)</span>
          <span class="slider-val" id="sv-rate">$60</span>
        </div>
        <input type="range" min="30" max="200" step="5" value="60" oninput="updateSim('rate',this.value)">
      </div>
    </div>
    <div class="sim-total">
      <span class="sim-total-label">Estimated annual impact for your firm</span>
      <span class="sim-total-val" id="sim-result">$10.7M / yr</span>
    </div>
  </div>

  <!-- Sensitivity Table -->
  <div class="section-title">Sensitivity analysis</div>
  <table class="sensitivity-table">
    <thead>
      <tr>
        <th>Scenario</th>
        <th>Change from base</th>
        <th>Annual impact</th>
        <th>vs. Base</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Base case</td>
        <td>As modelled</td>
        <td><strong>~$10.7M</strong></td>
        <td><span class="scenario-pill pill-green">Baseline</span></td>
      </tr>
      <tr>
        <td>50% of missed RFPs recovered</td>
        <td>Revenue recovery halved</td>
        <td>~$8.4M</td>
        <td><span class="scenario-pill pill-amber">−21%</span></td>
      </tr>
      <tr>
        <td>Win rate improves only +1pp</td>
        <td>$3.36M less revenue uplift</td>
        <td>~$7.3M</td>
        <td><span class="scenario-pill pill-amber">−32%</span></td>
      </tr>
      <tr>
        <td>Both pessimistic scenarios</td>
        <td>Combined downside</td>
        <td>~$5.0M</td>
        <td><span class="scenario-pill pill-red">−53%</span></td>
      </tr>
      <tr>
        <td>Labour savings only</td>
        <td>No revenue assumptions</td>
        <td>~$1.0M</td>
        <td><span class="scenario-pill pill-gray">Floor</span></td>
      </tr>
    </tbody>
  </table>

</div>

<div class="footer">
  <span>AutonomIQ &nbsp;·&nbsp; TechCoders &nbsp;·&nbsp; ET Gen AI Hackathon 2026</span>
  <span>All figures are estimates based on public industry benchmarks</span>
</div>

<script>
const impactPcts = [9.1, 43.7, 46.8, 0.4];
const totals = [979200, 4704000, 5040000, 43776];
const maxImpact = 5040000;

function animateBars() {
  impactPcts.forEach((pct, i) => {
    setTimeout(() => {
      document.getElementById('bar-'+i).style.width = pct+'%';
    }, 200 + i*150);
  });
}

function toggleRow(i) {
  const row = document.getElementById('row-'+i);
  row.classList.toggle('expanded');
}

const sim = { rfps:40, acv:350, wr:28, wri:3, missed:4, rate:60 };

function updateSim(key, val) {
  sim[key] = parseFloat(val);
  const labels = { rfps:'sv-rfps', acv:'sv-acv', wr:'sv-wr', wri:'sv-wri', missed:'sv-missed', rate:'sv-rate' };
  const formats = {
    rfps: v => v,
    acv: v => '$'+v+'K',
    wr: v => v+'%',
    wri: v => v+'pp',
    missed: v => v,
    rate: v => '$'+v
  };
  document.getElementById(labels[key]).textContent = formats[key](val);

  const labour_before = 36 * sim.rate * sim.rfps * 12;
  const labour_after = 2 * sim.rate * sim.rfps * 12;
  const labour = labour_before - labour_after;

  const missed_rev = sim.missed * (sim.wr/100) * (sim.acv*1000) * 12;
  const winrate_rev = sim.rfps * (sim.wri/100) * (sim.acv*1000) * 12;
  const rework = (0.22 - 0.03) * sim.rfps * 8 * sim.rate * 12;

  const total = labour + missed_rev + winrate_rev + rework;

  const el = document.getElementById('sim-result');
  if (total >= 1e6) el.textContent = '$' + (total/1e6).toFixed(1) + 'M / yr';
  else el.textContent = '$' + Math.round(total/1000) + 'K / yr';

  el.style.color = total >= 10e6 ? '#818cf8' : total >= 5e6 ? '#34d399' : '#fbbf24';
}

window.onload = () => { animateBars(); };
</script>
</body>
</html>
