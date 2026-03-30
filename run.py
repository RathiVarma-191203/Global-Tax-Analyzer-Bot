"""
Launcher for Global Tax Analyzer.
Runs both FastAPI (Backend) and Streamlit (Frontend) concurrently.
"""
import subprocess
import sys
import os
import time
from dotenv import load_dotenv

load_dotenv()

def run_backend():
    print("🚀 Starting FastAPI Backend on http://localhost:8000...")
    return subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.backend.main:app",
        "--host", "0.0.0.0", "--port", "8000"
    ])

def run_frontend():
    print("🎨 Starting Streamlit Frontend...")
    return subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app/frontend/app.py"
    ])

if __name__ == "__main__":
    backend_proc = None
    frontend_proc = None
    
    try:
        backend_proc = run_backend()
        # Give backend a moment to start
        time.sleep(3)
        
        frontend_proc = run_frontend()
        
        print("\n✅ Both services are now running.")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:8501 (default Streamlit port)")
        print("\nPress Ctrl+C to stop both services.")
        
        # Keep the main script alive while processes are running
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("❌ Backend stopped unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("❌ Frontend stopped unexpectedly.")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
    finally:
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print("👋 Goodbye!")
