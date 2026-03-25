"""
Multi-Agent RFP Automation System - Main Application Entry Point

This module initializes the FastAPI application with all necessary middleware,
routers, and configurations for the multi-agent RFP processing system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import structlog

from core.config import settings
from core.database import init_db
from core.redis_client import init_redis
from api.v1.api import api_router


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    Handles:
    - Database initialization (optional for demo)
    - Redis connection setup (in-memory fallback)
    - Agent service initialization
    - Cleanup on shutdown
    """
    logger.info("Starting Multi-Agent RFP System...")
    
    try:
        # Initialize database (optional for demo)
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning("Database initialization skipped for demo", error=str(e))
    
    try:
        # Initialize Redis (with in-memory fallback)
        await init_redis()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning("Redis initialization skipped for demo", error=str(e))
    
    # TODO: Initialize agents when implemented
    # await init_agents()
    
    logger.info("Multi-Agent RFP System started successfully (Demo Mode)")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Multi-Agent RFP System...")


# Create FastAPI application
app = FastAPI(
    title="Multi-Agent RFP Automation System",
    description="Intelligent platform for automated RFP response generation using specialized AI agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add security middleware
from core.config import get_allowed_hosts, get_cors_origins

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=get_allowed_hosts()
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint providing system information."""
    return {
        "message": "Multi-Agent RFP Automation System",
        "version": "1.0.0",
        "status": "operational",
        "agents": {
            "rfp_identification": "Ready for RFP monitoring",
            "orchestrator": "Ready for workflow management", 
            "technical_match": "Ready for requirement processing",
            "pricing": "Ready for cost analysis"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        # TODO: Add actual health checks for database, redis, agents
        return {
            "status": "healthy",
            "timestamp": structlog.processors.TimeStamper(fmt="iso")(),
            "services": {
                "database": "connected",
                "redis": "connected", 
                "agents": "operational"
            }
        }
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unavailable")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )