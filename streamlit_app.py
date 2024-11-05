import streamlit as st
import pandas as pd
import numpy as np
import subprocess

st.title('Regulatory check')

# Function to run the entire Agent_for_noncompliance_checks.py file
def run_agent_for_noncompliance_checks():
    subprocess.run(["python", "Agent_for_noncompliance_checks.py"], check=True)

def run_dual_agents_for_GCS():
    subprocess.run(["python", "Dual_Agents_for_GCS.py"], check=True)

def run_dual_agents_for_requirements():
    subprocess.run(["python", "Dual_Agents_for_Requirements.py"], check=True)

# Use the on_click parameter to link the function to the button
st.button("Parse project data", on_click=run_agent_for_noncompliance_checks)
st.button("Parse regulatory requirements", on_click=run_dual_agents_for_GCS)
st.button("Compare and check", on_click=run_dual_agents_for_requirements)


