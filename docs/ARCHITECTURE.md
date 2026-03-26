# AutonomIQ — System Architecture Document

**Team:** TechCoders &nbsp;|&nbsp; **Version:** 2.0 &nbsp;|&nbsp; **ET Gen AI Hackathon 2026**

---

## 1. Overview

AutonomIQ is a multi-agent AI platform that automates the complete RFP (Request for Proposal) lifecycle — from detection through submission — with a 94.2% autonomy rate. The system is built around four specialized agents coordinated by a central Orchestrator, communicating asynchronously through a message queue, and backed by a FastAPI REST layer and a real-time WebSocket feed to the dashboard.

---

## 2. Full System Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          EXTERNAL DATA SOURCES                              ║
║                                                                              ║
║   ┌─────────────────┐   ┌──────────────────────┐   ┌──────────────────┐    ║
║   │  Government     │   │  University /        │   │  Enterprise RFP  │    ║
║   │  Procurement    │   │  Research Portals    │   │  Platforms       │    ║
║   │  Portals        │   │                      │   │                  │    ║
║   └────────┬────────┘   └──────────┬───────────┘   └────────┬─────────┘    ║
╚════════════╪══════════════════════╪════════════════════════╪══════════════╝
             │  HTTP polling /      │  webhook triggers      │
             └──────────────────────┼────────────────────────┘
                                    │
                                    ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                       AGENT LAYER                                           ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                  RFP IDENTIFICATION AGENT                           │    ║
║  │                                                                     │    ║
║  │  • Scans all configured portals on a scheduled interval             │    ║
║  │  • Deduplicates against existing pipeline (hash-based check)        │    ║
║  │  • Classifies RFP by domain: IT / Infrastructure / Security / HR    │    ║
║  │  • Assigns priority score: Urgent / High / Medium / Low             │    ║
║  │  • Extracts metadata: title, source, deadline, estimated value      │    ║
║  │  • Publishes structured RFP event → Redis Queue                     │    ║
║  └──────────────────────────────┬──────────────────────────────────────┘    ║
║                                 │  RFP Event (JSON payload)                 ║
║                                 ▼                                           ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    ORCHESTRATOR AGENT                               │    ║
║  │                                                                     │    ║
║  │  • Consumes events from Redis queue                                 │    ║
║  │  • Determines workflow path based on RFP type, priority, value      │    ║
║  │  • Dispatches parallel tasks to Technical Match + Pricing agents    │    ║
║  │  • Starts SLA countdown timer per RFP deadline                      │    ║
║  │  • Monitors agent heartbeats every 30 seconds                       │    ║
║  │  • On SLA breach prediction → reroutes to fast-track path           │    ║
║  │  • On retry exhaustion → escalates to Human Review queue            │    ║
║  │  • Writes every routing decision to Audit Log                       │    ║
║  └──────────┬──────────────────────────────────────┬────────────────────    ║
║             │ Task dispatch                         │ Task dispatch         ║
║             ▼                                       ▼                       ║
║  ┌──────────────────────────┐         ┌──────────────────────────────┐      ║
║  │  TECHNICAL MATCH AGENT   │         │      PRICING AGENT           │      ║
║  │                          │         │                              │      ║
║  │  • Receives RFP document │         │  • Receives matched product  │      ║
║  │  • Runs NLP pipeline to  │         │    list + confidence scores  │      ║
║  │    extract requirements  │         │  • Queries live market data  │      ║
║  │  • Scores each product   │         │    feed for competitor rates │      ║
║  │    in catalog (0–100%)   │         │  • Applies cost + margin     │      ║
║  │  • Returns top N matches │         │    model to build bid        │      ║
║  │    with confidence score │         │  • Flags bids outside budget │      ║
║  │  • Escalates if best     │         │  • Returns final pricing     │      ║
║  │    match < 70% confidence│         │    strategy to Orchestrator  │      ║
║  └──────────┬───────────────┘         └──────────────┬───────────────┘      ║
║             │ Match results                           │ Pricing output       ║
║             └──────────────────┬────────────────────-┘                      ║
║                                │ Combined proposal package                  ║
║                                ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                     DECISION GATE                                   │    ║
║  │                                                                     │    ║
║  │   Confidence ≥ 70%  AND  Value < $500K  AND  No SLA risk            │    ║
║  │          │                                        │                 │    ║
║  │          ▼ YES                                    ▼ NO              │    ║
║  │   AUTO-SUBMIT                            HUMAN REVIEW QUEUE         │    ║
║  │   (fully autonomous)                     • Low confidence           │    ║
║  │                                          • High-value deal          │    ║
║  │                                          • SLA breach risk          │    ║
║  └──────────────────────────────────────────────────────────────────────    ║
╚══════════════════════════════════════════════════════════════════════════════╝
             │
             ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                     INFRASTRUCTURE LAYER                                    ║
║                                                                              ║
║   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────┐  ║
║   │  PostgreSQL  │   │    Redis     │   │   FastAPI    │   │  Audit Log │  ║
║   │  (RFPs,      │   │  (Message    │   │  REST API    │   │  (append-  │  ║
║   │  Workflows,  │   │   Queue +    │   │  + WebSocket │   │   only,    │  ║
║   │  Audit)      │   │   Cache)     │   │  /docs UI)   │   │  immutable)│  ║
║   └──────────────┘   └──────────────┘   └──────────────┘   └────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════════╝
             │
             ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                       FRONTEND LAYER                                        ║
║                                                                              ║
║   login.html                    dashboard.html + app.js                     ║
║   ┌─────────────────────┐       ┌──────────────────────────────────────┐    ║
║   │ • Split-panel UI    │  ───► │ • Auth guard (localStorage session)  │    ║
║   │ • Sign In / Sign Up │       │ • Command Center (KPIs + charts)     │    ║
║   │ • Phone number      │       │ • RFP Pipeline (table + filters)     │    ║
║   │ • Location field    │       │ • Agent Monitor (live cards)         │    ║
║   │ • GPS geolocation   │       │ • Workflow Engine (live countdown)   │    ║
║   │   popup + reverse   │       │ • Audit Trail (live feed + search)   │    ║
║   │   geocoding         │       │ • My Profile (user data from login)  │    ║
║   └─────────────────────┘       └──────────────────────────────────────┘    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Agent Communication Flow

```
  RFP Identification          Orchestrator           Technical Match        Pricing
        │                          │                        │                  │
        │── RFP Event (Redis) ────►│                        │                  │
        │                          │── dispatch task ──────►│                  │
        │                          │── dispatch task ───────────────────────►  │
        │                          │                        │                  │
        │                          │◄── match results ──────│                  │
        │                          │◄── pricing output ─────────────────────── │
        │                          │                        │                  │
        │                          │── assemble proposal    │                  │
        │                          │── decision gate        │                  │
        │                          │     ├─ auto-submit     │                  │
        │                          │     └─ human review    │                  │
        │                          │── write audit log      │                  │
```

---

## 4. Error Handling & Self-Correction

```
  Agent Action
       │
       ├──► Transient failure (timeout / network drop)?
       │         └──► Retry 1 ──► Retry 2 ──► Retry 3
       │                   └── Success: continue workflow
       │                   └── All failed: escalate to Orchestrator
       │
       ├──► Confidence score < 70%?
       │         └──► Flag step → route to Human Review queue
       │              Notify reviewer via email/in-app alert
       │
       ├──► SLA breach predicted (< 2h remaining)?
       │         └──► Orchestrator reroutes to fast-track path
       │              Bumps priority → notifies human reviewer
       │
       └──► Unrecoverable / unknown error?
                 └──► Mark workflow status = ERROR
                      Log full stack trace to audit trail
                      Trigger on-call notification
                      Preserve all intermediate outputs for replay
```

---

## 5. Data Flow Summary

```
  [Portal Scan]
       │
       ▼
  [RFP Detected] ──► Deduplicate ──► Classify ──► Prioritize
       │
       ▼
  [Orchestrator] ──► Start SLA timer ──► Dispatch tasks
       │
       ├──► [Technical Match] ──► Extract requirements ──► Score products
       │
       └──► [Pricing Agent]   ──► Query market data ──► Build bid
       │
       ▼
  [Decision Gate]
       ├──► Auto-submit (high confidence, low value)
       └──► Human Review (low confidence / high value / SLA risk)
                 │
                 ▼
           [Approve / Reject]
                 │
                 ▼
           [Submit / Archive] ──► [Audit Record Written]
```

---

## 6. Key Design Decisions

| Decision | Rationale |
|---|---|
| Async queue (Redis) over direct agent calls | Agents are fully decoupled — one slow agent never blocks others |
| Confidence threshold gate (70%) | Prevents low-quality outputs from reaching clients without human review |
| SLA-aware proactive rerouting | Orchestrator acts before a breach happens, not after |
| Append-only audit log | No agent can modify or delete past entries — full traceability guaranteed |
| Demo mode (in-memory fallback) | Full system runs without Docker, PostgreSQL, or Redis for instant preview |
| localStorage auth (frontend) | Zero-dependency prototype — works as a static file with no server |
| GPS reverse geocoding (Nominatim) | Free, open-source, no API key required — city/country from coordinates |
