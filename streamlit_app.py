import streamlit as st
import subprocess
import pandas as pd
import numpy as np
import ifcopenshell
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

# Set the title for the application
st.title('Agent-based Analyser for Technical and Regulatory Requirements Checks')

# Intro text
st.write("""
This application provides tools for file parsing, compliance checks, IFC integration, and access to a GPT-based text file parsing tool.
Use the buttons below to run different parsing scripts, or browse through additional resources.
""")

# Section: Run Parsing Scripts
st.header("Run Parsing and Compliance Check Scripts")

# Define paths to the parser scripts
path_to_non_compliance_script = r"C:\2024_ABC\ants_streamlit\parsers\Agent_for_non-compliances_Checks.py"
path_to_gcs_parsing_script = r"C:\2024_ABC\ants_streamlit\parsers\Dual_Agents_for_GCS.py"
path_to_requirements_parsing_script = r"C:\2024_ABC\ants_streamlit\parsers\Dual_Agents_for_Requirements.py"

# Button to run the non-compliance checks script
if st.button("Run Compliance Check Script"):
    with st.spinner("Running Compliance Check..."):
        result = subprocess.run(["python", path_to_non_compliance_script], capture_output=True, text=True)
    st.write("Output from Compliance Check Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/check_1.xlsx"
    df = read_excel_from_gcs(bucket_name, file_name)
    st.write("Content of the Excel file:")
    st.dataframe(df)  # Displaying the DataFrame in the app

# Button to run the GCS parsing script
if st.button("Run GCS Parsing Script"):
    with st.spinner("Running GCS Parsing..."):
        result = subprocess.run(["python", path_to_gcs_parsing_script], capture_output=True, text=True)
    st.write("Output from GCS Parsing Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/window_schedue.xls"
    df = read_excel_from_gcs(bucket_name, file_name)
    st.write("Content of the Excel file:")
    st.dataframe(df)  # Displaying the DataFrame in the app

# Button to run the requirements parsing script
if st.button("Run Requirements Parsing Script"):
    with st.spinner("Running Requirements Parsing..."):
        result = subprocess.run(["python", path_to_requirements_parsing_script], capture_output=True, text=True)
    st.write("Output from Requirements Parsing Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error(result.stderr)

    # Input for GCS bucket name and file name
    bucket_name = "data_parsing"
    file_name = "parsed_output/Requirements.txt"
    content = read_file_from_gcs(bucket_name, file_name)
    st.write("Content of the file:")
    st.text_area("File Content", content, height=300)

# IFC File Parsing Section
st.header("IFC File Parsing")

# Button to run the IFC parsing script (inline script for consistency)
ifc_file_path = st.text_input("Enter the file path for the IFC file:")

if st.button("Run IFC Parsing Script"):
    if ifc_file_path:
        try:
            # Load the IFC file
            ifc_file = ifcopenshell.open(ifc_file_path)
            st.success("IFC file loaded successfully!")

            # Parse IFC file properties
            psets = ifc_file.by_type("IfcPropertySet")
            df = pd.DataFrame(columns=["Pset", "Property", "Value"])

            for pset in psets:
                for prop in pset.HasProperties:
                    value = prop.NominalValue.wrappedValue if hasattr(prop.NominalValue, 'wrappedValue') else str(prop.NominalValue)
                    df = pd.concat([df, pd.DataFrame({"Pset": [pset.Name], "Property": [prop.Name], "Value": [value]})], ignore_index=True)

            # Show the DataFrame in a table using Streamlit
            st.write("Parsed IFC Properties:")
            st.write(df)

        except FileNotFoundError:
            st.error("The file could not be found. Please check the file path and try again.")
        except Exception as e:
            st.error(f"An error occurred while parsing the IFC file: {e}")
    else:
        st.warning("Please enter a file path for the IFC file before running the parser.")

# New Section: GPT-4o-Mini Text File Parsing
st.header("GPT-4o-Mini Text File Parsing")

st.write("Click the button below to open the GPT-4o-Mini application for text file parsing in a new tab.")

if st.button("Open GPT-4o-Mini Text File Parser"):
    webbrowser.open_new_tab("https://bca-project.streamlit.app/")
    st.success("Opened GPT-4o-Mini Text File Parser in a new browser tab.")

# Additional Information Section
st.header("Additional Resources for BIM and IFC Development")

st.write("""
Here are some useful resources for working with BIM, IFC, and Python development tools:
- [Programming with GitHub](https://github.com)
- [IFC File Manipulation with Python](http://blog.ifcopenshell.org/)
- [Blender for IFC](https://blenderbim.org/docs-python/ifcopenshell/installation.html)
- [Visual Studio Code for Python](https://code.visualstudio.com/docs/python/python-tutorial)
- [Dynamo Resources](https://www.youtube.com/watch?v=lvO2_0IQ8vQ)
""")
