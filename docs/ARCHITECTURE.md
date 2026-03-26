# AutonomIQ — Architecture Document

Team: TechCoders  
Version: 2.0 · ET Gen AI Hackathon 2026

---

## System Overview

AutonomIQ is a multi-agent orchestration platform that automates the end-to-end RFP (Request for Proposal) lifecycle. Four specialized AI agents collaborate through a central Orchestrator, each owning a distinct stage of the pipeline. The system operates autonomously at a 94%+ rate, with structured escalation paths for edge cases.

The frontend is a standalone static prototype (`login.html` → `dashboard.html`) that runs entirely in the browser using `localStorage` for auth and in-memory state for live simulation. A FastAPI backend (`demo_main.py`) provides the full API layer when connected.

---

## Agent Roles

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SOURCES                         │
│   Gov Portals · University Procurement · Enterprise RFP Feeds   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP polling / webhook
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               RFP IDENTIFICATION AGENT                          │
│  • Scans procurement portals on a configurable schedule         │
│  • Classifies RFPs by domain, urgency, and estimated value      │
│  • Assigns priority: Urgent / High / Medium / Low               │
│  • Deduplicates against existing pipeline                       │
└────────────────────────────┬────────────────────────────────────┘
                             │ Publishes RFP event to queue
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                           │
│  • Consumes RFP events from Redis queue                         │
│  • Determines workflow path based on RFP type and priority      │
│  • Dispatches tasks to Technical Match and Pricing agents       │
│  • Tracks SLA timers — escalates if breach is predicted         │
│  • Manages retries (max 3) with exponential back-off            │
│  • Routes low-confidence results to Human Review queue          │
└──────────┬──────────────────────────────────────┬───────────────┘
           │ task dispatch                         │ task dispatch
           ▼                                       ▼
┌──────────────────────────┐         ┌─────────────────────────────┐
│  TECHNICAL MATCH AGENT   │         │      PRICING AGENT          │
│  • Parses RFP documents  │         │  • Receives matched product  │
│  • Extracts structured   │         │    list from Technical Match │
│    requirements via NLP  │         │  • Queries market data feed  │
│  • Scores each product   │         │  • Builds competitive bid    │
│    in catalog (0–100%)   │         │    using cost + margin model │
│  • Returns top matches   │         │  • Flags bids outside SLA    │
│    with confidence score │         │    budget thresholds         │
└──────────┬───────────────┘         └──────────────┬──────────────┘
           │ match results                           │ pricing output
           └──────────────────┬──────────────────────┘
                              │ combined result
                              ▼
                   ┌──────────────────────┐
                   │    HUMAN REVIEW      │
                   │  (only when needed)  │
                   │  • Confidence < 70%  │
                   │  • Value > $500K     │
                   │  • SLA breach risk   │
                   └──────────┬───────────┘
                              │ approved / rejected
                              ▼
                   ┌──────────────────────┐
                   │   SUBMISSION &       │
                   │   AUDIT LOGGER       │
                   │  • Submits proposal  │
                   │  • Writes immutable  │
                   │    audit record      │
                   └──────────────────────┘
```

---

## Communication Model

| Channel | Used For |
|---|---|
| Redis Pub/Sub queue | Agent-to-agent task handoff (async, decoupled) |
| REST API (FastAPI) | Frontend ↔ backend data fetch and action triggers |
| WebSocket | Real-time dashboard updates (agent status, workflow progress) |
| PostgreSQL | Persistent storage for RFPs, workflows, audit records |
| localStorage (browser) | Auth session and user profile in prototype mode |
| In-memory state (JS) | Live agent simulation, workflow ticking, audit feed |

Agents do not call each other directly. All communication flows through the Orchestrator or the shared queue. This keeps agents independently deployable and testable.

---

## Frontend Architecture

```
login.html
  └── Sign In / Create Account (split-panel UI)
        • Phone number field with country code prefix
        • Location field with GPS geolocation popup
        • Reverse geocoding via OpenStreetMap Nominatim
        • Stores user object in localStorage on signup/login
        └── Redirects to dashboard.html on success

dashboard.html
  └── Auth guard — redirects to login.html if no session
        • Injects user name, initials, role, email,
          phone, location into navbar and profile page
        • Sign Out clears session → back to login.html
        └── Loads app.js for all live functionality

app.js
  ├── Live Audit Trail
  │     • Starts with 10 seed entries
  │     • Injects new entry every 6 seconds from a pool
  │     • Search filter (agent name / action text)
  │     • Severity filter (High / Medium / Low)
  │     • NEW badge + slide-in animation on fresh entries
  │     • Dashboard mini-audit also updates live
  └── Live Workflow Engine (WF-001)
        • Est. completion countdown (HH:MM:SS, ticks every 1s)
        • Overall progress bar animates upward every 3s
        • Active step progress bar ticks forward
        • Elapsed time counter updates per tick
        • Step output text updates (e.g. 6/8 → 7/8 → 8/8)
        • Sidebar workflow list progress syncs in real time
```

---

## Tool Integrations

| Integration | Agent | Purpose |
|---|---|---|
| Procurement portal scrapers | RFP Identification | Detect new RFPs from Gov/University/Enterprise feeds |
| NLP requirement extractor | Technical Match | Parse unstructured RFP text into structured requirements |
| Product catalog API | Technical Match | Match requirements against internal product database |
| Market data feed | Pricing | Pull competitor pricing signals for bid calibration |
| Email / notification service | Orchestrator | Alert human reviewers when escalation is triggered |
| Audit log writer | All agents | Append every decision to the immutable audit trail |
| OpenStreetMap Nominatim | Frontend (login) | Reverse geocode GPS coordinates to city/country |

---

## Error Handling Logic

```
Agent Action Fails
       │
       ├─► Transient error (timeout, network)?
       │         └─► Retry up to 3× with exponential back-off
       │                   ├─► Success → continue workflow
       │                   └─► All retries exhausted → escalate to Orchestrator
       │
       ├─► Low confidence score (< 70%)?
       │         └─► Flag step, route to Human Review queue
       │
       ├─► SLA breach predicted?
       │         └─► Orchestrator reroutes to fast-track path,
       │             notifies human reviewer immediately
       │
       └─► Unrecoverable error?
                 └─► Mark workflow as ERROR, log full trace to audit,
                     notify on-call via notification service
```

Every error event — including retries and escalations — is written to the audit trail with agent name, timestamp, error type, and resolution action.

---

## Data Flow Summary

```
Portal Scan → RFP Detected → Classified & Queued
    → Orchestrator picks up → Dispatches to Technical Match
    → Requirements extracted → Products matched (confidence scored)
    → Pricing Agent builds bid → Orchestrator assembles proposal
    → If confidence ≥ 70% and value < $500K → Auto-submit
    → Else → Human Review → Approve/Reject → Submit/Archive
    → Audit record written at every step
```

---

## Key Design Decisions

- Async queue over direct calls — agents are decoupled; one slow agent doesn't block others
- Confidence thresholds — prevents low-quality outputs from reaching clients without review
- SLA-aware routing — Orchestrator monitors deadlines and reroutes proactively, not reactively
- Immutable audit log — append-only; no agent can modify or delete past entries
- Live frontend simulation — audit trail and workflow engine tick in real time without a backend connection
- Demo mode — full system runs without Docker, PostgreSQL, or Redis using in-memory fallbacks
