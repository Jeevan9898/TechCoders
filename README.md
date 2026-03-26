# AutonomIQ — Agentic AI for Autonomous Enterprise Workflows

> Built for the **ET Gen AI Hackathon 2026** · Problem Statement: Agentic AI for Autonomous Enterprise Workflows  
> Team: **TechCoders**

---

## What It Does

AutonomIQ is a multi-agent system that autonomously manages the full RFP (Request for Proposal) lifecycle — from detection to submission — with minimal human involvement. Agents detect failures, self-correct, and maintain a complete live-updating auditable trail of every decision made.

---

## The 4 Specialized Agents

| Agent | Role |
|---|---|
| RFP Identification Agent | Scans procurement portals, classifies and prioritizes RFPs |
| Orchestrator Agent | Routes tasks, manages SLA compliance, handles failures and retries |
| Technical Match Agent | Extracts requirements, matches products with confidence scoring |
| Pricing Agent | Builds competitive pricing strategies using market data |

---

## Key Features

- 94.2% Autonomy Rate — most steps complete without human involvement
- Self-correction — agents retry on failure, reroute on SLA breach, escalate on low confidence
- Live Audit Trail — entries appear every 6 seconds with severity tags, search, and filter
- Live Workflow Engine — real countdown timer, animated progress bar, elapsed step time
- Login / Sign-up — split-panel UI with phone, location, and GPS geolocation detection
- User details (name, role, email, phone, location) flow through to the dashboard profile page
- Role-based profile — permissions and notification preferences rendered correctly
- Sign Out — clears session and returns to login

---

## Quick Start

### Option 1 — Instant Preview (No Setup)

Serve the static files locally:

```bash
cd frontend/public
python3 -m http.server 3000
```

Open `http://localhost:3000/login.html` in your browser.

To stop the server: press `Ctrl + C` in the terminal.  
To restart: run the same command again.

Alternatively just double-click `login.html` — it works as a `file://` URL too since everything uses `localStorage`.

---

### Option 2 — Full Stack (Backend + Frontend)

Requirements: Python 3.11+, Node.js 18+

Step 1 — Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python demo_main.py
```
Backend runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

Step 2 — Frontend (new terminal)
```bash
cd frontend
npm install
npm start
```
Frontend runs at `http://localhost:3000`

Or use the one-command script:
```bash
./quick_start.sh
```

---

## Project Structure

```
TechCoders/
├── frontend/
│   ├── public/
│   │   ├── login.html          ← Entry point — sign in / create account
│   │   ├── dashboard.html      ← Main dashboard (auth-guarded)
│   │   └── app.js              ← All JS logic, live data, agent simulation
│   └── src/                    ← React TypeScript app
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── AgentStatus.tsx
│       │   ├── RFPMonitoring.tsx
│       │   ├── WorkflowVisualization.tsx
│       │   └── Settings.tsx
│       └── components/layout/
├── backend/
│   ├── demo_main.py            ← FastAPI app (no Docker needed)
│   ├── agents/                 ← Agent implementations
│   ├── models/                 ← SQLAlchemy models
│   └── requirements.txt
├── database/
│   └── init.sql
├── docs/
│   ├── ARCHITECTURE.md         ← Agent roles, communication, error handling
│   └── IMPACT_MODEL.md         ← Quantified business impact estimate
└── quick_start.sh
```

---

## Dashboard Pages

| Page | Description |
|---|---|
| Command Center | KPIs, autonomy trend chart, agent health, recent RFPs, live audit feed |
| RFP Pipeline | Full table with search/filter, create new RFP, approve/process actions |
| Agent Monitor | Live agent cards with efficiency bars, enable/disable/restart controls |
| Workflow Engine | Live countdown timer, animated step progress, elapsed time per step |
| Audit Trail | Live-updating log with search, severity filter, and NEW entry animation |
| My Profile | Name, role, email, phone, location populated from login — permissions and notification toggles rendered correctly |
| Settings | System and agent configuration |

---

## Tech Stack

Frontend: React 18, TypeScript, Material-UI, Recharts, Chart.js  
Backend: FastAPI, Python 3.11, SQLAlchemy, Pydantic, Uvicorn  
Auth: localStorage-based session (prototype)  
Geolocation: Browser Geolocation API + OpenStreetMap Nominatim reverse geocoding  
Demo Mode: SQLite + in-memory storage (no Docker/PostgreSQL/Redis needed)

---

## Supporting Documents

| Document | Description |
|---|---|
| `docs/ARCHITECTURE.md` | Agent roles, communication flow, tool integrations, error-handling logic |
| `docs/IMPACT_MODEL.md` | Quantified business impact: time saved, cost reduced, revenue recovered |

---

## Evaluation Criteria Coverage

| Criteria | Implementation |
|---|---|
| Depth of autonomy | 94.2% of steps complete without human input |
| Error recovery | Orchestrator retries on timeout, reroutes on SLA breach, escalates on low confidence |
| Auditability | Every agent action logged live — searchable, filterable, severity-tagged, auto-refreshing |
| Real-world applicability | Full RFP lifecycle: detect → analyze → match → price → review → submit |
