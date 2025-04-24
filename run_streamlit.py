import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))  # Changed from append to insert to give it priority

if __name__ == "__main__":
    os.system(f"PYTHONPATH={project_root} streamlit run {project_root}/app/main.py") 