import os
import subprocess

# Run Streamlit script using subprocess
def run_streamlit():
    streamlit_file = "ollama_server/exp_ollama_streamlit_app.py"
    subprocess.Popen(["streamlit", "run", streamlit_file])

if __name__ == "__main__":
    run_streamlit()

# This Python script helps to run the streamlit based Py code via the "Run Python File" botton in VS Code.

