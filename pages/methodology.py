import streamlit as st

# Define the Streamlit app
def app():
    st.header("[ Methodology ]")
    st.write("""
    This page provides a comprehensive overview of the implementation details and workflow for the proof of concept. The methodology covers data extraction from the provided non-sensitive data, stored at Google Cloud Storage (GCS), using different AI models for processing, analysis, and compliance checks through modular applications.  

    Data Input:
    - A preliminary dataset, consisting of window_schedule.jpg, approveddoc.pdf, and scdf_chapter_4.pdf, serves as the initial input for the applications.
    
    Implementation using AI agents, with outputs stored in GCS:
    - Agent 1 and Agent 2 produce structured data in Excel format (window_schedule.xls).
    - Agent 2 and Agent 4 translate the PDF documents into text format, saved as Requirements.txt.
    - Agent 5 generates a structured output named check01.xls based on window_schedule.xls and Requirements.txt.
    - An independent UI, based on the OpenAI model, was developed to validate uploaded text files according to users' specific queries.   
    
    AI Models used for different purposes:
    - Parsing Design Intent and Requirements (using the Google Gemini-1.5-Pro-002 model): Extract, parse, clean, and tabulate data into structured formats for easier understanding and usage.
    - OpenAI-Powered Validation (using the OpenAI GPT-4o-mini model): Validate information accuracy by allowing users to upload data and request specific checks.

    ![Flowchart Image](https://raw.githubusercontent.com/integrations-space/streamlit/main/pictures/WorkflowDiagram.jpg)
    - 
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Methodology", page_icon="📋", layout="wide")
    app()
