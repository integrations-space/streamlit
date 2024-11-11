import streamlit as st

# Define the Streamlit app
def app():
    st.title("[ Documentation ]")
    
    st.header("Agent-Based Analyser for Technical and Regulatory Requirements Checks")
    st.subheader("for AI BootCamp 2024 by GovTech")
    
    st.header("Overview")
    st.write("""
    This page documents the process of building an Agent-Based Analyser using Vertex AI to parse, clean, analyse, and export project data to Excel for stakeholder review.
    """)
    
    st.header("Introduction")
    st.subheader("Problem Statement")
    st.write("""
    The construction industry still relies on manual checks to verify design intent against building specifications and regulations. This process is time-consuming and introduces compliance risks.
    """)

    st.subheader("Proposed Solution")
    st.write("""
    The proposed solution automates checks using Vertex AI agents to parse project data, extract relevant information, and perform compliance checks.
    """)

    st.subheader("Users & Impact")
    st.write("""
    Industry practitioners, contractors, suppliers, and public officers benefit from automated analysis and improved efficiency in verifying design and compliance.
    """)

    st.header("Setting Up Google Cloud and Vertex AI")
    st.write("""
    1. Create a Google Cloud Project and enable necessary APIs.
    2. Set up authentication and service accounts for using Google services such as Vertex AI and Cloud Storage.
    """)

    st.header("Developing the Data Parsing, Analysis and Processing Script")
    st.write("""
    This script demonstrates:
    1. Reading JPEG drawings and PDF data (use case as window/door schedule)
    2. Parsing it into a structured format
    3. Converting to a Pandas DataFrame for analysis
    4. Performing basic calculations as analysis and recommendation
    5. Exporting the outputs into Excel files
    6. Running the Application
    """)

    st.header("Running the Application")
    st.write("""
    - Use the navigation bar on the left to switch between different pages.
    - Upload the respective files to perform parsing and compliance checks. 
    [For this PoC, default datasets are provided and stored in Google Cloud Storage (GCS) for parsing. The generated output will also be stored in GCS and displayed upon task completion.]
    """)

    st.header("Challenges and Best Practices")
    st.write("""
    - Functionality & User Experience: Engaging different models to replace parsing functions, limited time for a quick learning-while-doing approach, engaging GovTech provided guides and advice.
    - Technical Implementation: Proper use of Vertex AI tools, comparisons of different tools, prompt engineering techniques for effective outcomes.
    - Innovation: Implement AI Agentic workflow to streamline programming processes and automate actual practice processes using LLM with a user-interactive approach.
    """)

    st.header("Conclusion")
    st.write("""
    This documentation aims to serve as a reference for users and developers looking to set up, use, and extend this application.
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Documentation", page_icon="📋", layout="wide")
    app()
