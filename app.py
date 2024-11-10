import streamlit as st
import pandas as pd
import webbrowser
from google.cloud import storage
from google.oauth2 import service_account
import sys
import logging
import os
import importlib.util
import time
import threading

# Import the new pages
from pages import about, methodology  # Assuming the folder name is "pages" and you have "about.py" and "methodology.py"

# Display the disclaimer using st.sidebar.expander
with st.expander("⚠️ Disclaimer and Important Notice", expanded=False):
    st.write("""
    **This web application is a proof of concept developed for learning purposes only.** 
    - The information provided here is NOT fully ready to be relied upon for making any decisions, especially those related to financial, legal, construction-related matters, or any other actual real-life applications.
    - Please be aware that the LLM may generate inaccurate or incorrect information. 
    - You should assume full responsibility for how you use any generated output.
    - **Please consult with qualified professionals for accurate and personalized advice.**
    """)

# Setting up logging to handle UnicodeEncodeError
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

# Simple authentication mechanism
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def authenticate():
    # Using secrets for authentication credentials
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if (username == st.secrets["auth"]["username"] and 
            password == st.secrets["auth"]["password"]):
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials")

if not st.session_state.authenticated:
    st.sidebar.header('Authentication Required')
    authenticate()
    if not st.session_state.authenticated:
        st.stop()

# Set up Google Cloud credentials using secrets
credentials_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)
storage_client = storage.Client(credentials=credentials)
logging.info("Google Cloud Storage client initialized using credentials from Streamlit secrets.")

# Directory to save downloaded scripts locally
LOCAL_SCRIPT_PATH = "/tmp/gcs_agents"
os.makedirs(LOCAL_SCRIPT_PATH, exist_ok=True)

# Define bucket name and script paths
bucket_name = "data_parsing"
gcs_scripts = {
    "Design Intent Parsing": "agents/Dual_Agents_for_GCS.py",
    "Requirements Parsing": "agents/Dual_Agents_for_Requirements.py",
    "Non-Compliance Checks": "agents/Agent_for_non-compliances_Checks.py"
}

# Function to download and save the Python scripts from GCS
def download_script_from_gcs(bucket_name, gcs_path, local_script_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_path)
        local_path = os.path.join(LOCAL_SCRIPT_PATH, local_script_name)
        blob.download_to_filename(local_path)
        logging.info(f"Downloaded {gcs_path} to {local_path}")
        return local_path
    except Exception as e:
        st.error(f"Failed to download file from GCS: {e}")
        return None

# Function to load and run a Python script from the given path
def load_and_run_script(script_path):
    try:
        spec = importlib.util.spec_from_file_location("script_module", script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            logging.error(f"Could not load the script at {script_path}")
    except Exception as e:
        logging.error(f"Error while loading the script: {e}")

# Function to read a file from GCS
def read_file_from_gcs(bucket_name, file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        return blob.download_as_text()
    except Exception as e:
        st.error(f"Error reading file from GCS: {e}")
        return None

# Function to read an Excel file from GCS
def read_excel_from_gcs(bucket_name, file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        excel_data = blob.download_as_bytes()
        return pd.read_excel(pd.io.common.BytesIO(excel_data))
    except Exception as e:
        st.error(f"Error reading Excel file from GCS: {e}")
        return None

# Function to run a script in a separate thread to prevent UI hang
def run_script_in_thread(target, *args):
    thread = threading.Thread(target=target, args=args)
    thread.start()

# Main Page Content
st.header("Agent-based Analyser for Technical and Regulatory Requirements Checks")

# Button to run the Design Intent parsing script
st.subheader("Design Intent - Parse, Calculate & Tabulate")
st.write("""
Click the button to allow:
1. AI Agent 1 to parse the provided window schedule drawing (in jpeg), and calculate the maximum room area using the predefined 10% ventilation requirement.
2. AI Agent 2 to clean, tabulate and save as Excel output for the next AI Agent to check.
""")

if st.button("Run Design Intent Parsing Script"):
    with st.spinner("Downloading and Running Design Intent Parsing Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["Design Intent Parsing"], "Dual_Agents_for_GCS.py")
        if local_path:
            run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Display the output
    file_name = "parsed_output/window_schedule.xls"
    df = read_excel_from_gcs(bucket_name, file_name)
    if df is not None:
        st.write("Content of the Excel file:")
        st.dataframe(df)

# Button to run the requirements parsing script
st.subheader("Requirements - Parse & Compare")
st.write("""
Click the button to allow:
1. Agent 3 to analyze compliance-related requirements with the provided PDF documents from Google Cloud Storage.
2. Agent 4 to extract and summarize key information from regulatory documents, providing structured analysis on specific requirements.
""")

if st.button("Run Requirements Parsing Script"):
    with st.spinner("Downloading and Running Requirements Parsing Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["Requirements Parsing"], "Dual_Agents_for_Requirements.py")
        if local_path:
            run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Display the output
    file_name = "parsed_output/Requirements.txt"
    content = read_file_from_gcs(bucket_name, file_name)
    if content:
        st.write("Content of the file:")
        st.text_area("File Content", content, height=300)

# Button to run the non-compliance checks script
st.subheader("Output - Checks and Recommend")
st.write("""
Click the button to allow:
1. Agent 5 to use the provided window schedule as design requirements to check against regulatory requirements and provide recommendations for compliance.
2. BCA Approved Doc & SCDF Chapter 4 are provided as default requirements for the checks and recommendations.
""")

if st.button("Run Compliance Check Script"):
    with st.spinner("Downloading and Running Compliance Check Script..."):
        local_path = download_script_from_gcs(bucket_name, gcs_scripts["Non-Compliance Checks"], "Agent_for_non_compliances_Checks.py")
        if local_path:
            run_script_in_thread(load_and_run_script, local_path)
    time.sleep(2)

    # Display the output
    file_name = "parsed_output/check_1.xlsx"
    df = read_excel_from_gcs(bucket_name, file_name)
    if df is not None:
        st.write("Content of the Excel file:")
        st.dataframe(df)

# New Section: GPT-4o-Mini Text File Parsing
st.header("Validation - explore the use of GPT-4o-Mini Text File Parsing for topic-focused requirements")
st.write("Click the link below to open the GPT-4o-Mini application for text file parsing in a new tab.")

# CSS styling to set link color to white with dark gray background and mild red on hover, no underline on hover
button_html = f"""
    <style>
        .button {{
            background-color: #1a1a1a;
            color: white !important;
            border: 1px solid #444444;
            padding: 5px 7px;
            font-size: 16px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            display: inline-block;
            text-decoration: none;
            transition: color 0.3s ease, border-color 0.3s ease;
        }}
        .button:hover {{
            color: #ff6b6b !important;
            border-color: #ff6b6b;
            text-decoration: none;
        }}
    </style>
    <a href="https://bca-project.streamlit.app/" target="_blank" class="button">Open GPT-4o-Mini Text File Parser</a>
"""
# Display the styled button
st.markdown(button_html, unsafe_allow_html=True)

# Section: Presentation Link
st.header("Presentation Slides")
st.write("Click the link below to view the presentation slides for the project:")
# CSS styling to set link color to white with dark gray background and mild red on hover, no underline on hover
button_html = f"""
    <style>
        .button {{
            background-color: #1a1a1a;
            color: white !important;
            border: 1px solid #444444;
            padding: 5px 7px;
            font-size: 16px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            display: inline-block;
            text-decoration: none;
            transition: color 0.3s ease, border-color 0.3s ease;
        }}
        .button:hover {{
            color: #ff6b6b !important;
            border-color: #ff6b6b;
            text-decoration: none;
        }}
    </style>
    <a href="https://github.com/integrations-space/streamlit/blob/main/ants_abc2024.pdf" target="_blank" class="button">Presentation Slides</a>
"""
# Display the styled button
st.markdown(button_html, unsafe_allow_html=True)
