// AutonomIQ - App Data & Logic

const AGENTS = [
  { id:'rfp', name:'RFP Identification', role:'Scans portals & classifies RFPs', status:'active', health:'healthy', uptime:'2d 14h', processed:156, efficiency:94, cpu:23, mem:45, errors:2, avgTime:1.2, enabled:true, color:'#6366f1', task:'Scanning Gov Contracts Portal — 3 new RFPs queued' },
  { id:'orch', name:'Orchestrator', role:'Routes tasks & manages SLA compliance', status:'active', health:'healthy', uptime:'2d 14h', processed:89, efficiency:98, cpu:15, mem:38, errors:0, avgTime:0.8, enabled:true, color:'#10b981', task:'Coordinating workflow RFP-2024-047 — step 3/5' },
  { id:'tech', name:'Technical Match', role:'Extracts requirements & matches products', status:'processing', health:'healthy', uptime:'2d 14h', processed:78, efficiency:91, cpu:45, mem:67, errors:3, avgTime:3.4, enabled:true, color:'#f59e0b', task:'Analyzing 8 requirements for Enterprise Software RFP' },
  { id:'price', name:'Pricing Agent', role:'Builds competitive pricing strategies', status:'idle', health:'warning', uptime:'2d 14h', processed:67, efficiency:89, cpu:8, mem:32, errors:5, avgTime:2.1, enabled:true, color:'#ef4444', task:'Waiting for market data feed — retry in 2m' },
];

const RFPS = [
  { id:'RFP-047', title:'Enterprise Software Modernization Initiative', source:'Government Technology Portal', status:'processing', priority:'high', dueDate:'2024-01-15', value:500000, progress:65, agent:'Technical Match Agent', requirements:8, matches:12 },
  { id:'RFP-046', title:'High-Performance Computing Infrastructure', source:'Research University Procurement', status:'matched', priority:'urgent', dueDate:'2024-01-10', value:750000, progress:85, agent:'Pricing Agent', requirements:6, matches:8 },
  { id:'RFP-045', title:'Cybersecurity Assessment and Implementation', source:'City Government Portal', status:'priced', priority:'high', dueDate:'2024-01-20', value:300000, progress:90, agent:'Orchestrator Agent', requirements:10, matches:15 },
  { id:'RFP-044', title:'IT Staff Training and Certification Program', source:'Corporate Procurement Portal', status:'reviewed', priority:'medium', dueDate:'2024-01-25', value:150000, progress:95, agent:'Human Review', requirements:5, matches:6 },
  { id:'RFP-043', title:'Cloud Migration and Integration Services', source:'Enterprise RFP Platform', status:'detected', priority:'low', dueDate:'2024-02-01', value:425000, progress:15, agent:'RFP Identification Agent', requirements:0, matches:0 },
];

const WORKFLOWS = [
  { id:'WF-001', rfpId:'RFP-047', title:'Enterprise Software Modernization', status:'processing', progress:65, start:'10:00', est:'16:30',
    steps:[
      { name:'RFP Detection', agent:'RFP Identification Agent', status:'completed', start:'10:00', end:'10:15', dur:'15m', output:'RFP detected and classified as High Priority' },
      { name:'Workflow Orchestration', agent:'Orchestrator Agent', status:'completed', start:'10:15', end:'10:20', dur:'5m', output:'Tasks distributed to 3 specialized agents' },
      { name:'Technical Analysis', agent:'Technical Match Agent', status:'processing', start:'10:20', end:null, dur:null, output:'Analyzing 8 requirements — 6/8 matched so far...' },
      { name:'Pricing Analysis', agent:'Pricing Agent', status:'pending', start:null, end:null, dur:null, output:'Waiting for technical analysis completion' },
      { name:'Human Review', agent:'Human Reviewer', status:'pending', start:null, end:null, dur:null, output:'Awaiting human approval' },
    ]
  },
  { id:'WF-002', rfpId:'RFP-045', title:'Cybersecurity Infrastructure', status:'completed', progress:100, start:'08:00', est:'14:00',
    steps:[
      { name:'RFP Detection', agent:'RFP Identification Agent', status:'completed', start:'08:00', end:'08:12', dur:'12m', output:'High-priority RFP detected from Gov portal' },
      { name:'Workflow Orchestration', agent:'Orchestrator Agent', status:'completed', start:'08:12', end:'08:15', dur:'3m', output:'Urgent workflow initiated — SLA: 6h' },
      { name:'Technical Analysis', agent:'Technical Match Agent', status:'completed', start:'08:15', end:'10:30', dur:'2h 15m', output:'15 matching products identified — 94% confidence' },
      { name:'Pricing Analysis', agent:'Pricing Agent', status:'completed', start:'10:30', end:'12:45', dur:'2h 15m', output:'Competitive pricing strategy developed — $300K' },
      { name:'Human Review', agent:'Human Reviewer', status:'completed', start:'12:45', end:'14:00', dur:'1h 15m', output:'Proposal approved and submitted ✓' },
    ]
  },
];

const AUDIT = [
  { time:'14:32', agent:'Orchestrator', action:'Routed RFP-047 to Technical Match Agent — confidence 91%', type:'info' },
  { time:'14:28', agent:'Pricing Agent', action:'Auto-corrected pricing model — SLA risk avoided', type:'success' },
  { time:'14:15', agent:'RFP Identifier', action:'Detected 3 new RFPs from Gov portal', type:'info' },
  { time:'13:58', agent:'Technical Match', action:'Escalated RFP-043 — low confidence score (62%)', type:'warning' },
  { time:'13:44', agent:'Orchestrator', action:'Self-corrected workflow after API timeout (retry 2/3)', type:'success' },
  { time:'13:30', agent:'Pricing Agent', action:'Generated competitive bid for RFP-045 — $300K', type:'success' },
  { time:'13:12', agent:'RFP Identifier', action:'Classified RFP-046 as URGENT — deadline in 48h', type:'warning' },
  { time:'12:55', agent:'Orchestrator', action:'SLA breach predicted for RFP-044 — rerouted to fast track', type:'warning' },
  { time:'12:40', agent:'Technical Match', action:'Matched 15 products for Cybersecurity RFP', type:'success' },
  { time:'12:20', agent:'Human Reviewer', action:'Approved proposal for RFP-045 — submitted to client', type:'success' },
];

const fmt = n => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:0}).format(n);

function statusClass(s){ return ({processing:'s-processing',matched:'s-matched',priced:'s-priced',reviewed:'s-reviewed',approved:'s-reviewed',detected:'s-detected',active:'s-reviewed',idle:'s-detected',warning:'s-warning',error:'s-error'})[s]||'s-detected'; }
function priorityClass(p){ return ({urgent:'p-urgent',high:'p-high',medium:'p-medium',low:'p-low'})[p]||'p-low'; }
function stepColor(s){ return ({completed:'#10b981',processing:'#6366f1',error:'#ef4444',pending:'#cbd5e1'})[s]||'#cbd5e1'; }
function stepBg(s){ return ({completed:'#f0fdf4',processing:'#eef2ff',error:'#fef2f2',pending:'#f8fafc'})[s]||'#f8fafc'; }
function stepIcon(s){ return ({completed:'fa-check',processing:'fa-spinner fa-spin',error:'fa-times',pending:'fa-circle'})[s]||'fa-circle'; }
function auditBg(t){ return ({success:'#f0fdf4',warning:'#fffbeb',info:'#eef2ff'})[t]||'#eef2ff'; }
function auditColor(t){ return ({success:'#10b981',warning:'#f59e0b',info:'#6366f1'})[t]||'#6366f1'; }
function auditIcon(t){ return ({success:'fa-check',warning:'fa-exclamation',info:'fa-bolt'})[t]||'fa-bolt'; }

// ── Navigation ──────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-'+id).classList.add('active');
  document.querySelector('[onclick="showPage(\''+id+'\')"]').classList.add('active');
  const titles = {dashboard:'Command Center',rfps:'RFP Pipeline',agents:'Agent Monitor',workflows:'Workflow Engine',audit:'Audit Trail',settings:'Settings',profile:'My Profile'};
  const subs = {dashboard:'Autonomous enterprise workflow intelligence · Real-time',rfps:'Autonomous RFP detection, analysis, and response generation',agents:'Real-time control and observability for all autonomous agents',workflows:'End-to-end autonomous workflow visualization with full audit trail',audit:'Complete immutable log of every agent decision and action',settings:'System configuration and preferences',profile:'Manage your account, role, and notification preferences'};
  document.getElementById('navbar-title').textContent = titles[id]||id;
  document.getElementById('navbar-sub').textContent = subs[id]||'';
  if(id==='agents') renderAgents();
  if(id==='workflows') renderWorkflows();
  if(id==='audit') renderFullAudit();
}

// ── Clock ────────────────────────────────────────────────────
function updateClock(){
  const now = new Date();
  document.getElementById('live-clock').textContent = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// ── Notification ─────────────────────────────────────────────
function showNotif(msg) {
  const n = document.getElementById('notif');
  document.getElementById('notif-text').textContent = msg;
  n.classList.add('show');
  setTimeout(() => n.classList.remove('show'), 3000);
}

// ── Dashboard ─────────────────────────────────────────────────
function renderAgentHealth() {
  const el = document.getElementById('agent-health-list');
  if(!el) return;
  el.innerHTML = AGENTS.map(a => `
    <div style="margin-bottom:14px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="width:8px;height:8px;border-radius:50%;background:${a.color};display:inline-block"></span>
          <span style="font-size:13px;font-weight:600;color:#0f172a">${a.name}</span>
        </div>
        <div style="display:flex;align-items:center;gap:6px">
          <span style="font-size:11px;color:#94a3b8">${a.processed} tasks</span>
          <span class="status ${statusClass(a.status)}">${a.status}</span>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <div class="progress-bar"><div class="progress-fill" style="width:${a.efficiency}%;background:${a.color}"></div></div>
        <span style="font-size:12px;font-weight:700;color:${a.color};min-width:32px">${a.efficiency}%</span>
      </div>
    </div>`).join('');
}

function renderRecentRFPs() {
  const el = document.getElementById('recent-rfps-list');
  if(!el) return;
  const colors = {urgent:'#ef4444',high:'#f59e0b',medium:'#6366f1',low:'#10b981'};
  el.innerHTML = RFPS.slice(0,4).map(r => `
    <div style="padding:10px 12px;border-radius:10px;background:#f8fafc;border:1px solid #f1f5f9;margin-bottom:8px;cursor:pointer" onclick="showPage('rfps')">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <div style="display:flex;align-items:center;gap:6px">
          <span style="width:7px;height:7px;border-radius:50%;background:${colors[r.priority]||'#94a3b8'};display:inline-block"></span>
          <span style="font-size:11px;font-weight:700;color:#6366f1">${r.id}</span>
        </div>
        <span style="font-size:11px;color:#94a3b8">${r.dueDate}</span>
      </div>
      <div style="font-size:12px;font-weight:600;color:#0f172a;margin-bottom:6px;line-height:1.3">${r.title}</div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span class="status ${statusClass(r.status)}">${r.status}</span>
        <span style="font-size:12px;font-weight:700;color:#10b981">${fmt(r.value)}</span>
      </div>
    </div>`).join('');
}

function renderAuditMini() {
  const el = document.getElementById('audit-mini-list');
  if(!el) return;
  el.innerHTML = AUDIT.slice(0,5).map(a => `
    <div class="audit-item">
      <div class="audit-icon" style="background:${auditBg(a.type)};color:${auditColor(a.type)}"><i class="fas ${auditIcon(a.type)}"></i></div>
      <div style="flex:1;min-width:0">
        <div class="audit-agent">${a.agent}</div>
        <div class="audit-action">${a.action}</div>
      </div>
      <div class="audit-time">${a.time}</div>
    </div>`).join('');
}

function refreshDashboard() { renderAgentHealth(); renderRecentRFPs(); renderAuditMini(); showNotif('Dashboard refreshed!'); }

// ── RFP Table ─────────────────────────────────────────────────
let rfpData = [...RFPS];
function renderRFPTable(data) {
  const tbody = document.getElementById('rfp-table-body');
  if(!tbody) return;
  tbody.innerHTML = (data||rfpData).map(r => `
    <tr>
      <td><span class="td-id">${r.id}</span><span class="td-title">${r.title}</span></td>
      <td style="font-size:12px;color:#64748b;max-width:160px">${r.source}</td>
      <td><span class="status ${statusClass(r.status)}">${r.status}</span></td>
      <td><span class="status ${priorityClass(r.priority)}">${r.priority}</span></td>
      <td style="font-size:12px;color:#64748b">${r.dueDate}</td>
      <td class="td-value">${fmt(r.value)}</td>
      <td>
        <div class="progress-wrap" style="min-width:90px">
          <div class="progress-bar"><div class="progress-fill ${r.progress>80?'fill-green':'fill-indigo'}" style="width:${r.progress}%"></div></div>
          <span style="font-size:11px;font-weight:700;color:#64748b;min-width:28px">${r.progress}%</span>
        </div>
      </td>
      <td>
        <div style="display:flex;gap:4px">
          <button class="btn btn-outline btn-sm" onclick="viewRFP('${r.id}')" title="View"><i class="fas fa-eye"></i></button>
          ${r.status==='detected'?`<button class="btn btn-sm" style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0" onclick="processRFP('${r.id}')" title="Start"><i class="fas fa-play"></i></button>`:''}
          ${r.status==='reviewed'?`<button class="btn btn-sm" style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0" onclick="approveRFP('${r.id}')" title="Approve"><i class="fas fa-check"></i></button>`:''}
        </div>
      </td>
    </tr>`).join('');
}

function filterRFPs() {
  const s = document.getElementById('rfp-search').value.toLowerCase();
  const sf = document.getElementById('rfp-status-filter').value;
  const pf = document.getElementById('rfp-priority-filter').value;
  let f = rfpData;
  if(s) f = f.filter(r => r.title.toLowerCase().includes(s)||r.source.toLowerCase().includes(s));
  if(sf!=='all') f = f.filter(r => r.status===sf);
  if(pf!=='all') f = f.filter(r => r.priority===pf);
  renderRFPTable(f);
}

function clearRFPFilters() {
  document.getElementById('rfp-search').value='';
  document.getElementById('rfp-status-filter').value='all';
  document.getElementById('rfp-priority-filter').value='all';
  renderRFPTable(rfpData);
}

function viewRFP(id) {
  const r = rfpData.find(x=>x.id===id);
  if(!r) return;
  alert(`RFP Details\n\nID: ${r.id}\nTitle: ${r.title}\nSource: ${r.source}\nStatus: ${r.status}\nPriority: ${r.priority}\nDue: ${r.dueDate}\nValue: ${fmt(r.value)}\nProgress: ${r.progress}%\nAgent: ${r.agent}\nRequirements: ${r.requirements}\nMatches: ${r.matches}`);
}

function processRFP(id) {
  rfpData = rfpData.map(r => r.id===id ? {...r, status:'processing', progress:25} : r);
  renderRFPTable(rfpData);
  showNotif(`RFP ${id} processing started!`);
}

function approveRFP(id) {
  rfpData = rfpData.map(r => r.id===id ? {...r, status:'approved', progress:100} : r);
  renderRFPTable(rfpData);
  showNotif(`RFP ${id} approved and submitted!`);
}

function openCreateModal() { document.getElementById('create-modal').classList.add('open'); }
function closeCreateModal() { document.getElementById('create-modal').classList.remove('open'); }

function createRFP() {
  const title = document.getElementById('new-title').value.trim();
  const source = document.getElementById('new-source').value.trim();
  const priority = document.getElementById('new-priority').value;
  const dueDate = document.getElementById('new-date').value;
  const value = parseInt(document.getElementById('new-value').value)||0;
  if(!title||!source||!dueDate||!value) { alert('Please fill in all required fields.'); return; }
  const newId = 'RFP-0'+Math.floor(Math.random()*900+100);
  rfpData.unshift({ id:newId, title, source, status:'processing', priority, dueDate, value, progress:0, agent:'RFP Identification Agent', requirements:0, matches:0 });
  renderRFPTable(rfpData);
  closeCreateModal();
  showNotif(`RFP "${title}" created! Workflow started.`);
  // Simulate progress
  let p = 0;
  const interval = setInterval(() => {
    p = Math.min(p+10, 100);
    rfpData = rfpData.map(r => r.id===newId ? {...r, progress:p, status:p<100?'processing':'reviewed'} : r);
    renderRFPTable(rfpData);
    if(p>=100) clearInterval(interval);
  }, 1500);
}

// ── Agents ────────────────────────────────────────────────────
let agentData = AGENTS.map(a => ({...a}));

function renderAgents() {
  const grid = document.getElementById('agent-cards-grid');
  if(!grid) return;
  grid.innerHTML = agentData.map(a => `
    <div class="card agent-card">
      <div class="agent-accent" style="background:${a.color}"></div>
      <div class="agent-header">
        <div style="display:flex;align-items:center;gap:12px">
          <div class="agent-avatar" style="background:${a.color}">${a.name.charAt(0)}</div>
          <div>
            <div class="agent-name">${a.name}</div>
            <div class="agent-role">${a.role}</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          <i class="fas ${a.health==='healthy'?'fa-check-circle':'fa-exclamation-circle'}" style="color:${a.health==='healthy'?'#10b981':'#f59e0b'};font-size:15px"></i>
          <span class="status ${statusClass(a.status)}">${a.status}</span>
        </div>
      </div>
      <div class="agent-task">
        <div class="agent-task-label" style="color:${a.color}">Current Task</div>
        <div class="agent-task-text">${a.task}</div>
      </div>
      <div style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span style="font-size:12px;font-weight:600;color:#64748b">Efficiency</span>
          <span style="font-size:12px;font-weight:800;color:${a.color}">${a.efficiency}%</span>
        </div>
        <div class="progress-bar" style="height:6px"><div class="progress-fill" style="width:${a.efficiency}%;background:${a.color}"></div></div>
      </div>
      <div class="agent-stats">
        <div class="stat-box"><div class="stat-box-val">${a.processed}</div><div class="stat-box-lbl">Processed</div></div>
        <div class="stat-box"><div class="stat-box-val">${a.errors}</div><div class="stat-box-lbl">Errors</div></div>
        <div class="stat-box"><div class="stat-box-val">${a.avgTime}s</div><div class="stat-box-lbl">Avg Time</div></div>
        <div class="stat-box"><div class="stat-box-val">${a.uptime}</div><div class="stat-box-lbl">Uptime</div></div>
      </div>
      <div class="agent-controls">
        <div style="display:flex;align-items:center;gap:8px">
          <label class="toggle"><input type="checkbox" ${a.enabled?'checked':''} onchange="toggleAgent('${a.id}')"><span class="toggle-slider"></span></label>
          <span style="font-size:12px;color:#64748b">${a.enabled?'Enabled':'Disabled'}</span>
        </div>
        <div style="display:flex;gap:6px">
          <button class="btn btn-outline btn-sm" onclick="restartAgent('${a.id}')" title="Restart"><i class="fas fa-redo"></i></button>
          <button class="btn btn-outline btn-sm" title="Configure"><i class="fas fa-cog"></i></button>
        </div>
      </div>
    </div>`).join('');
}

function toggleAgent(id) {
  agentData = agentData.map(a => a.id===id ? {...a, enabled:!a.enabled, status:a.enabled?'stopped':'active'} : a);
  renderAgents();
  const a = agentData.find(x=>x.id===id);
  showNotif(`${a.name} ${a.enabled?'enabled':'disabled'}`);
}

function restartAgent(id) {
  agentData = agentData.map(a => a.id===id ? {...a, status:'processing', uptime:'0m'} : a);
  renderAgents();
  setTimeout(() => {
    agentData = agentData.map(a => a.id===id ? {...a, status:'active'} : a);
    renderAgents();
    showNotif('Agent restarted successfully!');
  }, 2000);
}

function refreshAgents() {
  agentData = agentData.map(a => ({...a, cpu:Math.max(5,Math.min(85,a.cpu+(Math.random()-.5)*10)), mem:Math.max(20,Math.min(90,a.mem+(Math.random()-.5)*5))}));
  renderAgents();
  showNotif('Agent data refreshed!');
}

// Live agent CPU/mem updates
setInterval(() => {
  agentData = agentData.map(a => ({...a, cpu:Math.max(5,Math.min(85,a.cpu+(Math.random()-.5)*6)), mem:Math.max(20,Math.min(90,a.mem+(Math.random()-.5)*3))}));
  if(document.getElementById('page-agents').classList.contains('active')) renderAgents();
}, 4000);

// ── Workflows ─────────────────────────────────────────────────
let selectedWF = WORKFLOWS[0];

function renderWorkflows() {
  renderWFList();
  renderWFDetail(selectedWF);
}

function renderWFList() {
  const el = document.getElementById('wf-list');
  if(!el) return;
  el.innerHTML = WORKFLOWS.map(w => `
    <div class="wf-list-item ${w.id===selectedWF.id?'active':''}" onclick="selectWF('${w.id}')">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <span style="font-size:11px;font-weight:700;color:#6366f1">${w.id}</span>
        <span class="status ${statusClass(w.status)}">${w.status}</span>
      </div>
      <div style="font-size:13px;font-weight:600;color:#0f172a;margin-bottom:8px;line-height:1.3">${w.title}</div>
      <div style="display:flex;align-items:center;gap:8px">
        <div class="progress-bar"><div class="progress-fill ${w.status==='completed'?'fill-green':'fill-indigo'}" style="width:${w.progress}%"></div></div>
        <span style="font-size:11px;font-weight:700;color:#64748b;min-width:28px">${w.progress}%</span>
      </div>
    </div>`).join('');
}

function selectWF(id) {
  selectedWF = WORKFLOWS.find(w=>w.id===id)||WORKFLOWS[0];
  renderWFList();
  renderWFDetail(selectedWF);
}

function renderWFDetail(wf) {
  const el = document.getElementById('wf-detail-panel');
  if(!el) return;
  const statusBg = {processing:'#eef2ff',completed:'#f0fdf4',error:'#fef2f2'};
  const statusCol = {processing:'#4338ca',completed:'#166534',error:'#991b1b'};
  el.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px">
      <div>
        <div style="font-size:17px;font-weight:700;color:#0f172a;margin-bottom:4px">${wf.title}</div>
        <div style="font-size:12px;color:#94a3b8">Workflow ${wf.id} · RFP ${wf.rfpId} · Started ${wf.start}</div>
      </div>
      <span class="status" style="background:${statusBg[wf.status]||'#f8fafc'};color:${statusCol[wf.status]||'#475569'}">${wf.status}</span>
    </div>
    <div style="margin-bottom:24px">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:12px;font-weight:600;color:#64748b">Overall Progress</span>
        <span style="font-size:12px;font-weight:800;color:#0f172a">${wf.progress}%</span>
      </div>
      <div class="progress-bar" style="height:8px;border-radius:4px"><div class="progress-fill ${wf.status==='completed'?'fill-green':'fill-indigo'}" style="width:${wf.progress}%;border-radius:4px"></div></div>
    </div>
    <div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:16px">Processing Timeline</div>
    ${wf.steps.map((s,i) => `
      <div class="wf-step">
        <div class="wf-connector">
          <div class="wf-dot" style="background:${stepColor(s.status)}"><i class="fas ${stepIcon(s.status)}" style="font-size:13px"></i></div>
          ${i<wf.steps.length-1?`<div class="wf-line" style="background:${i<wf.steps.findIndex(x=>x.status==='pending')?stepColor('completed'):'#e2e8f0'}"></div>`:''}
        </div>
        <div class="wf-content">
          <div class="wf-box" style="background:${stepBg(s.status)};border-color:${s.status==='processing'?'#c7d2fe':'#f1f5f9'}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
              <div class="wf-box-title">${s.name}</div>
              <div style="display:flex;gap:8px;align-items:center">
                ${s.dur?`<span style="font-size:10px;background:#f1f5f9;color:#64748b;padding:2px 8px;border-radius:6px;font-weight:600">${s.dur}</span>`:''}
                ${s.start?`<span style="font-size:11px;color:#94a3b8;font-family:monospace">${s.start}</span>`:''}
              </div>
            </div>
            <div class="wf-box-agent"><i class="fas fa-robot" style="margin-right:4px"></i>${s.agent}</div>
            <div class="wf-box-output">${s.output}</div>
            ${s.status==='processing'?`<div class="progress-bar" style="height:3px;margin-top:8px"><div class="progress-fill fill-indigo" style="width:60%;animation:none"></div></div>`:''}
          </div>
        </div>
      </div>`).join('')}
    ${wf.status==='completed'?`<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:12px 16px;margin-top:8px;color:#166534;font-size:13px;font-weight:600"><i class="fas fa-check-circle" style="margin-right:8px"></i>Workflow completed successfully with full audit trail preserved.</div>`:''}
    ${wf.status==='processing'?`<div style="background:#eef2ff;border:1px solid #c7d2fe;border-radius:10px;padding:12px 16px;margin-top:8px;color:#4338ca;font-size:13px;font-weight:600"><i class="fas fa-info-circle" style="margin-right:8px"></i>Workflow running autonomously · Est. completion: ${wf.est}</div>`:''}
  `;
}

// ── Full Audit ────────────────────────────────────────────────
function renderFullAudit() {
  const el = document.getElementById('full-audit-list');
  if(!el) return;
  el.innerHTML = AUDIT.map(a => `
    <div class="audit-item">
      <div class="audit-icon" style="background:${auditBg(a.type)};color:${auditColor(a.type)}"><i class="fas ${auditIcon(a.type)}"></i></div>
      <div style="flex:1;min-width:0">
        <div class="audit-agent">${a.agent}</div>
        <div class="audit-action">${a.action}</div>
      </div>
      <div class="audit-time">${a.time}</div>
    </div>`).join('');
}

// ── Charts ────────────────────────────────────────────────────
function initCharts() {
  // Area chart
  new Chart(document.getElementById('areaChart'), {
    type:'line',
    data:{
      labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
      datasets:[
        {label:'Autonomous',data:[8,12,9,15,11,6,4],borderColor:'#6366f1',backgroundColor:'rgba(99,102,241,0.08)',fill:true,tension:0.4,borderWidth:2.5,pointRadius:3},
        {label:'Human',data:[2,1,3,1,2,0,1],borderColor:'#f59e0b',backgroundColor:'rgba(245,158,11,0.08)',fill:true,tension:0.4,borderWidth:2.5,pointRadius:3},
      ]
    },
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:12},boxWidth:12}}},scales:{x:{grid:{color:'#f1f5f9'},ticks:{font:{size:11},color:'#94a3b8'}},y:{grid:{color:'#f1f5f9'},ticks:{font:{size:11},color:'#94a3b8'}}}}
  });
  // Pie chart
  new Chart(document.getElementById('pieChart'), {
    type:'doughnut',
    data:{labels:['Completed','Processing','Pending'],datasets:[{data:[28,12,7],backgroundColor:['#10b981','#6366f1','#f59e0b'],borderWidth:0,hoverOffset:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},cutout:'65%'}
  });
  // Bar chart
  new Chart(document.getElementById('barChart'), {
    type:'bar',
    data:{labels:['Detect','Analyze','Match','Price','Review','Submit'],datasets:[{label:'RFPs',data:[47,41,38,35,30,28],backgroundColor:'#6366f1',borderRadius:6,borderSkipped:false}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{font:{size:11},color:'#94a3b8'}},y:{grid:{color:'#f1f5f9'},ticks:{font:{size:11},color:'#94a3b8'}}}}
  });
  // Agent perf chart
  const agentPerfEl = document.getElementById('agentPerfChart');
  if(agentPerfEl) {
    new Chart(agentPerfEl, {
      type:'line',
      data:{
        labels:['00:00','04:00','08:00','12:00','16:00','20:00'],
        datasets:[
          {label:'RFP Identification',data:[8,12,15,18,14,10],borderColor:'#6366f1',fill:false,tension:0.4,borderWidth:2.5,pointRadius:3},
          {label:'Orchestrator',data:[12,15,18,20,16,12],borderColor:'#10b981',fill:false,tension:0.4,borderWidth:2.5,pointRadius:3},
          {label:'Technical Match',data:[6,8,12,15,11,8],borderColor:'#f59e0b',fill:false,tension:0.4,borderWidth:2.5,pointRadius:3},
          {label:'Pricing',data:[9,11,14,16,13,10],borderColor:'#ef4444',fill:false,tension:0.4,borderWidth:2.5,pointRadius:3},
        ]
      },
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:11},boxWidth:12}}},scales:{x:{grid:{color:'#f1f5f9'},ticks:{font:{size:11},color:'#94a3b8'}},y:{grid:{color:'#f1f5f9'},ticks:{font:{size:11},color:'#94a3b8'}}}}
    });
  }
}

// ── Init ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderAgentHealth();
  renderRecentRFPs();
  renderAuditMini();
  renderRFPTable(rfpData);
  setTimeout(initCharts, 100);
});
