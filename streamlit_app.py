import streamlit as st
import subprocess
import pandas as pd
import webbrowser
from google.cloud import storage
import sys
import logging
import os
import importlib.util
import time
import threading

# Setting up logging to handle UnicodeEncodeError
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s', encoding='utf-8')

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Directory to save downloaded scripts locally
LOCAL_SCRIPT_PATH = "/tmp/gcs_agents"
os.makedirs(LOCAL_SCRIPT_PATH, exist_ok=True)

# Function to download and save the Python scripts from GCS

def download_script_from_gcs(bucket_name, gcs_path, local_script_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    local_path = os.path.join(LOCAL_SCRIPT_PATH, local_script_name)
    blob.download_to_filename(local_path)
    logging.info(f"Downloaded {gcs_path} to {local_path}")
    return local_path

# Function to load and run a Python script from the given path

def load_and_run_script(script_path):
    spec = importlib.util.spec_from_file_location("script_module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

# Function to read a file from GCS
def read_file_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.download_as_text()  # Returns the content of the file as text

# Function to read an Excel file from GCS
def read_excel_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the Excel file to a BytesIO object
    excel_data = blob.download_as_bytes()

    # Use pandas to read the Excel file from the BytesIO object
    return pd.read_excel(pd.io.common.BytesIO(excel_data))

# Function to run a script in a separate thread to prevent UI hang
def run_script_in_thread(target, *args):
    thread = threading.Thread(target=target, args=args)
    thread.start()

# Set the title for the application
st.title('Agent-based Analyser for Technical and Regulatory Requirements Checks')

# Intro text
st.write("""
The solutions are using Vertex AI and OpenAI LLM models, the proposed solution enables a structured understanding of project data, 
focusing on design intent, requirement parsing, output checks, and validations. 
It organizes user-provided project data and requirements into an accessible tabulated format, covering five key areas:
1. Design Intent: Extracts measurable figures from technical drawings, PDF building specifications, and project documents to clarify the intended design.
2. Requirements: Parses guidelines, Singapore Standards, and/or regulations to derive measurable figures that form the project’s compliance criteria.
3. Output Checks: Compares the extracted design intent against parsed requirements to identify any non-compliance issues.
4. Recommendations: Provides suggestions based on the most stringent requirements for improved compliance.
5. Validations: Cross-checks online data to confirm common practices and compliance requirements using OpenAI 4.0 mini.
""")

# Define GCS bucket and paths to the parser scripts
bucket_name = "data_parsing"
gcs_scripts = {
    "GCS Parsing": "agents/Dual_Agents_for_GCS.py",
    "Requirements Parsing": "agents/Dual_Agents_for_Requirements.py",
    "Non-Compliance Checks": "agents/Agent_for_non-compliances_Checks.py"
}

# Button to run the GCS parsing script
st.header("Design Intent - Parse, Calculate & Tabulate")
st.write("""
Click the button to allow:
1. AI Agent 1 to parse the provided window schedule drawing (in jpeg), and calculate the maximum room area using the predefined 10% ventilation requirement.
2. AI Agent 2 to clean, tabulate and save as Excel output for the next AI Agent to check.
""")

if st.button("Run GCS Parsing Script"):
    with st.spinner("Downloading and Running GCS Parsing Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["GCS Parsing"], "Dual_Agents_for_GCS.py")
        run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Input for GCS bucket name and file name
    file_name = "parsed_output/window_schedule.xls"
    try:
        df = read_excel_from_gcs(bucket_name, file_name)
        st.write("Content of the Excel file:")
        st.dataframe(df)  # Displaying the DataFrame in the app
    except Exception as e:
        st.error(f"Error reading Excel file from GCS: {str(e)}")

# Button to run the requirements parsing script
st.header("Requirements - Parse & Compare")
st.write("""
Click the button to allow:
1. Agent 3 to analyze compliance-related requirements with the provided pdf documents from Google Buckets.
2. Agent 4 to extract and summarize key information from regulatory documents, providing structured analysis on specific requirements.
""")

if st.button("Run Requirements Parsing Script"):
    with st.spinner("Downloading and Running Requirements Parsing Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["Requirements Parsing"], "Dual_Agents_for_Requirements.py")
        run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Input for GCS bucket name and file name
    file_name = "parsed_output/Requirements.txt"
    try:
        content = read_file_from_gcs(bucket_name, file_name)
        st.write("Content of the file:")
        st.text_area("File Content", content, height=300)
    except Exception as e:
        st.error(f"Error reading text file from GCS: {str(e)}")

# Button to run the non-compliance checks script
st.header("Output - Checks and Recommend")
st.write("""
Click the button to allow:
1. Agent 5 to use the provided window schedule as design requirements to check against design requirements, and recommendations for compliance needs.
2. BCA Approved Doc & SCDF Chapter 4 were provided as default requirements for the checks and recommendations.
""")

if st.button("Run Compliance Check Script"):
    with st.spinner("Downloading and Running Compliance Check Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["Non-Compliance Checks"], "Agent_for_non_compliances_Checks.py")
        run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Input for GCS bucket name and file name
    file_name = "parsed_output/check_1.xlsx"
    try:
        df = read_excel_from_gcs(bucket_name, file_name)
        st.write("Content of the Excel file:")
        st.dataframe(df)  # Displaying the DataFrame in the app
    except Exception as e:
        st.error(f"Error reading Excel file from GCS: {str(e)}")

# New Section: GPT-4o-Mini Text File Parsing
st.header("Validation - explore the use of GPT-4o-Mini Text File Parsing for topic-focused requirements")
st.write("Click the button below to open the GPT-4o-Mini application for text file parsing in a new tab.")
if st.button("Open GPT-4o-Mini Text File Parser"):
    webbrowser.open_new_tab("https://bca-project.streamlit.app/")
