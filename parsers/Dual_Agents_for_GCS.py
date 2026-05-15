# Dual-Agent Pipeline for Design Intent Parsing — BYOK version
#
# Mirrors the original Vertex AI / GCS implementation (archived in parsers/archived/),
# but reads input images from the local repo and writes Excel output locally, using a
# Bring Your Own Key (BYOK) approach via LiteLLM. Pick any LiteLLM-supported vision
# model from Gemini, OpenAI, Groq, or Mistral.
#
# Agent 1 (agent_parsing): vision model extracts a markdown table from the schedule image.
# Agent 2 (agent_export):  text model standardises the table and exports to Excel.

import logging
import os
import sys

# Make `byo_agent` importable whether this file is run as a script or imported as a module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from byo_agent import (
    parse_schedule_image,
    format_table,
    table_text_to_dataframe,
    dataframe_to_excel_bytes,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === BYOK configuration ===
# Set the matching environment variable before running, e.g. GEMINI_API_KEY=...
# (Provider prefix is part of the MODEL string — LiteLLM routes accordingly.)
PROVIDER_ENV = "GEMINI_API_KEY"
MODEL = "gemini/gemini-2.5-flash"  # also try: openai/gpt-4o-mini, groq/meta-llama/llama-4-scout-17b-16e-instruct, mistral/pixtral-large-latest


def agent_parsing(image_path: str, api_key: str, model: str = MODEL) -> str:
    """Agent 1: extract a markdown table of building components from the schedule image."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    logging.info("Extracting content with multimodal model %s.", model)
    table_text = parse_schedule_image(image_bytes, api_key, model)
    logging.info("Extracted table text:\n%s", table_text)
    return table_text


def agent_export(table_text: str, output_xls_path: str, api_key: str, model: str = MODEL):
    """Agent 2: standardise the extracted table, validate columns, and export to Excel locally."""
    formatted_table_text = format_table(table_text, api_key, model)
    df, schedule_type = table_text_to_dataframe(formatted_table_text)
    os.makedirs(os.path.dirname(output_xls_path) or ".", exist_ok=True)
    with open(output_xls_path, "wb") as f:
        f.write(dataframe_to_excel_bytes(df))
    logging.info("Excel file (%s schedule) saved to %s", schedule_type, output_xls_path)


# Using the agents
if __name__ == "__main__":
    api_key = os.environ.get(PROVIDER_ENV)
    if not api_key:
        raise SystemExit(f"Set {PROVIDER_ENV} (or change PROVIDER_ENV/MODEL above for another provider).")

    # Local input/output paths (mirroring the original GCS-based flow)
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    input_image = os.path.join(repo, "design_intent", "Window Schedule.jpg")
    output_xls = os.path.join(repo, "parsed_output", "window_schedule.xls")

    table_text = agent_parsing(input_image, api_key)
    agent_export(table_text, output_xls, api_key)
    print(f"Excel file successfully saved to {output_xls}.")
