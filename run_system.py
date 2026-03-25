#!/usr/bin/env python3
"""
Multi-Agent RFP System Launcher

This script provides a convenient way to start the entire system
including the backend API, agents, and database initialization.
"""

import asyncio
import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Print system banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                Multi-Agent RFP Automation System             ║
    ║                                                              ║
    ║  🤖 Intelligent RFP Processing with AI Agents               ║
    ║  🚀 Transforming RFP Response from Days to Hours            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required dependencies are available."""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3.8, 0):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check if virtual environment exists
    venv_path = Path("backend/venv")
    if not venv_path.exists():
        print("⚠️  Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", "backend/venv"])
        print("✅ Virtual environment created")
    
    # Check if requirements are installed
    try:
        import fastapi
        import sqlalchemy
        import redis
        print("✅ Core dependencies found")
    except ImportError:
        print("⚠️  Installing Python dependencies...")
        subprocess.run([
            "backend/venv/bin/pip" if os.name != 'nt' else "backend\\venv\\Scripts\\pip",
            "install", "-r", "backend/requirements.txt"
        ])
        print("✅ Dependencies installed")
    
    return True

def check_services():
    """Check if required services are running."""
    print("🔍 Checking required services...")
    
    # Check PostgreSQL
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="rfp_system",
            user="rfp_user",
            password="rfp_password"
        )
        conn.close()
        print("✅ PostgreSQL is running")
    except Exception:
        print("❌ PostgreSQL not available. Please start it with: docker-compose up -d postgres")
        return False
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis is running")
    except Exception:
        print("❌ Redis not available. Please start it with: docker-compose up -d redis")
        return False
    
    return True

def initialize_database():
    """Initialize the database with sample data."""
    print("🗄️  Initializing database...")
    
    try:
        # Run database initialization
        subprocess.run([
            "backend/venv/bin/python" if os.name != 'nt' else "backend\\venv\\Scripts\\python",
            "database/init_db.py"
        ], cwd="backend", check=True)
        print("✅ Database initialized with sample data")
        return True
    except subprocess.CalledProcessError:
        print("❌ Database initialization failed")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting FastAPI backend server...")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Start the server
    cmd = [
        "venv/bin/uvicorn" if os.name != 'nt' else "venv\\Scripts\\uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    
    return subprocess.Popen(cmd)

def start_frontend():
    """Start the React frontend development server."""
    print("🎨 Starting React frontend server...")
    
    # Change to frontend directory
    os.chdir("../frontend")
    
    # Install dependencies if needed
    if not Path("node_modules").exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
    
    # Start the development server
    cmd = ["npm", "start"]
    return subprocess.Popen(cmd)

async def start_agents():
    """Start the AI agents."""
    print("🤖 Starting AI agents...")
    
    # Import and start agents
    sys.path.append("backend")
    
    try:
        from agents.rfp_identification_agent import RFPIdentificationAgent
        from agents.orchestrator_agent import OrchestratorAgent
        from agents.technical_match_agent import TechnicalMatchAgent
        from agents.pricing_agent import PricingAgent
        
        # Create agent instances
        agents = [
            RFPIdentificationAgent(),
            OrchestratorAgent(),
            TechnicalMatchAgent(),
            PricingAgent()
        ]
        
        # Start all agents
        tasks = []
        for agent in agents:
            task = asyncio.create_task(agent.start())
            tasks.append(task)
        
        print("✅ All agents started successfully")
        
        # Keep agents running
        await asyncio.gather(*tasks)
        
    except Exception as e:
        print(f"❌ Failed to start agents: {e}")

def main():
    """Main function to orchestrate system startup."""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return 1
    
    # Check services
    if not check_services():
        print("❌ Please start required services with: docker-compose up -d")
        return 1
    
    # Initialize database
    if not initialize_database():
        print("❌ Database initialization failed")
        return 1
    
    print("\n🎉 System startup complete!")
    print("\n📊 Access points:")
    print("   • Frontend Dashboard: http://localhost:3000")
    print("   • Backend API: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Database Admin: http://localhost:5050 (admin@rfpsystem.com / admin123)")
    print("   • Redis Commander: http://localhost:8081")
    
    try:
        # Start backend
        backend_process = start_backend()
        
        # Start frontend
        frontend_process = start_frontend()
        
        # Start agents
        print("\n🤖 Starting AI agents...")
        asyncio.run(start_agents())
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        print("✅ System shutdown complete")
        return 0
    except Exception as e:
        print(f"❌ System error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())