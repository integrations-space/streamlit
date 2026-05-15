# Agent 5: Compliance Checker — BYOK version
#
# Mirrors the original Vertex AI / GCS implementation (archived in parsers/archived/),
# but reads design-intent + requirements from local files and writes the Excel report
# locally, using a Bring Your Own Key (BYOK) approach via LiteLLM.
#
# Agent 5 (agent_1_compliance_checker): compares the design intent against the
# extracted regulatory requirements and produces a structured non-compliance table.

import json
import logging
import os
import re
import sys

import pandas as pd
import PyPDF2

# Make `byo_agent` importable whether this file is run as a script or imported as a module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from byo_agent import run_text_prompt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("compliance_analysis.log", encoding='utf-8'),
        logging.StreamHandler(stream=sys.stdout),
    ],
)

# === BYOK configuration ===
PROVIDER_ENV = "GEMINI_API_KEY"
MODEL = "gemini/gemini-2.5-flash"  # or openai/gpt-4o-mini, groq/meta-llama/llama-4-scout-17b-16e-instruct, mistral/mistral-large-latest


def read_text_file(file_path: str) -> str:
    """Read a text file and return its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    logging.info("Read text file %s", file_path)
    return content


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    logging.info("Extracted text from PDF %s", file_path)
    return text


def agent_1_compliance_checker(
    design_intent_path: str,
    requirements_path: str,
    output_xlsx_path: str,
    api_key: str,
    model: str = MODEL,
) -> pd.DataFrame:
    """Agent 5: compare design intent (PDF) against extracted requirements (text)."""
    design_intent = extract_text_from_pdf(design_intent_path)
    requirements = read_text_file(requirements_path)

    prompt = f"""
    Analyze the following design intent data against the provided requirements.
    Identify non-compliances or potential issues related to BCA and SCDF regulations.

    Design Intent: {design_intent}

    Requirements: {requirements}

    Provide a structured analysis in JSON format (and JSON only, no commentary) as an
    array of objects with the following fields:
    - Item
    - Design Intent Details
    - BCA Non-compliances
    - SCDF Non-compliances
    """

    response = run_text_prompt(prompt, api_key, model).strip()
    logging.info("Received response of %d chars.", len(response))

    cleaned_response = re.sub(r'```[a-zA-Z]*\n|```', '', response)
    analysis = parse_response(cleaned_response)
    analysis = split_multiline_entries(analysis)

    os.makedirs(os.path.dirname(output_xlsx_path) or ".", exist_ok=True)
    analysis.to_excel(output_xlsx_path, index=False)
    logging.info("Agent 5 analysis saved to %s", output_xlsx_path)
    return analysis


def split_multiline_entries(df: pd.DataFrame) -> pd.DataFrame:
    """Split multi-line strings in DataFrame cells into separate rows for readability."""
    rows = []
    for _, row in df.iterrows():
        bca_lines = str(row.get('BCA Non-compliances', '')).split('\n')
        scdf_lines = str(row.get('SCDF Non-compliances', '')).split('\n')
        max_len = max(len(bca_lines), len(scdf_lines))
        for i in range(max_len):
            new_row = row.copy()
            new_row['BCA Non-compliances'] = bca_lines[i] if i < len(bca_lines) else ""
            new_row['SCDF Non-compliances'] = scdf_lines[i] if i < len(scdf_lines) else ""
            rows.append(new_row)
    return pd.DataFrame(rows)


def parse_response(response: str) -> pd.DataFrame:
    """Parse the LLM's JSON response into a DataFrame."""
    if not response:
        raise ValueError("Empty response received from LLM.")
    data = json.loads(response)
    df = pd.DataFrame(data)
    logging.info("Parsed Agent 5 response successfully.")
    return df


def main():
    api_key = os.environ.get(PROVIDER_ENV)
    if not api_key:
        raise SystemExit(f"Set {PROVIDER_ENV} (or change PROVIDER_ENV/MODEL above for another provider).")

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)

    design_intent_pdf = os.path.join(repo, "design_intent", "Window Schedule.pdf")
    requirements_txt = os.path.join(repo, "parsed_output", "Requirements.txt")
    output_xlsx = os.path.join(repo, "parsed_output", "check_1.xlsx")

    if not os.path.exists(requirements_txt):
        raise SystemExit(
            f"{requirements_txt} not found. Run Dual_Agents_for_Requirements.py first to generate it."
        )

    try:
        agent_1_compliance_checker(design_intent_pdf, requirements_txt, output_xlsx, api_key)
        logging.info("Compliance analysis workflow completed successfully.")
    except Exception as e:
        logging.error("Workflow failed: %s", e)


if __name__ == "__main__":
    main()
