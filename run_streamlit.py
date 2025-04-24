import os
import sys
import streamlit.web.cli as stcli

def main():
    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the script directory to the Python path
    sys.path.insert(0, script_dir)
    
    # Set up the command line arguments for Streamlit
    sys.argv = [
        "streamlit",
        "run",
        os.path.join(script_dir, "app", "main.py"),
        "--global.developmentMode=false",
    ]
    
    # Run Streamlit
    sys.exit(stcli.main())

if __name__ == "__main__":
    main() 