"""
Multi-Agent RFP System - Demo Version

This is a simplified version that runs without external dependencies
for immediate demonstration purposes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import structlog
from datetime import datetime, timedelta
import uuid
import random

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Multi-Agent RFP Automation System (Demo)",
    description="Intelligent platform for automated RFP response generation using specialized AI agents",
    version="1.0.0-demo",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for demo (in production, this would be a database)
import asyncio
import threading
import time

# Mock data for demo
mock_rfps = [
    {
        "id": str(uuid.uuid4()),
        "title": "Enterprise Software Modernization Initiative",
        "source": "Government Technology Portal",
        "status": "processing",
        "priority": "high",
        "dueDate": "2024-01-15",
        "projectValue": 500000,
        "progress": 65,
        "detectedAt": "2024-01-01T10:00:00Z",
        "requirements": 8,
        "matches": 12,
        "agent": "Technical Match Agent"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "High-Performance Computing Infrastructure",
        "source": "Research University Procurement",
        "status": "matched",
        "priority": "urgent",
        "dueDate": "2024-01-10",
        "projectValue": 750000,
        "progress": 85,
        "detectedAt": "2024-01-01T08:30:00Z",
        "requirements": 6,
        "matches": 8,
        "agent": "Pricing Agent"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Cybersecurity Assessment and Implementation",
        "source": "City Government Portal",
        "status": "priced",
        "priority": "high",
        "dueDate": "2024-01-20",
        "projectValue": 300000,
        "progress": 90,
        "detectedAt": "2024-01-01T14:15:00Z",
        "requirements": 10,
        "matches": 15,
        "agent": "Orchestrator Agent"
    },
    {
        "id": str(uuid.uuid4()),
        "title": "IT Staff Training and Certification Program",
        "source": "Corporate Procurement Portal",
        "status": "reviewed",
        "priority": "medium",
        "dueDate": "2024-01-25",
        "projectValue": 150000,
        "progress": 95,
        "detectedAt": "2024-01-01T16:45:00Z",
        "requirements": 5,
        "matches": 6,
        "agent": "Human Review"
    }
]

mock_agents = [
    {
        "id": "rfp-identification",
        "name": "RFP Identification Agent",
        "type": "rfp_identification",
        "status": "active",
        "health": "healthy",
        "uptime": "2d 14h 32m",
        "processed": 156,
        "efficiency": 94,
        "currentTask": "Scanning Government Contracts Portal",
        "lastActivity": "2 minutes ago"
    },
    {
        "id": "orchestrator",
        "name": "Orchestrator Agent",
        "type": "orchestrator",
        "status": "active",
        "health": "healthy",
        "uptime": "2d 14h 32m",
        "processed": 89,
        "efficiency": 98,
        "currentTask": "Coordinating RFP workflow #RF-2024-001",
        "lastActivity": "30 seconds ago"
    },
    {
        "id": "technical-match",
        "name": "Technical Match Agent",
        "type": "technical_match",
        "status": "processing",
        "health": "healthy",
        "uptime": "2d 14h 32m",
        "processed": 78,
        "efficiency": 91,
        "currentTask": "Analyzing requirements for Enterprise Software RFP",
        "lastActivity": "1 minute ago"
    },
    {
        "id": "pricing",
        "name": "Pricing Agent",
        "type": "pricing",
        "status": "idle",
        "health": "warning",
        "uptime": "2d 14h 32m",
        "processed": 67,
        "efficiency": 89,
        "currentTask": "Waiting for market data update",
        "lastActivity": "5 minutes ago"
    }
]

# Global storage for workflows
mock_workflows = {}

# Request models
class CreateRFPRequest(BaseModel):
    title: str
    source: str
    priority: str = "medium"
    dueDate: str
    projectValue: int
    description: str = ""

# Workflow simulation function
def simulate_workflow_progress(rfp_id: str, workflow_id: str):
    """Simulate the workflow progress for a new RFP"""
    steps = [
        {"name": "RFP Detection", "agent": "RFP Identification Agent", "duration": 15},
        {"name": "Workflow Orchestration", "agent": "Orchestrator Agent", "duration": 5},
        {"name": "Technical Analysis", "agent": "Technical Match Agent", "duration": 120},
        {"name": "Pricing Analysis", "agent": "Pricing Agent", "duration": 90},
        {"name": "Human Review", "agent": "Human Reviewer", "duration": 60}
    ]
    
    current_time = datetime.utcnow()
    
    # Initialize workflow
    workflow = {
        "id": workflow_id,
        "rfpId": rfp_id,
        "rfpTitle": next((r["title"] for r in mock_rfps if r["id"] == rfp_id), "New RFP"),
        "status": "processing",
        "progress": 0,
        "startTime": current_time.isoformat() + "Z",
        "estimatedCompletion": (current_time + timedelta(minutes=sum(s["duration"] for s in steps))).isoformat() + "Z",
        "currentStep": 0,
        "steps": []
    }
    
    # Initialize steps
    for i, step_info in enumerate(steps):
        step = {
            "id": f"step_{i}",
            "name": step_info["name"],
            "agent": step_info["agent"],
            "status": "pending" if i > 0 else "processing",
            "startTime": current_time.isoformat() + "Z" if i == 0 else None,
            "endTime": None,
            "duration": None,
            "output": f"Starting {step_info['name'].lower()}..." if i == 0 else f"Waiting for {steps[i-1]['name'].lower()} completion"
        }
        workflow["steps"].append(step)
    
    mock_workflows[workflow_id] = workflow
    
    # Simulate progress in background
    def progress_simulation():
        for i, step_info in enumerate(steps):
            # Update current step
            workflow["currentStep"] = i
            workflow["steps"][i]["status"] = "processing"
            workflow["steps"][i]["startTime"] = datetime.utcnow().isoformat() + "Z"
            workflow["steps"][i]["output"] = f"Processing {step_info['name'].lower()}..."
            
            # Update RFP progress
            progress = int((i + 0.5) / len(steps) * 100)
            workflow["progress"] = progress
            
            # Update RFP in mock_rfps
            for rfp in mock_rfps:
                if rfp["id"] == rfp_id:
                    rfp["progress"] = progress
                    rfp["status"] = "processing" if i < len(steps) - 1 else "reviewed"
                    break
            
            # Simulate processing time (reduced for demo)
            time.sleep(step_info["duration"] / 10)  # 10x faster for demo
            
            # Complete current step
            workflow["steps"][i]["status"] = "completed"
            workflow["steps"][i]["endTime"] = datetime.utcnow().isoformat() + "Z"
            workflow["steps"][i]["duration"] = step_info["duration"]
            workflow["steps"][i]["output"] = f"{step_info['name']} completed successfully"
            
            # Start next step if exists
            if i < len(steps) - 1:
                workflow["steps"][i + 1]["status"] = "pending"
                workflow["steps"][i + 1]["output"] = f"Ready to start {steps[i + 1]['name'].lower()}"
        
        # Mark workflow as completed
        workflow["status"] = "completed"
        workflow["progress"] = 100
        workflow["currentStep"] = len(steps) - 1
        
        # Update final RFP status
        for rfp in mock_rfps:
            if rfp["id"] == rfp_id:
                rfp["progress"] = 100
                rfp["status"] = "reviewed"
                rfp["agent"] = "Human Review"
                break
    
    # Start simulation in background thread
    thread = threading.Thread(target=progress_simulation)
    thread.daemon = True
    thread.start()

@app.get("/")
async def root():
    """Root endpoint providing system information."""
    return {
        "message": "Multi-Agent RFP Automation System (Demo Mode)",
        "version": "1.0.0-demo",
        "status": "operational",
        "mode": "demo",
        "agents": {
            "rfp_identification": "Ready for RFP monitoring",
            "orchestrator": "Ready for workflow management", 
            "technical_match": "Ready for requirement processing",
            "pricing": "Ready for cost analysis"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "demo",
        "services": {
            "api": "operational",
            "agents": "simulated",
            "database": "mock_data"
        }
    }

@app.get("/api/v1/rfps/")
async def list_rfps():
    """Get list of RFPs."""
    return mock_rfps

@app.get("/api/v1/rfps/{rfp_id}")
async def get_rfp(rfp_id: str):
    """Get specific RFP by ID."""
    rfp = next((r for r in mock_rfps if r["id"] == rfp_id), None)
    if not rfp:
        return JSONResponse(status_code=404, content={"detail": "RFP not found"})
    return rfp

@app.get("/api/v1/agents/")
async def list_agents():
    """Get list of agents."""
    return mock_agents

@app.get("/api/v1/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent by ID."""
    agent = next((a for a in mock_agents if a["id"] == agent_id), None)
    if not agent:
        return JSONResponse(status_code=404, content={"detail": "Agent not found"})
    return agent

@app.post("/api/v1/rfps/")
async def create_rfp(rfp_data: CreateRFPRequest):
    """Create a new RFP and start workflow processing."""
    # Generate new RFP
    new_rfp = {
        "id": str(uuid.uuid4()),
        "title": rfp_data.title,
        "source": rfp_data.source,
        "status": "processing",
        "priority": rfp_data.priority,
        "dueDate": rfp_data.dueDate,
        "projectValue": rfp_data.projectValue,
        "progress": 0,
        "detectedAt": datetime.utcnow().isoformat() + "Z",
        "requirements": 0,
        "matches": 0,
        "agent": "RFP Identification Agent"
    }
    
    # Add to mock data
    mock_rfps.append(new_rfp)
    
    # Create and start workflow
    workflow_id = f"wf-{str(uuid.uuid4())[:8]}"
    simulate_workflow_progress(new_rfp["id"], workflow_id)
    
    return {
        "rfp": new_rfp,
        "workflow_id": workflow_id,
        "message": "RFP created and workflow started successfully"
    }

@app.get("/api/v1/workflows/")
async def list_workflows():
    """Get list of workflows."""
    return list(mock_workflows.values())

@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get specific workflow by ID."""
    workflow = mock_workflows.get(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@app.get("/api/v1/dashboard/metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics."""
    return {
        "totalRFPs": len(mock_rfps),
        "activeRFPs": len([r for r in mock_rfps if r["status"] in ["processing", "matched"]]),
        "completedRFPs": len([r for r in mock_rfps if r["status"] in ["reviewed", "submitted"]]),
        "totalValue": sum(r["projectValue"] for r in mock_rfps),
        "activeAgents": len([a for a in mock_agents if a["status"] == "active"]),
        "avgEfficiency": sum(a["efficiency"] for a in mock_agents) / len(mock_agents),
        "lastUpdate": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Multi-Agent RFP System Demo...")
    print("📊 Demo Mode - No external dependencies required")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "demo_main:app",
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload to prevent workflow data loss
    )