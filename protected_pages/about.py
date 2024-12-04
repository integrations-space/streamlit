import streamlit as st
import pandas as pd

# Define the Streamlit app
def app():
    st.title("[ About ]")

    # About the Project Section
    st.header("**The Project**")
    st.write("""
        This project was developed for learning purposes as the final assignment for the GovTech AI Bootcamp under the Project B category, with the aim of addressing real challenges in the construction industry. 
        Below are some of the considerations outlined for this project.
        
        **Key Question**: 

        - How can we simplify and automate repetitive checks, reduce non-compliance risks, and improve workflows to ease the work burden on project stakeholders?
          (referencing [AI Hackathon](https://www.aihackathon.pro/p/topics.html) topic 1)

        **Objective**:

        - Develop a scalable Proof of Concept (PoC) using a common building component to demonstrate how an AI-powered solution can automate repetitive checks, reduce non-compliance risks, and minimize manual workloads.
        
        **Scope**:

        - Use a window schedule as the design intent to check for compliance with relevant BCA-approved documents and SCDF Chapter 4 requirements.

        **Benefits**:

        - **Work Efficiency**: Simplifies understanding of regulatory requirements, speeding up design processes.
        - **Reduced Manual Effort**: Automates design checks, providing real-time guidance and feedback.
        - **Scalability**: Modular functions allow for continuous updates and further development.

        **Strategies**:

        - **AI-Driven Workflow**: Use AI tools and language models to improve efficiency and accuracy in compliance checks.
        - **Simple Data Hosting**: Store non-sensitive data on Google Cloud Storage (GCS) and GitHub for scalable and easy cloud setup.
        - **Fast Web Development**: Use Streamlit for quick, interactive website creation to enhance user experience.

        **Data**:

        - **Input**: Window schedules (JPEG format), BCA-approved documents, and SCDF Fire Code 2023 Chapter 4 (PDF format).
        - **Output**: Processed documents and recommendations (XLS and/or TXT formats) generated by AI models.
    
        **Features**:

        - **AI-Driven Parsing**: Automated extraction and tabulation of design requirements using Google AI model Gemini-1.5-Pro-002.
        - **Data Analysis & Recommendations**: AI-powered data processing to analyze compliance and generate design recommendations.
        - **Interactive Validation Interface**: Real-time regulatory checks using OpenAI’s GPT-4o-Mini model for enhanced user interaction.
    """)

    st.header("**Who are we?**")
    
    col1, col2 = st.columns(2)

    # Use markdown for links since link_button is not a valid function
    with col1:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/ww.jpg", width=100) 
        st.write("Mr. PONG Woon Wei (Lead)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/woonwei/)")  
        st.write("Explore the use of AI agents for data parsing, analysis, and reporting [gemini-1.5-pro-002]")
        st.markdown("[aianalyser.streamlit.app](https://aianalyser.streamlit.app/)")  


    with col2:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/unni.jpg", width=100) 
        st.write("Mr. Unni Krishnan AMBADY")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/unni-krishnan-ambady-0287a4164)")
        st.write("Explore the use of the OpenAI model as an independent interactive validator to verify generated outputs [gpt-4o-mini]")
        st.markdown("[bca-project.streamlit.app](https://bca-project.streamlit.app/)") 
        
# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure the page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
