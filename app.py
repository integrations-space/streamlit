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
from io import BytesIO  # Add missing import

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
[data-testid="stToolbar"] {visibility: hidden !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {visibility: hidden !important;}
[data-testid="stHeader"] {background-color: transparent !important;}
[data-testid="stToolbar"] {right: 2rem !important;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Setting up logging to handle UnicodeEncodeError
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')  # Logging configuration to send logs to stdout

# Authentication mechanism
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False  # Adding a key to session_state to track authentication status

def authenticate():
    """Function to authenticate the user."""
    st.sidebar.header("Authentication Required")  # Header to prompt user to authenticate
    username = st.sidebar.text_input("Username")  # Username input field
    password = st.sidebar.text_input("Password", type="password")  # Password input field

    if st.sidebar.button("Login"):  # Login button to trigger authentication
        if (username == st.secrets["auth"]["username"] and  # Check if username matches the secret stored
            password == st.secrets["auth"]["password"]):  # Check if password matches the secret stored
            st.session_state.authenticated = True  # Update authentication status on successful login
        else:
            st.sidebar.error("Invalid credentials")  # Error message for invalid credentials

# Authentication check
if not st.session_state.authenticated:
    authenticate()  # Call authenticate function if user is not authenticated
    if not st.session_state.authenticated:
        st.stop()  # Stop the application until the user is authenticated

# Navigation after successful authentication
st.sidebar.title("Navigation")  # Sidebar title for navigation
selected_page = st.sidebar.radio("Select a page:", ["About", "Methodology", "Proposed Solution / PoC", "Documentation", "AI Models' Comparison", "Disclaimer", "Acknowledgement"])  # Sidebar navigation options

# Function to dynamically load a module from the protected_pages directory
def load_protected_page(page_name):
    """Dynamically loads a page module from the protected_pages directory."""
    module_path = os.path.join(os.path.dirname(__file__), "protected_pages", f"{page_name}.py")  # Construct the path to the page module

    # Check if the file exists before attempting to load it
    if not os.path.exists(module_path):
        st.error(f"The requested page '{page_name}' does not exist. Path: {module_path}")  # Display error if file doesn't exist
        return

    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(page_name, module_path)  # Get the module specification
        if spec and spec.loader:
            page_module = importlib.util.module_from_spec(spec)  # Create a module object
            spec.loader.exec_module(page_module)  # Execute the module
            # Check if app() function exists
            if hasattr(page_module, "app"):
                page_module.app()  # Call a function named `app()` within the module to display content
            else:
                st.error(f"The page '{page_name}' does not have an 'app()' function.")  # Error if no app() function is found
        else:
            st.error(f"Failed to load the page '{page_name}'. Module specification issue.")  # Error if module spec is invalid
    except Exception as e:
        st.error(f"An error occurred while loading the page '{page_name}': {str(e)}")  # Error handling for exceptions during module loading

# Display the selected page
if selected_page == "About":
    load_protected_page("about")  # Load the about page
elif selected_page == "Methodology":
    load_protected_page("methodology")  # Load the methodology page
elif selected_page == "Proposed Solution / PoC":
# Create an expander for the notice on errors
    with st.expander("⚠️ Important Notice for Errors ⚠️"):
        st.write("""
        The Proof of Concept (PoC) was successfully completed with a perfect score of 45/45. As a result, billing for Google services (GCS, Vertex AI, etc.) has been disabled to prevent further costs. 
        This may result in errors for certain buttons, as some functions have been deactivated. 
        Previously generated outcomes will still be available for viewing. Thank you for your understanding.
        """)
    # Set up Google Cloud credentials using secrets
    credentials_info = st.secrets["gcp_service_account"]  # Get GCP service account credentials from Streamlit secrets
    credentials = service_account.Credentials.from_service_account_info(credentials_info)  # Create credentials object
    storage_client = storage.Client(credentials=credentials)  # Initialize the storage client with credentials
    logging.info("Google Cloud Storage client initialized using credentials from Streamlit secrets.")  # Log successful initialization

    # Directory to save downloaded scripts locally
    LOCAL_SCRIPT_PATH = "/tmp/gcs_agents"  # Define local path to save scripts
    os.makedirs(LOCAL_SCRIPT_PATH, exist_ok=True)  # Create the directory if it does not exist

    # Define bucket name and script paths
    bucket_name = "data_parsing"  # Name of the GCS bucket
    gcs_scripts = {  # Dictionary with script names and their GCS paths
        "Design Intent Parsing": "agents/Dual_Agents_for_GCS.py",
        "Requirements Parsing": "agents/Dual_Agents_for_Requirements.py",
        "Non-Compliance Checks": "agents/Agent_for_non_compliances_Checks.py"  # Corrected file path
    }

    # Function to download and save the Python scripts from GCS
    def download_script_from_gcs(bucket_name, gcs_path, local_script_name):
        try:
            bucket = storage_client.bucket(bucket_name)  # Get the bucket from storage client
            blob = bucket.blob(gcs_path)  # Get the blob object representing the file
            local_path = os.path.join(LOCAL_SCRIPT_PATH, local_script_name)  # Define the local path for the file
            blob.download_to_filename(local_path)  # Download the file to the local path
            logging.info(f"Downloaded {gcs_path} to {local_path}")  # Log successful download
            return local_path  # Return the local path of the file
        except Exception as e:
            st.error(f"Failed to download file from GCS: {e}")  # Display error if download fails
            return None

    # Function to load and run a Python script from the given path
    def load_and_run_script(script_path):
        try:
            spec = importlib.util.spec_from_file_location("script_module", script_path)  # Get module spec for script
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)  # Create module from spec
                spec.loader.exec_module(module)  # Execute the script
            else:
                logging.error(f"Could not load the script at {script_path}")  # Log error if script could not be loaded
        except Exception as e:
            logging.error(f"Error while loading the script: {e}")  # Log error if exception occurs while loading script

    # Function to read a file from GCS
    def read_file_from_gcs(bucket_name, file_name):
        try:
            bucket = storage_client.bucket(bucket_name)  # Get the bucket from storage client
            blob = bucket.blob(file_name)  # Get the blob object representing the file
            return blob.download_as_text()  # Download file content as text
        except Exception as e:
            st.error(f"Error reading file from GCS: {e}")  # Display error if reading fails
            return None

    # Function to read an Excel file from GCS
    def read_excel_from_gcs(bucket_name, file_name):
        try:
            bucket = storage_client.bucket(bucket_name)  # Get the bucket from storage client
            blob = bucket.blob(file_name)  # Get the blob object representing the file
            excel_data = blob.download_as_bytes()  # Download file content as bytes
            return pd.read_excel(pd.io.common.BytesIO(excel_data))  # Load content into a DataFrame
        except Exception as e:
            st.error(f"Error reading Excel file from GCS: {e}")  # Display error if reading fails
            return None

    # Function to run a script in a separate thread to prevent UI hang
    def run_script_in_thread(target, *args):
        thread = threading.Thread(target=target, args=args)  # Create a new thread to run the target function
        thread.start()  # Start the thread

    # Main Page Content
    st.title("[ Proposed Solution / PoC]")  # Main header of the page
    st.header("Agent-based Analyser for Technical and Regulatory Requirements Checks")  # Main header of the page

    # Button to run the Design Intent parsing script
    st.subheader("Design Intent - Parse, Calculate & Tabulate")  # Subheader for the section

    st.write("The window schedule below serves as the design intent to be parsed by AI Agent 1.")
    # Add the image with a limited width
    st.image("https://github.com/integrations-space/streamlit/raw/main/design_intent/Window%20Schedule.jpg", width=700)

    st.write("""
    Click the button to allow:
    1. AI Agent 1 to parse the provided window schedule drawing (in jpeg), and calculate the maximum room area using the predefined 10% ventilation requirement.
    2. AI Agent 2 to clean, tabulate and save as Excel output for the next AI Agent to check.
    """)  # Description of the process

    if st.button("Run Design Intent Parsing Script"):  # Button to trigger script execution
        with st.spinner("Downloading and Running Design Intent Parsing Script..."):  # Spinner to indicate processing
            local_path = download_script_from_gcs(bucket_name, gcs_scripts["Design Intent Parsing"], "Dual_Agents_for_GCS.py")  # Download script
            if local_path:
                run_script_in_thread(load_and_run_script, local_path)  # Run script in a separate thread
        time.sleep(2)  # Pause to allow thread to start

        # Display the output
        st.write("The current generated output.")
        file_name = "parsed_output/window_schedule.xls"  # File name of the output
        df = read_excel_from_gcs(bucket_name, file_name)  # Read Excel output from GCS
        if df is not None:
            st.write("Content of the Excel file:")  # Header to indicate content display
            st.dataframe(df)  # Display the DataFrame

        # Embed the Google Sheet using iframe
        st.write("The past successfully generated output.")
        st.components.v1.iframe(
            src="https://docs.google.com/spreadsheets/d/1bACiCjdRTD_eVxbgoeJPV0YjLFs_rth9/edit?usp=sharing&ouid=111462678514080289565&rtpof=true&sd=true",  # Preview link for the spreadsheet
            width=700,  # Set width as per requirement
            height=500  # Height can be adjusted as needed
        )

    # Button to run the requirements parsing script
    st.subheader("Requirements - Parse & Compare")  # Subheader for the requirements parsing section
    st.markdown("[BCA Approvd Doc](https://drive.google.com/file/d/1avFLNumtOzi3mvDwA3aHBlsY2sJ_QxlD/view?usp=drive_link)")
    st.markdown("[SCDF Chapter 4](https://drive.google.com/file/d/1aAfxhjrRiGutbrIuDIm1SSOk8KGeHCV3/view?usp=drive_link)")
    st.write("""
    Click the button to allow:
    1. Agent 3 to analyze compliance-related requirements with the provided PDF documents from Google Cloud Storage.
    2. Agent 4 to extract and summarize key information from regulatory documents, providing structured analysis on specific requirements.
    """)  # Description of the process

    if st.button("Run Requirements Parsing Script"):  # Button to trigger script execution
        with st.spinner("Downloading and Running Requirements Parsing Script..."):  # Spinner to indicate processing
            local_path = download_script_from_gcs(bucket_name, gcs_scripts["Requirements Parsing"], "Dual_Agents_for_Requirements.py")  # Download script
            if local_path:
                run_script_in_thread(load_and_run_script, local_path)  # Run script in a separate thread
        time.sleep(2)  # Pause to allow thread to start

        # Display the output
        st.write("The current generated output.")
        file_name = "parsed_output/Requirements.txt"  # File name of the output
        content = read_file_from_gcs(bucket_name, file_name)  # Read text output from GCS
        if content:
            st.write("Content of the file:")  # Header to indicate content display
            st.text_area("File Content", content, height=300)  # Display content in a text area

        # Embed the Google Sheet using iframe
        st.write("The past successfully generated output.")
        st.components.v1.iframe(
            src="https://drive.google.com/file/d/1fXobXBEP9Nl0XdJQnL4E_tPBM8SGP2MN/preview",  # Preview link for the file
            width=700,  # Set width as per requirement
            height=500  # Height can be adjusted as needed
        )

    # Button to run the non-compliance checks script
    st.subheader("Output - Checks and Recommend")  # Subheader for the non-compliance checks section
    st.write("""
    Click the button to allow:
    1. Agent 5 to use the provided window schedule as design requirements to check against regulatory requirements and provide recommendations for compliance.
    2. BCA Approved Doc & SCDF Chapter 4 are provided as default requirements for the checks and recommendations.
    """)  # Description of the process

    if st.button("Run Compliance Check Script"):  # Button to trigger script execution
        with st.spinner("Downloading and Running Compliance Check Script..."):  # Spinner to indicate processing
            local_path = download_script_from_gcs(bucket_name, gcs_scripts["Non-Compliance Checks"], "Agent_for_non_compliances_Checks.py")  # Corrected file path
            if local_path:
                run_script_in_thread(load_and_run_script, local_path)  # Run script in a separate thread
        time.sleep(2)  # Pause to allow thread to start

        # Display the output
        st.write("The current generated output.")
        file_name = "parsed_output/check_1.xlsx"  # File name of the output
        df = read_excel_from_gcs(bucket_name, file_name)  # Read Excel output from GCS
        if df is not None:
            st.write("Content of the Excel file:")  # Header to indicate content display
            st.dataframe(df)  # Display the DataFrame

        # Embed the Google Sheet using iframe
        st.write("The past successfully generated output.")
        st.components.v1.iframe(
            src="https://docs.google.com/spreadsheets/d/1p0ShM-unKG_FG-fr0bBnc6MB4OY7nG3V/edit?usp=sharing&ouid=111462678514080289565&rtpof=true&sd=true",  # Preview link for the spreadsheet
            width=700,  # Set width as per requirement
            height=500  # Height can be adjusted as needed
        )


    # New Section: GPT-4o-Mini Text File Parsing
    st.header("Validation - explore the use of GPT-4o-Mini Text File Parsing for topic-focused requirements")  # Header for GPT-4o-Mini validation section
    st.write("Click the link below to open the GPT-4o-Mini application for text file parsing in a new tab.")  # Instruction to the user

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
    st.markdown(button_html, unsafe_allow_html=True)  # Render the button with specified styling

    # Section: Presentation Link
    st.header("Presentation Slides")  # Header for presentation section
    st.write("Click the link below to view the presentation slides for the project:")  # Instruction to the user
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
        <a href="https://drive.google.com/file/d/1mEflC7czp3CMtGiBjS7GmphLBcTsNX4R/view?usp=drive_link" target="_blank" class="button">Presentation Slides</a>
    """
    # Display the styled button
    st.markdown(button_html, unsafe_allow_html=True)  # Render the button with specified styling
elif selected_page == "Documentation":
    load_protected_page("documentation")  # Load the documentation page
elif selected_page == "Disclaimer":
    load_protected_page("disclaimer")  # Load the disclaimer page
elif selected_page == "Acknowledgement":
    load_protected_page("acknowledgement")  # Load the acknowledgement page
elif selected_page == "AI Models' Comparison":
    load_protected_page("comparison")  # Load the comparison page
