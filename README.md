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
- Human Review modal — shows proposal summary, all agent outputs, reviewer notes, approve/reject
- New RFP creates a live workflow — all 5 steps run automatically, review modal fires on completion
- Live Audit Trail — new entries every 6 seconds, searchable, severity-filtered, animated
- Live Workflow Engine — countdown timer, animated progress, elapsed step time, step-by-step updates
- Dark / Light mode toggle — moon/sun button in navbar, preference saved across sessions
- Dynamic scrolling — progress bar, parallax header, navbar shrink, scroll-reveal on cards
- Highlighted cards — indigo glow borders and layered shadows in both light and dark mode
- Login / Sign-up — split-panel UI with phone, location field, GPS geolocation popup
- User details (name, role, email, phone, location) populate dashboard and profile page
- Sign Out — clears session and returns to login

---

## Quick Start

### Option 1 — Instant Preview (No Setup)

```bash
cd frontend/public
python3 -m http.server 3000
```

Open `http://localhost:3000/login.html` in your browser.

To stop: `Ctrl + C` — To restart: run the same command again.

Or just double-click `login.html` — works as a `file://` URL since everything uses `localStorage`.

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
Backend: `http://localhost:8000` · API docs: `http://localhost:8000/docs`

Step 2 — Frontend (new terminal)
```bash
cd frontend
npm install
npm start
```
Frontend: `http://localhost:3000`

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
├── backend/
│   ├── demo_main.py            ← FastAPI app (no Docker needed)
│   ├── agents/
│   ├── models/
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
| RFP Pipeline | Table with search/filter, create RFP, approve (opens review modal), reject |
| Agent Monitor | Live agent cards with efficiency bars, enable/disable/restart |
| Workflow Engine | Live countdown, animated step progress, elapsed time, step outputs |
| Audit Trail | Live-updating log, search, severity filter, NEW badge animation |
| My Profile | Name, role, email, phone, location from login — permissions and notifications |
| Settings | System and agent configuration |

---

## Human Review Flow

When all agent steps complete on a new RFP, a **Human Review modal** automatically opens showing:
- Full proposal summary (title, source, priority, value, due date)
- Every agent step output (what was detected, matched, priced)
- A notes field for reviewer comments
- **Approve & Submit** → workflow completes, RFP marked approved, audit logged
- **Reject** → workflow archived, RFP marked rejected, audit logged

The same modal is accessible from the RFP Pipeline table via the review button on any `reviewed` RFP.

---

## Tech Stack

Frontend: React 18, TypeScript, Material-UI, Recharts, Chart.js
Backend: FastAPI, Python 3.11, SQLAlchemy, Pydantic, Uvicorn
Auth: localStorage-based session (prototype)
Geolocation: Browser Geolocation API + OpenStreetMap Nominatim
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
| Auditability | Every agent action logged live — searchable, filterable, severity-tagged |
| Human-in-the-loop | Review modal with full proposal context, notes, approve/reject — completes the workflow |
| Real-world applicability | Full RFP lifecycle: detect → analyze → match → price → human review → submit |
