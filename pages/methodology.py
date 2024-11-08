import streamlit as st

# Define the Streamlit app
def app():
    st.header("[ Methodology ]")
    st.write("""
    This page provides a comprehensive overview of the data flows and implementation details used in the application.
    The methodology covers data extraction, AI model utilization, and compliance checks through a structured flow.
    
    **Data Flows and Implementation Details**:
    - The project is using Google Cloud Storage (GCS) for data storage and management.
    - AI agents are assigned modular tasks such as data parsing, analysis, cleaning, exporting, and validating information extracted from input documents.
    
    **Flowchart of Data and Workflow**:
    - Parsing Design Intent and Requirements (using the Google Gemini-1.5-Pro-002 model): Extract, parse, clean, and tabulate into structured data for easier understanding and use.
    - OpenAI-Powered Validation (using the OpenAI GPT-4O-Mini model): Validate information accuracy by allowing users to upload data and request specific checks.
    ![Flowchart Image](https://raw.githubusercontent.com/integrations-space/streamlit/main/pictures/WorkflowDiagram.jpg)
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Methodology", page_icon="📋", layout="wide")
    app()
