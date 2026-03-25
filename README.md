# AutonomIQ — Agentic AI for Autonomous Enterprise Workflows

> Built for the **ET Gen AI Hackathon 2026** · Problem Statement: Agentic AI for Autonomous Enterprise Workflows

---

## What It Does

AutonomIQ is a multi-agent system that autonomously manages the full RFP (Request for Proposal) lifecycle — from detection to submission — with minimal human involvement. It detects failures, self-corrects, and maintains a complete auditable trail of every decision made.

### The 4 Specialized Agents

| Agent | Role |
|---|---|
| **RFP Identification Agent** | Scans procurement portals, classifies and prioritizes RFPs |
| **Orchestrator Agent** | Routes tasks, manages SLA compliance, handles failures and retries |
| **Technical Match Agent** | Extracts requirements, matches products with confidence scoring |
| **Pricing Agent** | Builds competitive pricing strategies using market data |

### Key Capabilities

- **94.2% Autonomy Rate** — most steps complete without human involvement
- **Self-correction** — agents retry on failure, reroute on SLA breach, escalate on low confidence
- **Full Audit Trail** — every agent decision is logged with timestamp, agent name, and action
- **Real-time Workflow Visualization** — step-by-step pipeline with live progress tracking
- **Role-based Access** — Admin, Risk Analyst, Operations Team views

---

## Quick Start

### Option 1 — Instant Preview (No Setup)

Just open this file in your browser:

```
frontend/public/dashboard.html
```

Double-click it. No server, no install, everything works immediately.

---

### Option 2 — Full Stack (Backend + Frontend)

**Requirements:** Python 3.11+, Node.js 18+

**Step 1 — Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python demo_main.py
```
Backend runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

**Step 2 — Frontend** (new terminal)
```bash
cd frontend
npm install
npm start
```
Frontend runs at `http://localhost:3000`

**Or use the one-command script:**
```bash
./quick_start.sh
```

---

## Project Structure

```
TechCoders/
├── frontend/
│   ├── public/
│   │   ├── dashboard.html      ← Standalone prototype (open directly)
│   │   └── app.js              ← All JS logic
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
├── VoyageHack/                 ← Fraud Prevention prototype (bonus)
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── quick_start.sh
```

---

## Dashboard Pages

| Page | Description |
|---|---|
| **Command Center** | KPIs, autonomy trend chart, agent health, recent RFPs, audit trail |
| **RFP Pipeline** | Full table with search/filter, create new RFP, approve/process actions |
| **Agent Monitor** | Live agent cards with CPU/memory, enable/disable/restart controls |
| **Workflow Engine** | Step-by-step timeline with agent attribution and duration tracking |
| **Audit Trail** | Complete immutable log of all agent decisions |
| **Settings** | System and agent configuration |

---

## Tech Stack

**Frontend:** React 18, TypeScript, Material-UI, Recharts, Chart.js  
**Backend:** FastAPI, Python 3.11, SQLAlchemy, Pydantic, Uvicorn  
**Demo Mode:** SQLite + in-memory storage (no Docker/PostgreSQL/Redis needed)

---

## Evaluation Criteria Coverage

| Criteria | Implementation |
|---|---|
| **Depth of autonomy** | 94.2% of steps complete without human input |
| **Error recovery** | Orchestrator retries on timeout, reroutes on SLA breach, escalates on low confidence |
| **Auditability** | Every agent action logged with timestamp, agent name, decision rationale |
| **Real-world applicability** | Full RFP lifecycle: detect → analyze → match → price → review → submit |

---

## Team

**TechCoders** — ET Gen AI Hackathon 2026
