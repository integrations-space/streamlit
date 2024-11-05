import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import webbrowser

st.title('Regulatory check')

# # Function to run the entire Agent_for_noncompliance_checks.py file
# def run_agent_for_noncompliance_checks():
#     with open("Agent_for_noncompliance_checks.py") as file:
#         exec(file.read())

# Button to run the non-compliance checks script
if st.button("Run Compliance Check Script"):
    with st.spinner("Running Compliance Check..."):
        with open("Agent_for_noncompliance_checks.py") as file:
            result = exec(file.read())
    st.write("Output from Compliance Check Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

# def run_dual_agents_for_GCS():
#     with open("Dual_Agents_for_GCS.py") as file:
#         exec(file.read())

# Button to run the GCS parsing script
if st.button("Run GCS Parsing Script"):
    with st.spinner("Running GCS Parsing..."):
        with open("Dual_Agents_for_GCS.py") as file:
            result = exec(file.read())
    st.write("Output from GCS Parsing Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

# def run_dual_agents_for_requirements():
#     with open("Dual_Agents_for_Requirements.py") as file:
#         exec(file.read())

# Button to run the requirements parsing script
if st.button("Run Requirements Parsing Script"):
    with st.spinner("Running Requirements Parsing..."):
        with open("Dual_Agents_for_Requirements.py") as file:
            result = exec(file.read())
    st.write("Output from Requirements Parsing Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

# # Use the on_click parameter to link the function to the button
# st.button("Parse project data", on_click=run_agent_for_noncompliance_checks)
# st.button("Parse regulatory requirements", on_click=run_dual_agents_for_GCS)
# st.button("Compare and check", on_click=run_dual_agents_for_requirements)

# New Section: GPT-4o-Mini Text File Parsing
st.header("GPT-4o-Mini Text File Parsing")

st.write("Click the button below to open the GPT-4o-Mini application for text file parsing in a new tab.")

if st.button("Open GPT-4o-Mini Text File Parser"):
    webbrowser.open_new_tab("https://bca-project.streamlit.app/")
    st.success("Opened GPT-4o-Mini Text File Parser in a new browser tab.")

