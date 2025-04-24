import os
import sys
import subprocess
import time
import signal
import atexit

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the Streamlit app
from app.main import main

def cleanup(process):
    """Cleanup function to terminate processes"""
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

def run_servers():
    # Start FastAPI server in a separate process
    fastapi_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Register cleanup for FastAPI process
    atexit.register(cleanup, fastapi_process)
    
    # Give FastAPI server time to start
    time.sleep(2)
    
    try:
        # Start Streamlit with the correct Python path
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app/main.py"],
            env={**os.environ, "PYTHONPATH": project_root},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Register cleanup for Streamlit process
        atexit.register(cleanup, streamlit_process)
        
        # Wait for both processes
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure cleanup is called
        cleanup(fastapi_process)
        cleanup(streamlit_process)

if __name__ == "__main__":
    main() 