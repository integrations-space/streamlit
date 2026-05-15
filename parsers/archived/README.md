# Archived: Original Vertex AI / GCS Pipeline

The three scripts in this folder are the **original implementation** of the dual-agent
compliance-analysis pipeline. They were written against:

- **Google Vertex AI** (`vertexai.preview.generative_models.GenerativeModel`)
- **Google Cloud Storage** for inputs, intermediate outputs, and the service-account key
- A hard-coded GCP project (`project-ants-440005`) and bucket (`data_parsing`)

They are kept here for **reference and learning continuity** — they correspond to the
architecture diagram in the project presentation. They are no longer loaded by the live
Streamlit app and **will not run** unless you re-provision the GCP project, restore
billing on Vertex AI / GCS, and supply a service-account key.

## What replaced them

The active pipeline now lives in `parsers/` and uses a **Bring Your Own Key (BYOK)**
approach via [LiteLLM](https://docs.litellm.ai/), so users can run the agents with their
own free-tier or paid key from Gemini, OpenAI, Groq, or Mistral. The file structure and
function names mirror these originals so the architecture diagram still maps:

| Archived (Vertex/GCS) | Active (BYOK) | Agents |
|---|---|---|
| `Dual_Agents_for_GCS.py` | `parsers/Dual_Agents_for_GCS.py` | 1 & 2 — Design Intent parse + tabulate |
| `Dual_Agents_for_Requirements.py` | `parsers/Dual_Agents_for_Requirements.py` | 3 & 4 — Requirements extract + summarise |
| `Agent_for_noncompliances_Checks.py` | `parsers/Agent_for_noncompliances_Checks.py` | 5 — Compliance check |

Shared helpers (LiteLLM wrappers, PDF text extraction, prompt templates) live in
`parsers/byo_agent.py`.
