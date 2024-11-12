import streamlit as st
import pandas as pd

# Define the Streamlit app
def app():
 
    # Define the data for the AI models
    ai_models_data = {
        "Model": ["Gemini 1.5 Pro-002", "GPT-4o Mini", "GPT-4o", "Llama 2", "Claude 3"],
        "Provider": ["Google DeepMind", "OpenAI", "OpenAI", "Meta AI", "Anthropic"],
        "Parameter Count": ["~600B+", "~80B", "~175B", "70B", "~100B"],
        "Capabilities & Unique Features": [
            "- Advanced multimodal capabilities.\n- High degree of context-awareness, integrates text and visual inputs.\n- Conversational AI, Image Processing, Data Analysis",
            "- General conversational, creative tasks.\n- Light-weight, optimized for low-resource environments.\n- Chatbots, content generation, summaries",
            "- Advanced text generation, reasoning.\n- Strong at complex problem-solving and nuanced text analysis.\n- Enterprise apps, customer support, education",
            "- General-purpose text processing.\n- Open-source friendly, customizable for research.\n- Open research, NLP tasks, conversational AI",
            "- Safety-oriented generative AI.\n- Enhanced focus on safe and ethical AI behaviors.\n- Assistant bots, safe generative output"
        ]
    }

    # Create a pandas DataFrame
    ai_models_df = pd.DataFrame(ai_models_data)


    # Streamlit App
    st.title("[ AI Models' Comparison ]")

    # Display the DataFrame as a table in Streamlit with wider layout
    st.write("Below is the comparison of several AI models excluding Bard and Falcon:")
    st.table(ai_models_df.set_index('Model').style.set_properties(**{'white-space': 'pre-wrap', 'vertical-align': 'top', 'color': '#ffffff'}).set_table_styles([{'selector': 'th', 'props': [('vertical-align', 'top'), ('color', '#ffffff'), ('font-weight', 'bold')]}, {'selector': 'td', 'props': [('vertical-align', 'top'), ('color', '#ffffff')]}]))


    st.header("Opted Models")
    st.write("""
    As a quick start, we have opted the use of:
    \n- Gemini Vertex AI 1.5 Pro-002, suited for its advanced multimodal tasks, supporting deep contextual understanding.
    \n- GPT-4o Mini, an highly efficient and lightweight solution for simple conversational and creative tasks, especially in resource-constrained environments.
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="AI Models Comparisons", page_icon="📋", layout="wide")
    app()

