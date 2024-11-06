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
from pages import about, documentation, methodology  # Assuming the folder name is "pages" and you have "about.py" and "methodology.py"

# Setting up logging to handle UnicodeEncodeError
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s', encoding='utf-8')

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

# Link to Google Docs
st.sidebar.title("[Documentation](https://docs.google.com/document/d/1WM_VcDOJFLNh7Mgytr2DAWONTII3NS-6Gi6kzUKtDfQ/edit?usp=sharing)")
# Sidebar content
st.sidebar.markdown("Prepared by")
st.sidebar.markdown("PONG Woon Wei (Lead)")

# Acknowledgement
st.sidebar.markdown("Acknowledgements: This project leverages AI models and services provided by OpenAI and Perplexity AI.")

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

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["[ About Us ]", "[ AI Solutions ]", "[ Methodology ]", "[ Documentation ]"])

if page == "[ AI Solutions ]":
    # [ About Us ] Page Content
    st.header("Home - Agent-based Analyser for Technical and Regulatory Requirements Checks")
    # Button to run the Design Intent parsing script
    st.header("Design Intent - Parse, Calculate & Tabulate")
    st.write("""
    Click the button to allow:
    1. AI Agent 1 to parse the provided window schedule drawing (in jpeg), and calculate the maximum room area using the predefined 10% ventilation requirement.
    2. AI Agent 2 to clean, tabulate and save as Excel output for the next AI Agent to check.
    """)

    if st.button("Run Design Intent Parsing Script"):
        with st.spinner("Downloading and Running Design Intent Parsing Script..."):
            local_path = download_script_from_gcs(bucket_name, gcs_scripts["Design Intent Parsing"], "Dual_Agents_for_GCS.py")
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
    1. Agent 3 to analyze compliance-related requirements with the provided PDF documents from Google Cloud Storage.
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
    1. Agent 5 to use the provided window schedule as design requirements to check against regulatory requirements and provide recommendations for compliance.
    2. BCA Approved Doc & SCDF Chapter 4 are provided as default requirements for the checks and recommendations.
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
    st.write("Click the link below to open the GPT-4o-Mini application for text file parsing in a new tab.")
    # CSS styling to set link color to white with dark gray background and mild red on hover, no underline on hover
    button_html = f"""
        <style>
            /* Button style */
            .button {{
                background-color: #1a1a1a; /* Dark gray background */
                color: white !important; /* White text, forced with !important */
                border: 1px solid #444444; /* Dark gray border */
                padding: 5px 7px; /* Padding for spacing */
                font-size: 16px; /* Font size */
                border-radius: 8px; /* Rounded corners */
                text-align: center;
                cursor: pointer; /* Pointer cursor on hover */
                display: inline-block; /* Inline-block for styling as button */
                text-decoration: none; /* No underline */
                transition: color 0.3s ease, border-color 0.3s ease; /* Smooth transition */
            }}
            /* Hover effect */
            .button:hover {{
                color: #ff6b6b !important; /* Mild red color on hover, forced with !important */
                border-color: #ff6b6b; /* Mild red border on hover */
                text-decoration: none; /* Ensures no underline on hover */
            }}
        </style>

        <!-- Button HTML as a link -->
        <a href="https://bca-project.streamlit.app/" target="_blank" class="button">Open GPT-4o-Mini Text File Parser</a>
    """

    # Display the styled button
    st.markdown(button_html, unsafe_allow_html=True)

elif page == "[ About Us ]":
    # [ About Us ] Page Content
    about.about()  # Calling the function 'app()' from about.py

elif page == "[ Methodology ]":
    # [ Methodology ] Page Content
    methodology.methodology()  # Calling the function 'app()' from methodology.py

elif page == "[ Documentation ]":
    # [ Documentation ] Page Content
    documentation.documentation()  # Calling the function 'app()' from documentation.py
