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
            (from [AI Hackathon](https://www.aihackathon.pro/p/topics.html) topic 1)

            Objectives:

            - Develop a Proof of Concept (PoC) to demonstrate the solution’s feasibility using a common building component, with a scalable method and approach
            - Streamline manual workload and improve compliance checks through AI-powered solution

            PoC Scope:

            - Use a window schedule as the design intent to check for compliance or non-compliance with relevant requirements.

            PoC Benefits:

            - Saves time by simplifying the understanding of regulatory requirements
            - Reduces manual work in design checks with real-time guidance
            - Modular functions allow for continuous updates and further development

            PoC Strategies:

            - Employ AI agents, LLMs, and different AI models to enhance efficiency and accuracy
            - Use non-sensitive data and host it on public cloud platforms, such as Google Cloud Storage (GCS) and GitHub
            - Use Streamlit for rapid website development

            PoC Data:

            - Window Schedule (jpeg format)
            - BCA Approved Documents, SCDF Fire Code 2023 Chapter 4 (pdf format)
            - Documents from users or generated output (xls and/or txt formats)
 
            PoC Features:

            - AI-driven parsing and tabulation of design requirements with Google AI model gemini-1.5-pro-002
            - Automated data processing, analysis, and generation of recommendations for design compliance considerations with Google AI model gemini-1.5-pro-002
            - Interactive interface for regulatory requirement checks and validations using OpenAI model gpt-4o-mini
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.experimental_set_page_config to ensure page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
