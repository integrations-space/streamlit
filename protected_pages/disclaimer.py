import streamlit as st

# Define the Streamlit app
def app():
    st.title("[ Disclaimer ]")
    st.write("""
    - This web application is a proof of concept developed for learning purposes only. 
    - LLM may generate inaccurate or incorrect information. 
    - Take full responsibility for how you use any generated output.
    - Consult qualified professionals for accurate and personalised advice.
    """)
    st.info("Information provided here is NOT ready to be relied upon for making any decisions, especially those related to financial, legal, construction-related matters, or any other actual real-life applications.")
# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Disclaimer", page_icon="⚠️", layout="wide")
    app()
