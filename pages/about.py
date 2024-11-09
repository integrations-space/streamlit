import streamlit as st
import pandas as pd

# Define the Streamlit app
def app():
    st.title("[ About Us ]")
    st.header("**Who are we**")
    
    col1, col2 = st.columns(2)
        # Use markdown for links since link_button is not a valid function
    with col1:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/ww.jpg", width=100, use_column_width=False) 
        st.write("Mr. PONG Woon Wei (Lead)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/woonwei/)")  
    with col2:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/unni.jpg", width=100, use_column_width=False) 
        st.write("Mr. Unni Krishnan AMBADY")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/unni-krishnan-ambady-0287a4164)")
         
    st.header("**About the Project**")
    st.write("""
            This project was developed for learning purposes as the final assignment for the GovTech AI Bootcamp under the Project B category, with an aim to address real challenges in the construction industry. 
            Below are some of the considerations outlined for this project.
            
            Key question: 

            - How can we simplify and automate repetitive checks, reduce non-compliance risks, and improve workflows to ease the work burden on project stakeholders?
            (referencing [AI Hackathon](https://www.aihackathon.pro/p/topics.html) topic 1)

            Objective:

            - Develop a scalable Proof of Concept (PoC) using a common building component to demonstrate how an AI-powered solution can automate repetitive checks, reduce non-compliance risks and manual workloads.
            
            PoC Scope:

            - Use a window schedule as the design intent to check for compliance with relevant BCA-approved documents and SCDF Chapter 4 requirements.

            PoC Benefits:

            - Work Efficiency: Simplifies understanding of regulatory requirements, speeding up design processes.
            - Reduced Manual Effort: Automates design checks, providing real-time guidance and feedback.
            - Scalability: Modular functions allow for continuous updates and further development.

            PoC Strategies:

            - Employ AI agents, LLMs, and different AI models to enhance efficiency and accuracy
            - Use non-sensitive data and host it on public cloud platforms, such as Google Cloud Storage (GCS) and GitHub
            - Use Streamlit for rapid website development

            PoC Data:

            - Window Schedule (jpeg format)
            - BCA Approved Documents, SCDF Fire Code 2023 Chapter 4 (pdf format)
            - Documents from users or generated output (xls and/or txt formats)
 
            PoC Features:

            - AI-Driven Parsing: Automated extraction and tabulation of design requirements using Google AI model Gemini-1.5-Pro-002
            - Data Analysis & Recommendations: AI-powered data processing to analyze compliance and generate design recommendations
            - Interactive Validation Interface: Real-time regulatory checks using OpenAI’s GPT-4o-Mini model for enhanced user interaction
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.experimental_set_page_config to ensure page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
