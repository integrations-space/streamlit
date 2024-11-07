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
            **Background**: Developed as the final assignment for the AI Bootcamp under the Project B category, this project leverages AI, large language models (LLMs), and online tools to address key challenges in the building and construction industry.
            
            **Objective**: This project aims to enhance the analysis of technical and regulatory requirements in the building and construction industry by improving compliance checks, automating document parsing, and providing AI-driven recommendations.
            
            **Benefits**: This approach helps professionals save time and gain a quicker understanding of regulatory requirements, streamlining design checks. With up-to-date project and regulatory datasets, it offers real-time guidance, identifies potential compliance issues, and provides continuously updated recommendations, transforming manual tasks into efficient, AI-driven workflows.
            
            **Scope**: The project covers regulatory requirements parsing, compliance checks, and validation using a sample dataset, including a window schedule, BCA-approved documents, and a segment of SCDF requirements as default datasets.
            
            **Strategies**: The solution explores modern AI tools, such as OpenAI and Vertex AI, using AI agents and large language models (LLMs) to replace conventional functions where applicable.
            
            **Data**: The project uses technical drawings (JPEG format), regulatory requirements (PDF format), and documents (Excel and txt formats), all hosted in Google Cloud Storage (GCS).
            
            **Features**:
            
            - AI-driven parsing and tabulation of design requirements.
            - Compliance analysis and generation of non-compliance recommendations.
            - Interactive interface for regulatory requirement checks and validations.
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.experimental_set_page_config to ensure page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
