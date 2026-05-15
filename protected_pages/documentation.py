import streamlit as st

# Define the Streamlit app
def app():
    st.title("[ Documentation ]")
    st.info("📝 Revised 2024 Google Vertex AI with 2026 BYOK Free Tier AI Tokens use")

    st.header("Agent-Based Analyser for Technical and Regulatory Requirements Checks")
    st.subheader("for AI BootCamp 2024 by GovTech")

    st.header("Overview")
    st.markdown("""
<s style="color:#888">This page documents the process of building an Agent-Based Analyser using Vertex AI to parse, clean, analyse, and export project data to Excel for stakeholder review.</s><br><span style="color:#4FC3F7">This page documents the process of building an Agent-Based Analyser using a <strong>Bring Your Own Key (BYOK)</strong> approach — visitors supply their own free-tier or paid API key from Gemini, OpenAI, Groq, or Mistral, and the same code path (powered by LiteLLM in <code>parsers/byo_agent.py</code>) parses, cleans, analyses, and exports project data to Excel for stakeholder review.</span>
    """, unsafe_allow_html=True)

    st.header("Introduction")
    st.subheader("Problem Statement")
    st.write("""
    The construction industry still relies on manual checks to verify design intent against building specifications and regulations. This process is time-consuming and introduces compliance risks.
    """)

    st.subheader("Proposed Solution")
    st.markdown("""
<s style="color:#888">The proposed solution automates checks using Vertex AI agents to parse project data, extract relevant information, and perform compliance checks.</s><br><span style="color:#4FC3F7">The proposed solution automates checks using a dual-agent pipeline (5 agents) that the visitor runs with their own API key. No Vertex AI project, no service account, no GCS — just paste a key and run.</span>
    """, unsafe_allow_html=True)

    st.subheader("Users & Impact")
    st.write("""
    Industry practitioners, contractors, suppliers, and public officers benefit from automated analysis and improved efficiency in verifying design and compliance.
    """)

    st.markdown("""
<s style="color:#888"><h2>Setting Up Google Cloud and Vertex AI</h2>
1. Create a Google Cloud Project and enable necessary APIs.<br>
2. Set up authentication and service accounts for using Google services such as Vertex AI and Cloud Storage.</s>
    """, unsafe_allow_html=True)

    st.markdown("""
<span style="color:#4FC3F7"><h2>Setting Up BYOK Access</h2>
1. Get a free API key from any supported provider:<br>
&nbsp;&nbsp;&nbsp;• <strong>Gemini</strong> (free tier): <a href="https://aistudio.google.com/apikey">aistudio.google.com/apikey</a><br>
&nbsp;&nbsp;&nbsp;• <strong>Groq</strong> (free tier): <a href="https://console.groq.com/keys">console.groq.com/keys</a><br>
&nbsp;&nbsp;&nbsp;• <strong>OpenAI</strong> (paid): <a href="https://platform.openai.com/api-keys">platform.openai.com/api-keys</a><br>
&nbsp;&nbsp;&nbsp;• <strong>Mistral</strong> (limited free trial): <a href="https://console.mistral.ai/api-keys/">console.mistral.ai/api-keys</a><br>
2. Open the "Proposed Solution / PoC" page, expand the 🔑 panel under each section, paste the key, and run. Your key is sent only to the chosen provider and is never stored or logged by this app.</span>
    """, unsafe_allow_html=True)

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
    st.markdown("""
- Use the navigation bar on the left to switch between different pages.
- Upload the respective files to perform parsing and compliance checks.
- <s style="color:#888">[For this PoC, default datasets are provided and stored in Google Cloud Storage (GCS) for parsing. The generated output will also be stored in GCS and displayed upon task completion.]</s><br><span style="color:#4FC3F7">[For this PoC, default datasets (window schedule JPEG + regulatory PDFs) are bundled in the GitHub repo. The generated output is shown directly in the browser and can be downloaded locally as Excel or Markdown — no cloud storage involved.]</span>
    """, unsafe_allow_html=True)

    st.header("Challenges and Best Practices")
    st.markdown("""
- **Functionality & User Experience**: Engaging different models to replace parsing functions, limited time for a quick learning-while-doing approach, engaging GovTech provided guides and advice.
- <s style="color:#888">**Technical Implementation**: Proper use of Vertex AI tools, comparisons of different tools, prompt engineering techniques for effective outcomes.</s><br><span style="color:#4FC3F7">**Technical Implementation**: Refactored from Vertex AI + GCS to a provider-neutral BYOK architecture via LiteLLM. Same prompts run unchanged across Gemini, OpenAI, Groq, and Mistral, with PyPDF2 for regulatory PDF text extraction.</span>
- **Innovation**: Implement AI Agentic workflow to streamline programming processes and automate actual practice processes using LLM with a user-interactive approach.
    """, unsafe_allow_html=True)

    st.header("Conclusion")
    st.write("""
    This documentation aims to serve as a reference for users and developers looking to set up, use, and extend this application.
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="Documentation", page_icon="📋", layout="wide")
    app()
