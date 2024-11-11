import streamlit as st
import pandas as pd

# Define the Streamlit app
def app():
    st.title("[ Acknowledgement ]")
    st.subheader("**Special Thanks**")
    st.write("""
            - We appreciate the support and guidance from our GovTech AI BootCamp Programme Lead, Nick Tan, for his patience and mentorship throughout the project development.
            - A special mention to Mr. Timothy Tang for his assistance with Python coding and Google Vertex AI setup, which significantly accelerated the project development.
    """)
    col1, col2 = st.columns(2)

    # Use markdown for links since link_button is not a valid function
    with col1:
        st.image("https://raw.githubusercontent.com/integrations-space/streamlit/main/pictures/Nick.jpg", width=100)  # Updated URL to use the raw version
        st.write("Mr. Nick TAN (GovTech Lead)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/nick-tsy/)")  
    
    with col2:
        st.image("https://raw.githubusercontent.com/integrations-space/streamlit/main/pictures/Timothy.jpg", width=100)  # Updated URL to use the raw version
        st.write("Mr. Timothy TANG (Tech Support)")
        st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/timothy-tang-xephori/)")

    st.subheader("**Important Support**")
    st.write("""   
            - We believe it is a must to express our gratitude to our beloved families, forgiving bosses, and supportive friends involved.
    """)
       
    st.subheader("**Tools Used**")
    st.write("""
            - Besides GitHub, Streamlit, and many Python packages involved, Google Vertex AI and OpenAI models used in the proposed solution/PoC, we would also like to acknowledge OpenAI (developer of ChatGPT-4 and ChatGPT-4 with Canvas) and Perplexity AI, which supported our learning journey for this project.
   """)
  

if __name__ == "__main__":
    # Use st.set_page_config to ensure the page is properly configured
    st.set_page_config(page_title="Acknowledgement", page_icon="📋", layout="wide")
    app()
