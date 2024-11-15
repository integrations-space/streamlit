import streamlit as st
import pandas as pd  # Fixed the import

# Define the Streamlit app
def app():
    # Define the data for the AI models
    ai_models_data = {
        "Model": ["Gemini 1.5 Pro", "GPT-4o Mini", "GPT-4o", "Llama 2", "Claude 3 Opus"],
        "Provider": ["Google DeepMind", "OpenAI", "OpenAI", "Meta AI", "Anthropic"],
        "Parameter Count": [
            "Not explicitly disclosed (Mixture-of-Experts architecture)",
            "Estimated ~8B active parameters (MoE architecture)",
            "Estimated 1.8 trillion parameters (MoE architecture)",
            "70B",
            "Not explicitly disclosed, estimated over 2 trillion"
        ],
        "Capabilities & Unique Features": [
            "- Advanced multimodal capabilities across text, images, audio, and video\n"
            "- Massive context window up to 10 million tokens\n"
            "- Efficient Mixture-of-Experts (MoE) architecture\n"
            "- High-performance reasoning and analysis",

            "- Lightweight, cost-efficient AI model\n"
            "- Supports text and vision inputs\n"
            "- Optimized for low-resource environments\n"
            "- Strong performance in reasoning and coding tasks",

            "- Comprehensive multimodal capabilities\n"
            "- Supports text, image, audio, and video inputs\n"
            "- Advanced reasoning and complex problem-solving\n"
            "- Enterprise-grade performance across multiple domains",

            "- Open-source large language model\n"
            "- Customizable for research and specific applications\n"
            "- Strong performance in natural language processing\n"
            "- Versatile across various conversational and analytical tasks",

            "- Advanced multimodal AI with high accuracy\n"
            "- Large context window (200K tokens)\n"
            "- Strong emphasis on safety and ethical AI\n"
            "- Multilingual and vision capabilities"
        ]
    }

    # Create a pandas DataFrame
    ai_models_df = pd.DataFrame(ai_models_data)
  
    # Streamlit App
    st.title("[ AI Models' Comparison ]")

    # Display the DataFrame as a table in Streamlit with wider layout
    st.write("Below is the comparison of several AI models:")
    st.table(
        ai_models_df.set_index('Model')
        .style.set_properties(**{'white-space': 'pre-wrap', 'vertical-align': 'top', 'color': '#ffffff'})
        .set_table_styles([
            {'selector': 'th', 'props': [('vertical-align', 'top'), ('color', '#ffffff'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('vertical-align', 'top'), ('color', '#ffffff')]}
        ])
    )

    st.subheader("Parameter Count and Model Performance")
    
    st.write("""
    #### Overview
    The parameter count of an AI model directly influences its performance, capabilities, and resource requirements. A higher parameter count allows the model to capture more complex patterns and relationships in data, thereby improving its reasoning and accuracy. However, it also requires more computational power.
    
    #### Impact of Parameter Count
    - **Performance & Capabilities**: A higher number of parameters typically means that the model can learn more complex relationships. For example, GPT-3, which has 175 billion parameters, outperforms earlier models like BERT (with 110 million parameters).
    - **Computational Requirements**: Higher parameter counts come at a cost. These models require more computational power and memory to train and operate effectively.

    #### Mixture-of-Experts (MoE) Architecture
    Mixture-of-Experts (MoE) architectures are a method used to optimize resource efficiency. In these architectures, only a subset of the model's parameters ("experts") is activated for any given input. This allows for efficient use of the model's capacity without activating all parameters simultaneously, striking a balance between performance and resource requirements.
    
    #### Examples
    - **Gemini 1.5 Pro and GPT-4o**: Both of these models use MoE architecture, allowing them to have very large numbers of parameters while optimizing which parts of the model are used for each task. This helps in achieving high scalability and efficient resource use.
    """)

    st.info("The relationship between parameter count and model performance is crucial for understanding the trade-offs between accuracy and computational resource requirements.")

    st.subheader("Opted Models")
    st.write("""
    As a quick start, we have opted the use of:
    \n- Gemini Vertex AI 1.5 Pro-002, suited for its advanced multimodal tasks, supporting deep contextual understanding.
    \n- GPT-4o Mini, a highly efficient and lightweight solution for simple conversational and creative tasks, especially in resource-constrained environments.
    """)

    # References Section
    st.subheader("References")
    st.write("""
    - Google DeepMind (2024) 'Gemini 1.5: Unlocking multimodal understanding across millions of tokens'. Available at: https://arxiv.org/abs/2403.05530 (Accessed: 15 November 2024).
    - Google AI (2024) 'Gemini - Google DeepMind'. Available at: https://deepmind.google/technologies/gemini/ (Accessed: 15 November 2024).
    - OpenAI (2024) 'GPT-4o'. Available at: https://en.wikipedia.org/wiki/GPT-4o (Accessed: 15 November 2024).
    - Latenode (2024) 'AI Anthropic Claude 3 Detailed Overview'. Available at: https://latenode.com/blog/ai-anthropic-claude-3-overview (Accessed: 15 November 2024).
    - Encord (2024) 'GPT-4o vs. Gemini 1.5 Pro vs. Claude 3 Opus: Multimodal AI Model Comparison'. Available at: https://encord.com/blog/gpt-4o-vs-gemini-vs-claude-3-opus/ (Accessed: 15 November 2024).
    - Summa Linguae (2024) 'What is GPT-4o mini (and how does it compare to other LLMs?)'. Available at: https://summalinguae.com/language-technology/what-is-gpt-4o-mini-and-how-does-it-compare-to-other-llms/ (Accessed: 15 November 2024).
    - Meta AI (2023) 'Llama 2: Open Foundation and Fine-Tuned Chat Models'. Available at: https://arxiv.org/abs/2307.09288 (Accessed: 15 November 2024).
    - Meta AI (2023) 'Llama 2'. Available at: https://www.llama.com/llama2/ (Accessed: 15 November 2024).
    - Originality.AI (2024) 'Meta Llama 2: Statistics on Meta AI and Microsoft's Open Source LLM'. Available at: https://originality.ai/blog/meta-llama-2-statistics (Accessed: 15 November 2024).
    - DeepLearning (2024) 'AI on Parameter Counts' Available at: https://www.deeplearning.ai/the-batch/trillions-of-parameters/ (Accessed: 15 Novemb 2024).
    - Hugging Face Blog (2024) 'Mixture-of-Experts'  Available at: https://huggingface.co/blog/moe) (Accessed: 15 Novemb 2024).
    """)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="AI Models Comparisons", page_icon="📋", layout="wide")
    app()
