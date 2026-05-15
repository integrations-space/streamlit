import streamlit as st
import pandas as pd
import sys
import logging
import os
import importlib.util
from io import BytesIO

# Set page configuration with correct favicon and title
st.set_page_config(
    page_title="AI Analyser",  # Custom title for the browser tab
    page_icon="https://drive.google.com/file/d/1wk6jJDuOEoMbicSc_o5UuCjhfVe1XZq5/view?usp=sharing",  # Replace with a direct link to your favicon
)
# CSS to hide Streamlit elements including "Manage app"
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
[data-testid="stToolbar"] {visibility: hidden !important;}
[data-testid="stDecoration"] {display: none !important;}  /* Hides "Manage app" */
[data-testid="stStatusWidget"] {visibility: hidden !important;}
[data-testid="stHeader"] {background-color: transparent !important;}
[data-testid="stToolbar"] {right: 2rem !important;}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Setting up logging to handle UnicodeEncodeError
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')  # Logging configuration to send logs to stdout

# Authentication mechanism
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False  # Adding a key to session_state to track authentication status

def authenticate():
    """Function to authenticate the user."""
    st.sidebar.header("Authentication Required")  # Header to prompt user to authenticate
    username = st.sidebar.text_input("Username")  # Username input field
    password = st.sidebar.text_input("Password", type="password")  # Password input field

    if st.sidebar.button("Login"):  # Login button to trigger authentication
        if (username == st.secrets["auth"]["username"] and  # Check if username matches the secret stored
            password == st.secrets["auth"]["password"]):  # Check if password matches the secret stored
            st.session_state.authenticated = True  # Update authentication status on successful login
        else:
            st.sidebar.error("Invalid credentials")  # Error message for invalid credentials

# Authentication check
if not st.session_state.authenticated:
    authenticate()  # Call authenticate function if user is not authenticated
    if not st.session_state.authenticated:
        st.stop()  # Stop the application until the user is authenticated

# Navigation after successful authentication
st.sidebar.title("Navigation")  # Sidebar title for navigation
selected_page = st.sidebar.radio("Select a page:", ["About", "Methodology", "Proposed Solution / PoC", "Documentation", "AI Models' Comparison", "Disclaimer"])  # Sidebar navigation options

# Function to dynamically load a module from the protected_pages directory
def load_protected_page(page_name):
    """Dynamically loads a page module from the protected_pages directory."""
    module_path = os.path.join(os.path.dirname(__file__), "protected_pages", f"{page_name}.py")  # Construct the path to the page module

    # Check if the file exists before attempting to load it
    if not os.path.exists(module_path):
        st.error(f"The requested page '{page_name}' does not exist. Path: {module_path}")  # Display error if file doesn't exist
        return

    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(page_name, module_path)  # Get the module specification
        if spec and spec.loader:
            page_module = importlib.util.module_from_spec(spec)  # Create a module object
            spec.loader.exec_module(page_module)  # Execute the module
            # Check if app() function exists
            if hasattr(page_module, "app"):
                page_module.app()  # Call a function named `app()` within the module to display content
            else:
                st.error(f"The page '{page_name}' does not have an 'app()' function.")  # Error if no app() function is found
        else:
            st.error(f"Failed to load the page '{page_name}'. Module specification issue.")  # Error if module spec is invalid
    except Exception as e:
        st.error(f"An error occurred while loading the page '{page_name}': {str(e)}")  # Error handling for exceptions during module loading

# Display the selected page
if selected_page == "About":
    load_protected_page("about")  # Load the about page
elif selected_page == "Methodology":
    load_protected_page("methodology")  # Load the methodology page
elif selected_page == "Proposed Solution / PoC":
# Create an expander for the notice on errors
    with st.expander("📢   Notice    📢"):
        st.write("""
        - This Proof of Concept (PoC) project has been completed.
        - **📝 Revised 2024 Google Vertex AI with 2026 BYOK Free Tier AI Tokens use** — the original pipeline ran on Vertex AI and Google Cloud Storage; the 2026 revision replaces that with a vendor-neutral **Bring Your Own Key (BYOK)** architecture via LiteLLM (`parsers/byo_agent.py`), so no GCP project, billing, or service account is required.
        - **🔑 Bring your own API key:** the Design Intent and Requirements sections support live runs with your own **Gemini, OpenAI, Groq, or Mistral** key. Gemini and Groq both offer free tiers. Your key is sent only to the provider you choose and is never stored or logged by this app.
        - The Compliance Checks section will get the same BYO-key flow in the next iteration.
        """)
    # Main Page Content
    st.title("[ Proposed Solution / PoC]")  # Main header of the page
    st.header("Agent-based Analyser for Technical and Regulatory Requirements Checks")  # Main header of the page

    # Button to run the Design Intent parsing script
    st.subheader("Design Intent - Parse, Calculate & Tabulate")  # Subheader for the section

    st.write("The window schedule below serves as the design intent to be parsed by AI Agent 1.")
    # Add the image with a limited width
    st.image("https://github.com/integrations-space/streamlit/raw/main/design_intent/Window%20Schedule.jpg", width=700)

    st.write("""
    Click the button to allow:
    1. AI Agent 1 to parse the provided window schedule drawing (in jpeg), and calculate the maximum room area using the predefined 10% ventilation requirement.
    2. AI Agent 2 to clean, tabulate and save as Excel output for the next AI Agent to check.
    """)  # Description of the process

    # Always display the previously generated demo output
    st.write("Previously generated output (for demonstration):")
    st.components.v1.iframe(
        src="https://docs.google.com/spreadsheets/d/1bACiCjdRTD_eVxbgoeJPV0YjLFs_rth9/edit?usp=sharing&ouid=111462678514080289565&rtpof=true&sd=true",
        width=700,
        height=500
    )

    # BYO API key: run live against the bundled window schedule using the visitor's own LLM key
    PROVIDERS = {
        "Gemini (free tier available)": {
            "models": ["gemini/gemini-2.5-flash", "gemini/gemini-2.5-pro", "gemini/gemini-1.5-pro"],
            "key_url": "https://aistudio.google.com/apikey",
            "vendor": "Google",
        },
        "OpenAI": {
            "models": ["openai/gpt-4o-mini", "openai/gpt-4o", "openai/gpt-5"],
            "key_url": "https://platform.openai.com/api-keys",
            "vendor": "OpenAI",
        },
        "Groq (free tier available)": {
            "models": [
                "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "groq/meta-llama/llama-4-maverick-17b-128e-instruct",
                "groq/llama-3.2-90b-vision-preview",
            ],
            "key_url": "https://console.groq.com/keys",
            "vendor": "Groq",
        },
        "Mistral": {
            "models": ["mistral/pixtral-large-latest", "mistral/pixtral-12b-2409"],
            "key_url": "https://console.mistral.ai/api-keys/",
            "vendor": "Mistral",
        },
    }

    with st.expander("🔑 Run with your own API key — Gemini / OpenAI / Groq / Mistral"):
        st.markdown(
            "Bring your own API key — your key is sent **only** to the provider you choose "
            "and is **not stored or logged** by this app."
        )
        provider_name = st.radio(
            "Provider",
            list(PROVIDERS.keys()),
            horizontal=True,
            key="byo_provider",
        )
        provider = PROVIDERS[provider_name]
        st.markdown(f"Get a key from **{provider['vendor']}**: [{provider['key_url']}]({provider['key_url']})")

        col1, col2 = st.columns([3, 2])
        with col1:
            user_api_key = st.text_input(
                f"{provider['vendor']} API key",
                type="password",
                key=f"byo_key_{provider_name}",
            )
        with col2:
            user_model = st.selectbox(
                "Model (vision-capable)",
                provider["models"],
                index=0,
                key=f"byo_model_{provider_name}",
            )

        if st.button("Run with my key", key="byo_run_design_intent"):
            if not user_api_key:
                st.error(f"Please paste your {provider['vendor']} API key first.")
            else:
                from parsers.byo_agent import (
                    parse_schedule_image,
                    format_table,
                    table_text_to_dataframe,
                    dataframe_to_excel_bytes,
                )
                image_path = os.path.join(os.path.dirname(__file__), "design_intent", "Window Schedule.jpg")
                try:
                    with open(image_path, "rb") as f:
                        image_bytes = f.read()
                    with st.spinner(f"Agent 1 ({user_model}): extracting schedule from image..."):
                        raw_table = parse_schedule_image(image_bytes, user_api_key, user_model)
                    with st.spinner(f"Agent 2 ({user_model}): cleaning and formatting..."):
                        formatted = format_table(raw_table, user_api_key, user_model)
                    df, schedule_type = table_text_to_dataframe(formatted)
                    st.success(f"Done — parsed as a {schedule_type} schedule using {user_model}.")
                    st.dataframe(df)
                    st.download_button(
                        "Download as Excel",
                        data=dataframe_to_excel_bytes(df),
                        file_name=f"{schedule_type}_schedule.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                except Exception as e:
                    st.error(f"Run failed: {e}")

    # Requirements - Parse & Compare (Agents 3 & 4)
    st.subheader("Requirements - Parse & Compare")  # Subheader for the requirements parsing section
    st.markdown("[BCA Approvd Doc](https://drive.google.com/file/d/1avFLNumtOzi3mvDwA3aHBlsY2sJ_QxlD/view?usp=drive_link)")
    st.markdown("[SCDF Chapter 4](https://drive.google.com/file/d/1aAfxhjrRiGutbrIuDIm1SSOk8KGeHCV3/view?usp=drive_link)")
    st.write("""
    With your own API key, this section will:
    1. **Agent 3** — analyse compliance-related requirements in each of the bundled regulatory PDF documents (BCA Approved Doc & SCDF Chapter 4).
    2. **Agent 4** — extract and summarise the most stringent requirements, potential non-compliances, and recommendations.
    """)  # Description of the process

    # Always display the previously generated demo output
    st.write("Previously generated output (for demonstration):")
    st.components.v1.iframe(
        src="https://drive.google.com/file/d/1fXobXBEP9Nl0XdJQnL4E_tPBM8SGP2MN/preview",
        width=700,
        height=500
    )

    # BYO API key flow for Requirements parsing (Agents 3 & 4)
    with st.expander("🔑 Run with your own API key — Gemini / OpenAI / Groq / Mistral"):
        st.markdown(
            "Bring your own API key — your key is sent **only** to the provider you choose "
            "and is **not stored or logged** by this app."
        )
        req_provider_name = st.radio(
            "Provider",
            list(PROVIDERS.keys()),
            horizontal=True,
            key="byo_provider_req",
        )
        req_provider = PROVIDERS[req_provider_name]
        st.markdown(f"Get a key from **{req_provider['vendor']}**: [{req_provider['key_url']}]({req_provider['key_url']})")

        rc1, rc2 = st.columns([3, 2])
        with rc1:
            req_api_key = st.text_input(
                f"{req_provider['vendor']} API key",
                type="password",
                key=f"byo_key_req_{req_provider_name}",
            )
        with rc2:
            req_model = st.selectbox(
                "Model",
                req_provider["models"],
                index=0,
                key=f"byo_model_req_{req_provider_name}",
            )

        schedule_type = st.radio(
            "Schedule type to analyse",
            ["Window", "Door"],
            horizontal=True,
            key="byo_req_schedule_type",
        )

        if st.button("Run Agents 3 & 4 with my key", key="byo_run_requirements"):
            if not req_api_key:
                st.error(f"Please paste your {req_provider['vendor']} API key first.")
            else:
                from parsers.byo_agent import (
                    extract_pdf_text,
                    run_text_prompt,
                    REQUIREMENTS_EXTRACT_PROMPT_TEMPLATE,
                    REQUIREMENTS_SUMMARY_PROMPT_TEMPLATE,
                    MAX_PDF_CHARS,
                )
                regulatory_dir = os.path.join(os.path.dirname(__file__), "regulatory_requirements")
                pdf_files = [
                    ("BCA Approved Doc", os.path.join(regulatory_dir, "approveddoc.pdf")),
                    ("SCDF Chapter 4", os.path.join(regulatory_dir, "scdf chapter 4.pdf")),
                ]
                try:
                    extracted_sections = []
                    for doc_name, pdf_path in pdf_files:
                        with st.spinner(f"Reading {doc_name}..."):
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()
                            doc_text = extract_pdf_text(pdf_bytes)
                            if len(doc_text) > MAX_PDF_CHARS:
                                st.warning(f"{doc_name}: truncating from {len(doc_text):,} to {MAX_PDF_CHARS:,} chars to fit model context.")
                                doc_text = doc_text[:MAX_PDF_CHARS]
                        with st.spinner(f"Agent 3 ({req_model}): extracting requirements from {doc_name}..."):
                            prompt = REQUIREMENTS_EXTRACT_PROMPT_TEMPLATE.format(
                                schedule_type=schedule_type,
                                doc_name=doc_name,
                                content=doc_text,
                            )
                            extracted = run_text_prompt(prompt, req_api_key, req_model)
                        extracted_sections.append(f"## From {doc_name}\n\n{extracted}")

                    combined = "\n\n---\n\n".join(extracted_sections)
                    with st.spinner(f"Agent 4 ({req_model}): synthesising final summary..."):
                        summary_prompt = REQUIREMENTS_SUMMARY_PROMPT_TEMPLATE.format(
                            schedule_type=schedule_type,
                            combined_extracted=combined,
                        )
                        final_summary = run_text_prompt(summary_prompt, req_api_key, req_model)

                    st.success(f"Done — analysed {len(pdf_files)} regulatory document(s) for {schedule_type} requirements.")
                    st.markdown("### Final Summary (Agent 4)")
                    st.markdown(final_summary)
                    with st.expander("Show per-document extractions (Agent 3)"):
                        st.markdown(combined)
                    st.download_button(
                        "Download summary as Markdown",
                        data=final_summary.encode("utf-8"),
                        file_name=f"requirements_summary_{schedule_type.lower()}.md",
                        mime="text/markdown",
                    )
                except Exception as e:
                    st.error(f"Run failed: {e}")

    # Button to run the non-compliance checks script
    st.subheader("Output - Checks and Recommend")  # Subheader for the non-compliance checks section
    st.write("""
    Click the button to allow:
    1. Agent 5 to use the provided window schedule as design requirements to check against regulatory requirements and provide recommendations for compliance.
    2. BCA Approved Doc & SCDF Chapter 4 are provided as default requirements for the checks and recommendations.
    """)  # Description of the process

    # Always display the previously generated demo output
    st.write("Previously generated output (for demonstration):")
    st.components.v1.iframe(
        src="https://docs.google.com/spreadsheets/d/1p0ShM-unKG_FG-fr0bBnc6MB4OY7nG3V/edit?usp=sharing&ouid=111462678514080289565&rtpof=true&sd=true",
        width=700,
        height=500
    )


    # New Section: GPT-4o-Mini Text File Parsing
    st.header("Validation - explore the use of GPT-4o-Mini Text File Parsing for topic-focused requirements")  # Header for GPT-4o-Mini validation section
    st.write("Click the link below to open the GPT-4o-Mini application for text file parsing in a new tab.")  # Instruction to the user

    # CSS styling to set link color to white with dark gray background and mild red on hover, no underline on hover
    button_html = f"""
        <style>
            .button {{
                background-color: #1a1a1a;
                color: white !important;
                border: 1px solid #444444;
                padding: 5px 7px;
                font-size: 16px;
                border-radius: 8px;
                text-align: center;
                cursor: pointer;
                display: inline-block;
                text-decoration: none;
                transition: color 0.3s ease, border-color 0.3s ease;
            }}
            .button:hover {{
                color: #ff6b6b !important;
                border-color: #ff6b6b;
                text-decoration: none;
            }}
        </style>
        <a href="https://bca-project.streamlit.app/" target="_blank" class="button">Open GPT-4o-Mini Text File Parser</a>
    """
    # Display the styled button
    st.markdown(button_html, unsafe_allow_html=True)  # Render the button with specified styling

    # Section: Presentation Link
    st.header("Presentation Slides")  # Header for presentation section
    st.write("Click the link below to view the presentation slides for the project:")  # Instruction to the user
    # CSS styling to set link color to white with dark gray background and mild red on hover, no underline on hover
    button_html = f"""
        <style>
            .button {{
                background-color: #1a1a1a;
                color: white !important;
                border: 1px solid #444444;
                padding: 5px 7px;
                font-size: 16px;
                border-radius: 8px;
                text-align: center;
                cursor: pointer;
                display: inline-block;
                text-decoration: none;
                transition: color 0.3s ease, border-color 0.3s ease;
            }}
            .button:hover {{
                color: #ff6b6b !important;
                border-color: #ff6b6b;
                text-decoration: none;
            }}
        </style>
        <a href="https://drive.google.com/file/d/1mEflC7czp3CMtGiBjS7GmphLBcTsNX4R/view?usp=drive_link" target="_blank" class="button">Presentation Slides</a>
    """
    # Display the styled button
    st.markdown(button_html, unsafe_allow_html=True)  # Render the button with specified styling
elif selected_page == "Documentation":
    load_protected_page("documentation")  # Load the documentation page
elif selected_page == "Disclaimer":
    load_protected_page("disclaimer")  # Load the disclaimer page
elif selected_page == "Acknowledgement":
    load_protected_page("acknowledgement")  # Load the acknowledgement page
elif selected_page == "AI Models' Comparison":
    load_protected_page("comparison")  # Load the comparison page
