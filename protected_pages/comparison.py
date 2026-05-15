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
            "- Massive context window up to 2 million tokens\n"
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
    st.info("📝 Revised 2024 Google Vertex AI with 2026 BYOK Free Tier AI Tokens use")

    # Display the DataFrame as a table — struck through as a 2024 snapshot;
    # the active BYOK model list is in the "Opted Models" section below.
    st.markdown(
        '<s style="color:#888">Below is the comparison of several AI models (snapshot from the 2024 PoC):</s>'
        '<br><span style="color:#4FC3F7">See <strong>Opted Models</strong> below for the 2026 BYOK provider/model picker that the live PoC actually uses.</span>',
        unsafe_allow_html=True,
    )
    st.table(
        ai_models_df.set_index('Model')
        .style.set_properties(**{
            'white-space': 'pre-wrap',
            'vertical-align': 'top',
            'color': '#888888',
            'text-decoration': 'line-through',
        })
        .set_table_styles([
            {'selector': 'th', 'props': [
                ('vertical-align', 'top'),
                ('color', '#888888'),
                ('font-weight', 'bold'),
                ('text-decoration', 'line-through'),
            ]},
            {'selector': 'td', 'props': [
                ('vertical-align', 'top'),
                ('color', '#888888'),
                ('text-decoration', 'line-through'),
            ]},
        ])
    )

    st.subheader("Parameter Count and Model Performance")

    st.markdown("""
#### Overview
The parameter count of an AI model directly influences its performance, capabilities, and resource requirements. A higher parameter count allows the model to capture more complex patterns and relationships in data, thereby improving its reasoning and accuracy. However, it also requires more computational power.

<div style="color:#4FC3F7;">
<strong>2026 nuance:</strong> raw parameter count is no longer the dominant driver of capability. Training-data quality, post-training (RLHF / DPO), tool use, and architecture choices now contribute as much or more. Small well-trained models — Gemini 2.5 Flash, gpt-4o-mini, Pixtral-12B, Llama 3.2 Vision — often match or beat older models several times their size. This is what makes the free-tier BYOK PoC practical: the cheap models are now genuinely capable.
</div>

#### Impact of Parameter Count
- <strong>Performance & Capabilities</strong>: A higher number of parameters typically means that the model can learn more complex relationships. <s style="color:#888">For example, GPT-3, which has 175 billion parameters, outperforms earlier models like BERT (with 110 million parameters).</s> <span style="color:#4FC3F7">For a 2026-relevant example: Llama 4 Maverick (~400B total / ~17B active params via MoE) competes with dense models several times its active size, while Gemini 2.5 Flash matches earlier Pro-tier performance at a fraction of the cost and latency.</span>
- <strong>Computational Requirements</strong>: Higher parameter counts come at a cost. These models require more computational power and memory to train and operate effectively. <span style="color:#4FC3F7">Sparse / MoE designs and aggressive quantisation (INT8, INT4) have softened this trade-off considerably since 2024.</span>

#### Mixture-of-Experts (MoE) Architecture
Mixture-of-Experts (MoE) architectures are a method used to optimize resource efficiency. In these architectures, only a subset of the model's parameters ("experts") is activated for any given input. This allows for efficient use of the model's capacity without activating all parameters simultaneously, striking a balance between performance and resource requirements.

#### Examples
- <s style="color:#888"><strong>Gemini 1.5 Pro and GPT-4o</strong>: Both of these models use MoE architecture, allowing them to have very large numbers of parameters while optimizing which parts of the model are used for each task. This helps in achieving high scalability and efficient resource use.</s>

<div style="color:#4FC3F7;">
<strong>2026 MoE landscape:</strong>
<ul>
<li><strong>Meta — Llama 4 Scout</strong> (~109B total / ~17B active) and <strong>Llama 4 Maverick</strong> (~400B total / ~17B active): both explicit MoE, available on Groq's free tier and used in this PoC.</li>
<li><strong>DeepSeek-V3</strong> (671B total / 37B active): one of the largest publicly disclosed MoE models.</li>
<li><strong>Mistral — Mixtral 8x7B / 8x22B</strong>: classic 8-expert MoE; Mistral's flagship dense models (Mistral Large, Pixtral) are <em>not</em> MoE.</li>
<li><strong>Google — Gemini 1.5 / 2.5 series</strong>: confirmed MoE; the free-tier <code>gemini-2.5-flash</code> in this PoC is a smaller MoE variant tuned for low-latency inference.</li>
<li><strong>OpenAI — GPT-4o / GPT-5</strong>: architecture not officially disclosed; widely believed to be MoE but not confirmed.</li>
</ul>
</div>
    """, unsafe_allow_html=True)

    st.info("The relationship between parameter count and model performance is crucial for understanding the trade-offs between accuracy and computational resource requirements.")

    st.subheader("Opted Models")
    st.markdown("""
<div style="color:#888">
<s>As a quick start, we have opted the use of:
<ul>
<li>Gemini Vertex AI 1.5 Pro-002, suited for its advanced multimodal tasks, supporting deep contextual understanding.</li>
<li>GPT-4o Mini, a highly efficient and lightweight solution for simple conversational and creative tasks, especially in resource-constrained environments.</li>
</ul>
</s>
</div>

<div style="color:#4FC3F7">
As of the 2026 revision, the PoC no longer pins a single model. With the <strong>Bring Your Own Key (BYOK)</strong> approach (via LiteLLM in <code>parsers/byo_agent.py</code>), visitors choose any vision-capable model from four providers:
<ul>
<li><strong>Gemini</strong> (free tier): gemini-2.5-flash, gemini-2.5-pro, gemini-1.5-pro</li>
<li><strong>OpenAI</strong> (paid): gpt-4o-mini, gpt-4o, gpt-5</li>
<li><strong>Groq</strong> (free tier): llama-4-scout, llama-4-maverick, llama-3.2-90b-vision-preview</li>
<li><strong>Mistral</strong> (limited free trial): pixtral-large-latest, pixtral-12b-2409</li>
</ul>
The same prompts and pipeline run unchanged on whichever model the visitor selects.
</div>
    """, unsafe_allow_html=True)

    # References Section
    st.subheader("References")
    st.markdown("""
<div style="color:#888; text-decoration:line-through;">
<strong>Original PoC (2024 reading list):</strong>
<ul>
<li>Google DeepMind (2024) 'Gemini 1.5: Unlocking multimodal understanding across millions of tokens'. Available at: https://arxiv.org/abs/2403.05530 (Accessed: 15 November 2024).</li>
<li>Google AI (2024) 'Gemini - Google DeepMind'. Available at: https://deepmind.google/technologies/gemini/ (Accessed: 15 November 2024).</li>
<li>OpenAI (2024) 'GPT-4o'. Available at: https://en.wikipedia.org/wiki/GPT-4o (Accessed: 15 November 2024).</li>
<li>Latenode (2024) 'AI Anthropic Claude 3 Detailed Overview'. Available at: https://latenode.com/blog/ai-anthropic-claude-3-overview (Accessed: 15 November 2024).</li>
<li>Encord (2024) 'GPT-4o vs. Gemini 1.5 Pro vs. Claude 3 Opus: Multimodal AI Model Comparison'. Available at: https://encord.com/blog/gpt-4o-vs-gemini-vs-claude-3-opus/ (Accessed: 15 November 2024).</li>
<li>Summa Linguae (2024) 'What is GPT-4o mini (and how does it compare to other LLMs?)'. Available at: https://summalinguae.com/language-technology/what-is-gpt-4o-mini-and-how-does-it-compare-to-other-llms/ (Accessed: 15 November 2024).</li>
<li>Meta AI (2023) 'Llama 2: Open Foundation and Fine-Tuned Chat Models'. Available at: https://arxiv.org/abs/2307.09288 (Accessed: 15 November 2024).</li>
<li>Meta AI (2023) 'Llama 2'. Available at: https://www.llama.com/llama2/ (Accessed: 15 November 2024).</li>
<li>Originality.AI (2024) 'Meta Llama 2: Statistics on Meta AI and Microsoft's Open Source LLM'. Available at: https://originality.ai/blog/meta-llama-2-statistics (Accessed: 15 November 2024).</li>
<li>DeepLearning (2024) 'AI on Parameter Counts'. Available at: https://www.deeplearning.ai/the-batch/trillions-of-parameters/ (Accessed: 15 November 2024).</li>
<li>Hugging Face Blog (2024) 'Mixture-of-Experts'. Available at: https://huggingface.co/blog/moe (Accessed: 15 November 2024).</li>
</ul>
</div>

<div style="color:#4FC3F7;">
<strong>2026 BYOK revision (additional reading):</strong>
<ul>
<li>DeepSeek-AI (2024) 'DeepSeek-V3 Technical Report'. Available at: <a href="https://arxiv.org/abs/2412.19437" style="color:#4FC3F7;">https://arxiv.org/abs/2412.19437</a> — large open-weight MoE (671B total / 37B active).</li>
<li>Meta AI (2025) 'The Llama 4 herd: native multimodal intelligence'. Available at: <a href="https://ai.meta.com/blog/" style="color:#4FC3F7;">https://ai.meta.com/blog/</a> — Llama 4 Scout (109B/17B active) and Maverick (400B/17B active), both MoE; the vision-capable picks used via Groq in this PoC.</li>
<li>Mistral AI (2024) 'Pixtral 12B'. Available at: <a href="https://mistral.ai/news/" style="color:#4FC3F7;">https://mistral.ai/news/</a> — first multimodal model from Mistral; <em>Pixtral Large</em> followed with stronger vision capability.</li>
<li>Google (2025) 'Gemini 2.5 Pro and 2.5 Flash'. Available at: <a href="https://blog.google/technology/google-deepmind/" style="color:#4FC3F7;">https://blog.google/technology/google-deepmind/</a> — current free-tier vision models on Google AI Studio.</li>
<li>OpenAI (n.d.) 'API platform — models'. Available at: <a href="https://platform.openai.com/docs/models" style="color:#4FC3F7;">https://platform.openai.com/docs/models</a> — current GPT-4o / GPT-5 model cards; OpenAI does not officially disclose MoE details.</li>
<li>BerriAI (n.d.) 'LiteLLM documentation'. Available at: <a href="https://docs.litellm.ai/" style="color:#4FC3F7;">https://docs.litellm.ai/</a> — unified provider-agnostic LLM client used in <code>parsers/byo_agent.py</code>.</li>
<li>Groq (n.d.) 'Supported models'. Available at: <a href="https://console.groq.com/docs/models" style="color:#4FC3F7;">https://console.groq.com/docs/models</a> — Llama 4 + vision models served on Groq's free-tier API.</li>
<li>Google AI Studio (n.d.) 'API keys'. Available at: <a href="https://aistudio.google.com/apikey" style="color:#4FC3F7;">https://aistudio.google.com/apikey</a> — free Gemini API keys for the BYOK flow.</li>
</ul>
</div>
    """, unsafe_allow_html=True)

# Run the app if the script is executed directly
if __name__ == "__main__":
    # Use st.set_page_config to ensure page is properly configured
    st.set_page_config(page_title="AI Models Comparisons", page_icon="📋", layout="wide")
    app()
