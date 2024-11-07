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
        st.write("Mr. PONG Woon Wei")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/woonwei/)")  
    with col2:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/unni.jpg", width=100, use_column_width=False) 
        st.write("Mr. Unni Krishnan AMBADY")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/unni-krishnan-ambady-0287a4164)")
         
    st.header("**About the Project**")
    st.write("""
            The project was developed as the final assignment for the AI Bootcamp under the Project B category to address key challenges in the building and construction industry. 
            With a focus on simplifying and automating repetitive checks, reducing non-compliance risks, and improving workflows to ease the burden on project stakeholders, we are building a use case that leverages AI-powered agents to augment manual processes, detailed below.

            Objectives:

            - Improve compliance checks through automation
            - Streamline document parsing to reduce manual workload
            - Deliver AI-driven recommendations to accelerate design and checking processes
                        
            Scope:

            - Focus on window schedules, BCA-approved documents, and SCDF requirements and use these datasets as defaults for testing and refinement
                        
            Strategies:

            - Employ AI agents, LLMs, and different AI models to enhance efficiency and accuracy
            - Use non-sensitive data and host it on public cloud platforms, such as Google Cloud Storage (GCS) and GitHub
            - Use Streamlit for rapid website development
                        
            Benefits:

            - Saves time by simplifying the understanding of regulatory requirements
            - Reduces manual work in design checks with real-time guidance
            - Modular functions allow for continuous updates and further development
                        
            Data:

            - Window Schedule (jpeg format)
            - BCA Approved Documents, SCDF Fire Code 2023 Chapter 4 (pdf format)
            - Documents from users or generated output (xls and/or txt formats)
                        
            Features:

            - AI-driven parsing and tabulation of design requirements with Google AI model gemini-1.5-pro-002
            - Automated data processing, analysis, and generation of recommendations for design compliance considerations with Google AI model gemini-1.5-pro-002
            - Interactive interface for regulatory requirement checks and validations using OpenAI model gpt-4o-mini
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.experimental_set_page_config to ensure page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
