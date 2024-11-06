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
        st.write("Senior Manager @ Digitalisation, CPQ, BCA (Lead)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/woonwei/)")  
    with col2:
        st.image("https://github.com/integrations-space/streamlit/raw/main/pictures/unni.jpg", width=100, use_column_width=False) 
        st.write("Mr. Unni Krishnan AMBADY")
        st.write("Senior Lecturer @ BCA ACADEMY (Member)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/unni-krishnan-ambady-0287a4164)")
         
    st.header("**About the Project**")
    st.write("""
    This project aims to provide a structured approach to analyzing technical and regulatory requirements in the building and construction industry. 
    Our key objectives include improving compliance checks, automating document parsing, and providing AI-driven recommendations to streamline the design and approval process.
    
    **Project Scope**: Covers regulatory requirements parsing, compliance checks, and validation using modern AI tools such as OpenAI and Vertex AI.
    
    **Data Sources**: Using technical drawings (jpg), regulatory requirements (pdf) and documents (xls & txt) hosted in Google Cloud Storage (GCS).
    
    **Features**:
    - AI-driven parsing and tabulation of design requirements.
    - Compliance analysis and non-compliance recommendation generation.
    - Interactive interface for regulatory requirement checks and validations.
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.experimental_set_page_config to ensure page is properly configured
    st.set_page_config(page_title="About Us", page_icon="📋", layout="wide")
    app()
