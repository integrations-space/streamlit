import streamlit as st

# Define the Streamlit app
def app():
    st.header("[ Methodology ]")
    st.write("""
    This page provides a comprehensive overview of the data flows and implementation details used in the application.
    The methodology covers data extraction, AI model utilization, and compliance checks through a structured flow.
    
    **Data Flows and Implementation Details**:
    - The project uses various Google Cloud services to store and manage the data (e.g., GCS for document storage).
    - AI Agents are responsible for parsing, analyzing, and validating information extracted from input documents.
    
    **Flowchart**:
    Below are flowcharts illustrating the process flow for each use case in the application:
    
    1. **Chat with Information**: Represents the flow where users interact with the AI to gain insights from regulatory documents.
    2. **Intelligent Search**: Shows the process of extracting and searching for specific requirements or standards from the documents.
    
    ![Flowchart Image](https://raw.githubusercontent.com/integrations-space/streamlit/main/pictures/WorkflowDiagram.jpg)
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Methodology", page_icon="📋", layout="wide")
    app()
