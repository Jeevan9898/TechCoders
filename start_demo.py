#!/usr/bin/env python3
"""
Quick Demo Launcher for Multi-Agent RFP System

This script starts the system with minimal setup for immediate demonstration.
"""

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
    ║                        DEMO MODE                             ║
    ║                                                              ║
    ║  🤖 4 AI Agents Ready for Demonstration                     ║
    ║  🚀 No External Dependencies Required                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

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
    
    # Start the development server
    cmd = ["npm", "start"]
    return subprocess.Popen(cmd)

def main():
    """Main function to start the demo."""
    print_banner()
    
    print("🎯 Starting Multi-Agent RFP System Demo...")
    print("\n📊 This demo includes:")
    print("   • Interactive React Dashboard")
    print("   • 4 AI Agents (simulated for demo)")
    print("   • Real-time monitoring interface")
    print("   • Complete workflow visualization")
    print("   • Sample RFP data")
    
    print("\n🌐 Access points:")
    print("   • Frontend Dashboard: http://localhost:3000")
    print("   • Backend API: http://localhost:8000")
    print("   • API Documentation: http://localhost:8000/docs")
    
    try:
        # Start backend
        print("\n🔧 Starting backend...")
        backend_process = start_backend()
        time.sleep(3)
        
        # Start frontend
        print("🎨 Starting frontend...")
        frontend_process = start_frontend()
        
        print("\n✅ System is starting up!")
        print("🎯 Open http://localhost:3000 in your browser")
        print("⏳ Please wait 30-60 seconds for both servers to fully start")
        print("\n🛑 Press Ctrl+C to stop the system")
        
        # Wait for user interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down system...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ System shutdown complete")
            return 0
            
    except Exception as e:
        print(f"❌ System error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())