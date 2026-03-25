"""
Main API router for version 1 of the Multi-Agent RFP System API.

This module aggregates all API endpoints and provides the main router
that is included in the FastAPI application.
"""

from fastapi import APIRouter

from api.v1.endpoints import rfps, agents, products, pricing, dashboard, websocket

# Create the main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    rfps.router,
    prefix="/rfps",
    tags=["RFPs"]
)

api_router.include_router(
    agents.router,
    prefix="/agents",
    tags=["Agents"]
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Products"]
)

api_router.include_router(
    pricing.router,
    prefix="/pricing",
    tags=["Pricing"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

api_router.include_router(
    websocket.router,
    prefix="/ws",
    tags=["WebSocket"]
)