import streamlit as st

def app():
    st.title("[ Documentation ]")
    
    st.write("""
  Agent-Based Analyzer for Technical and Regulatory Requirements Checks
    """)

    st.header("Overview")
    st.write("""
    This documentation provides a comprehensive guide to building an Agent-Based Analyzer using Google Cloud's Vertex AI for parsing project data, analyzing it, and performing calculations and requirement checks.
    """)

    st.subheader("for:")
    st.write("**AI BootCamp by GovTech**")

    st.subheader("prepared By:")
    st.write("PONG Woon Wei, BCA (Lead) & Uni Krishnan Ambady, BCA (Member)")

    st.header("Table of Contents")
    st.write("""
    1. Introduction
    2. Setting Up Google Cloud and Vertex AI 
    3. Developing the Data Parsing and Analysis Script
    4. Running the AI Agent for User Interaction
    5. Streamlit Integration and Streamlit Login
    6. Challenges and Best Practices
    7. Conclusion
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

    st.header("Running the Application")
    st.write("""Developing the Data Parsing and Analysis Script)
    st.write("""
    This script demonstrates:
    1. Reading jpeg drawings and pdf data (use case as window/door schedule)
    2. Parsing it into a structured format
    3. Converting to a pandas DataFrame for analysis
    4. Performing basic calculations as analysis and recommendation
    5. Exporting the outputs into a Excel files

    st.header("Running the Application")
    st.write("""
    - Use the navigation bar on the left to switch between different pages.
    - Upload the respective files to perform parsing and compliance checks.
    """)

    st.header("Challenges and Best Practices")
    st.write("""
    - **Functionality & User Experience**: Engaging different models to replace parsing functions, Limited time for quick learning while doing approach, Engage Govtech provided guides and advice.
    - **Technical Implementation**: Proper use of Vertex AI tools, Comparisons of different tools, Prompt Engineering techniques for effective outcomes.
    - **Innovation**: Implement AI Agentic workflow to streamline programming processes and automating actual practice processes using LLM with user interactive approach.
    """)

    st.header("Conclusion")
    st.write("""
    This documentation aims to serve as a reference for users and developers looking to set up, use, and extend this application.
    """)
