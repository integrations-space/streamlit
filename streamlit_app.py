import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import webbrowser
from google.cloud import storage

# Function to read a file from GCS
def read_file_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.download_as_text()  # Returns the content of the file as text

# Function to read an Excel file from GCS
def read_excel_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the Excel file to a BytesIO object
    excel_data = blob.download_as_bytes()
    
    # Use pandas to read the Excel file from the BytesIO object
    return pd.read_excel(pd.io.common.BytesIO(excel_data))
        
st.title('Regulatory check')

# # Function to run the entire Agent_for_noncompliance_checks.py file
# def run_agent_for_noncompliance_checks():
#     with open("Agent_for_noncompliance_checks.py") as file:
#         exec(file.read())

# Button to run the non-compliance checks script
if st.button("Run Compliance Check Script"):
    with st.spinner("Running Compliance Check..."):
        with open(r"C:\2024_ABC\ants_streamlit\parsers\Agent_for_non-compliances_Checks.py") as file:
            result = exec(file.read())
    st.write("Output from Compliance Check Script:")

    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/check_1.xlsx"
    df = read_excel_from_gcs(bucket_name, file_name)
    st.write("Content of the Excel file:")
    st.dataframe(df)  # Displaying the DataFrame in the app
        

# def run_dual_agents_for_GCS():
#     with open("Dual_Agents_for_GCS.py") as file:
#         exec(file.read())

# Button to run the GCS parsing script
if st.button("Run GCS Parsing Script"):
    with st.spinner("Running GCS Parsing..."):
        with open(r"C:\2024_ABC\ants_streamlit\parsers\Dual_Agents_for_GCS.py") as file:
            result = exec(file.read())
    st.write("Output from GCS Parsing Script:")
    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/window_schedue.xls"
    df = read_excel_from_gcs(bucket_name, file_name)
    st.write("Content of the Excel file:")
    st.dataframe(df)  # Displaying the DataFrame in the app

# def run_dual_agents_for_requirements():
#     with open("Dual_Agents_for_Requirements.py") as file:
#         exec(file.read())

# Button to run the requirements parsing script
if st.button("Run Requirements Parsing Script"):
    with st.spinner("Running Requirements Parsing..."):
        with open(r"C:\2024_ABC\ants_streamlit\parsers\Dual_Agents_for_Requirements.py") as file:
            result = exec(file.read())
    st.write("Output from Requirements Parsing Script:")
    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/Requirements.txt"
    content = read_file_from_gcs(bucket_name, file_name)
    st.write("Content of the file:")
    st.text_area("File Content", content, height=300)

    

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

