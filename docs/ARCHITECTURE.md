# AutonomIQ — System Architecture Document

**Team:** TechCoders &nbsp;|&nbsp; **Version:** 2.0 &nbsp;|&nbsp; **ET Gen AI Hackathon 2026**

---

# Overview

AutonomIQ is a multi-agent AI platform that automates the complete RFP (Request for Proposal) lifecycle — from detection through submission — with a 94.2% autonomy rate. The system is built around four specialized agents coordinated by a central Orchestrator, communicating asynchronously through a message queue, and backed by a FastAPI REST layer and a real-time WebSocket feed to the dashboard.

---

## 1. Full System Architecture Diagram

```╔════════════════════════════════════════════════════════════════════════════╗
║                         🌐 EXTERNAL DATA SOURCES                           ║
║  Govt Portals | University Portals | Enterprise RFP Systems               ║
╚═══════════════════════════════╤════════════════════════════════════════════╝
                                │ (Polling / Webhooks)
                                ▼
╔════════════════════════════════════════════════════════════════════════════╗
║                  🔍 RFP IDENTIFICATION AGENT                               ║
║  • Scan portals                                                            ║
║  • Deduplicate (hash check)                                                ║
║  • Classify + Priority                                                     ║
║  • Extract metadata                                                        ║
║                                                                            ║
║  OUTPUT → RFP Event (JSON)                                                 ║
╚═══════════════════════════════╤════════════════════════════════════════════╝
                                │
                                ▼
                     ⚡ REDIS MESSAGE QUEUE (ASYNC)
                                │
                                ▼
╔════════════════════════════════════════════════════════════════════════════╗
║                    🧠 ORCHESTRATOR AGENT                                   ║
║  • Consumes RFP events                                                     ║
║  • Decides workflow path                                                   ║
║  • Starts SLA timer                                                        ║
║  • Dispatches parallel tasks                                               ║
║  • Monitors agent health (heartbeat)                                       ║
║                                                                            ║
║  ERROR CONTROL:                                                            ║
║   - Retry (3x)                                                             ║
║   - SLA breach → Fast-track                                                ║
║   - Failure → Human escalation                                             ║
╚═══════════════╤═══════════════════════════════════════╤════════════════════╝
                │                                       │
     (Parallel Tasks)                         (Parallel Tasks)
                ▼                                       ▼

╔══════════════════════════╗               ╔══════════════════════════════╗
║ 🧪 TECHNICAL MATCH AGENT ║               ║ 💰 PRICING AGENT            ║
║                          ║               ║                              ║
║ • NLP requirement extract║               ║ • Market price lookup        ║
║ • Product matching       ║               ║ • Cost + margin model        ║
║ • Confidence scoring     ║               ║ • Budget validation          ║
║                          ║               ║                              ║
║ OUTPUT:                  ║               ║ OUTPUT:                      ║
║ Match list + confidence  ║               ║ Pricing strategy             ║
║                          ║               ║                              ║
║ ERROR:                   ║               ║ ERROR:                       ║
║ <70% → flag              ║               ║ Invalid → flag               ║
╚══════════════╤═══════════╝               ╚══════════════╤═══════════════╝
               └───────────────┬─────────────────────────┘
                               ▼
╔════════════════════════════════════════════════════════════════════════════╗
║                        🚦 DECISION GATE                                    ║
║                                                                            ║
║  Condition Check:                                                          ║
║   ✔ Confidence ≥ 70%                                                       ║
║   ✔ Value < $500K                                                          ║
║   ✔ No SLA Risk                                                            ║
║                                                                            ║
║        YES ✅                              NO ❌                            ║
║        ▼                                   ▼                               ║
║  🤖 AUTO SUBMIT                   👤 HUMAN REVIEW QUEUE                    ║
║                                   • Low confidence                        ║
║                                   • High value                            ║
║                                   • SLA risk                              ║
╚═══════════════════════════════╤════════════════════════════════════════════╝
                                │
                                ▼
╔════════════════════════════════════════════════════════════════════════════╗
║                    🏗 INFRASTRUCTURE & TOOLS                               ║
║                                                                            ║
║  🗄 PostgreSQL  → RFPs, workflows, audit logs                              ║
║  ⚡ Redis       → Message queue + cache                                     ║
║  🚀 FastAPI    → REST APIs + WebSocket                                     ║
║  📜 Audit Log  → Append-only (immutable tracking)                          ║
║                                                                            ║
║  🌍 External Tool:                                                         ║
║   • Nominatim API → Reverse geolocation (frontend)                         ║
╚═══════════════════════════════╤════════════════════════════════════════════╝
                                │
                                ▼
╔════════════════════════════════════════════════════════════════════════════╗
║                      🖥 FRONTEND DASHBOARD                                 ║
║                                                                            ║
║  • Real-time updates (WebSocket)                                           ║
║  • RFP Pipeline view                                                       ║
║  • Agent monitoring                                                        ║
║  • Workflow countdown timers                                               ║
║  • Human review modal                                                      ║
║  • Audit trail (live feed)                                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

## 2. Agent Communication Flow

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



## 3. Agent Roles

### 3.1 RFP Identification Agent
- Scans external portals for new RFPs  
- Removes duplicates using hashing  
- Classifies domain and assigns priority  
- Extracts structured metadata  
- Publishes events to Redis queue  

---

### 3.2 Orchestrator Agent
- Central decision-making unit  
- Consumes events from Redis  
- Dispatches tasks to agents in parallel  
- Tracks SLA deadlines  
- Handles retries, failures, and escalations  
- Logs all actions in audit system  

---

### 3.3 Technical Match Agent
- Processes RFP documents using NLP  
- Extracts requirements  
- Matches with internal catalog  
- Produces confidence score  
- Flags low-confidence results  

---

### 3.4 Pricing Agent
- Uses matched products as input  
- Fetches market pricing data  
- Applies cost + margin model  
- Generates optimized bid  

---

### 3.5 Decision Gate
- Evaluates final proposal based on:
  - Confidence score  
  - Deal value  
  - SLA risk  

**Outcomes:**
- Auto-submit (high confidence, low risk)  
- Human review (low confidence or high risk)  

---

## 4. Communication Flow

The system follows an **event-driven asynchronous architecture**:

1. RFP detected → published to Redis  
2. Orchestrator consumes event  
3. Tasks dispatched in parallel:
   - Technical Match Agent  
   - Pricing Agent  
4. Outputs returned to Orchestrator  
5. Proposal assembled  
6. Decision Gate executed  
7. Final action (submit / review)  
8. Audit log updated  

---

## 5. Tool Integrations

| Tool        | Purpose |
|-------------|--------|
| Redis       | Message queue & caching |
| PostgreSQL  | Data storage (RFPs, workflows, logs) |
| FastAPI     | REST APIs & WebSocket |
| WebSocket   | Real-time frontend updates |
| Audit Log   | Immutable tracking system |
| Nominatim   | Reverse geolocation (frontend) |

---

## 6. Error Handling & Resilience

### 6.1 Retry Mechanism
- Up to 3 retries for transient failures  
- Covers network issues and timeouts  

### 6.2 Confidence-Based Validation
- Confidence < 70% → routed to human review  

### 6.3 SLA Monitoring
- Tracks deadlines continuously  
- If breach risk detected:
  - Workflow is fast-tracked  
  - Priority increased  

### 6.4 Failure Handling
- Unrecoverable errors:
  - Workflow marked as ERROR  
  - Full trace logged  
  - Alerts triggered  
  - State preserved for replay  

---

## 7. Key Design Principles

- **Asynchronous Processing:** Ensures scalability and decoupling  
- **Parallel Execution:** Reduces processing time  
- **Self-Healing System:** Automatic retries and rerouting  
- **Human-in-the-Loop:** Ensures quality control  
- **Auditability:** Full traceability via immutable logs  

---

## 8. Summary

AutonomIQ is a scalable, resilient, and intelligent multi-agent system that automates the RFP lifecycle using:

- Event-driven architecture  
- Parallel agent execution  
- SLA-aware orchestration  
- Robust error handling  
- Real-time monitoring  

This design ensures high efficiency, reliability, and production readiness.

---
