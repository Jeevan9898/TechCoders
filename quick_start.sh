#!/bin/bash

# Multi-Agent RFP System - Quick Start Script
# This script starts the system in demo mode without external dependencies

echo "🚀 Multi-Agent RFP System - Quick Start"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Starting in Demo Mode (No Docker/PostgreSQL/Redis required)${NC}"
echo

# Function to start backend
start_backend() {
    echo -e "${GREEN}🔧 Starting Backend API Server...${NC}"
    cd backend
    source venv/bin/activate
    python demo_main.py &
    BACKEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
}

# Function to start frontend
start_frontend() {
    echo -e "${GREEN}🎨 Starting Frontend Dashboard...${NC}"
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down system...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}✅ System shutdown complete${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start services
start_backend
sleep 3
start_frontend

echo
echo -e "${BLUE}🎉 Multi-Agent RFP System is starting up!${NC}"
echo
echo -e "${GREEN}📊 Access Points:${NC}"
echo "   • Frontend Dashboard: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo
echo -e "${BLUE}✨ New Features Available:${NC}"
echo "   • Click 'Create RFP' button to add new RFPs"
echo "   • Watch real-time workflow progress in Workflow Visualization"
echo "   • See live agent coordination and step-by-step processing"
echo
echo -e "${YELLOW}⏳ Please wait 30-60 seconds for both servers to fully start${NC}"
echo -e "${YELLOW}🛑 Press Ctrl+C to stop the system${NC}"
echo

# Wait for user interrupt
while true; do
    sleep 1
done