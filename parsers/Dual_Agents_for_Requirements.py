# Dual-Agent Pipeline for Regulatory Requirements — BYOK version
#
# Mirrors the original Vertex AI / GCS implementation (archived in parsers/archived/),
# but reads regulatory PDFs from the local repo and writes the summary locally, using a
# Bring Your Own Key (BYOK) approach via LiteLLM. Pick any LiteLLM-supported model from
# Gemini, OpenAI, Groq, or Mistral.
#
# Agent 3 (extract_info_with_llm + read_document_content): extract categorised
#         requirements from each regulatory PDF.
# Agent 4 (main, second call): synthesise the most stringent requirements, potential
#         non-compliances, and recommendations.

import logging
import os
import sys

# Make `byo_agent` importable whether this file is run as a script or imported as a module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from byo_agent import (
    extract_pdf_text,
    run_text_prompt,
    REQUIREMENTS_EXTRACT_PROMPT_TEMPLATE,
    REQUIREMENTS_SUMMARY_PROMPT_TEMPLATE,
    MAX_PDF_CHARS,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === BYOK configuration ===
PROVIDER_ENV = "GEMINI_API_KEY"
MODEL = "gemini/gemini-2.5-flash"  # or openai/gpt-4o-mini, groq/meta-llama/llama-4-scout-17b-16e-instruct, mistral/mistral-large-latest


def read_document_content(pdf_path: str) -> str:
    """Read and extract text content from a local PDF file."""
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    text = extract_pdf_text(pdf_bytes)
    if len(text) > MAX_PDF_CHARS:
        logging.warning("Truncating %s from %d to %d chars.", pdf_path, len(text), MAX_PDF_CHARS)
        text = text[:MAX_PDF_CHARS]
    return text


def extract_info_with_llm(prompt: str, api_key: str, model: str = MODEL) -> str:
    """Call the chosen LLM with a single text prompt. Replaces the original Vertex-Gemini call."""
    try:
        return run_text_prompt(prompt, api_key, model)
    except Exception as e:
        logging.error("Error during text generation: %s", e)
        return ""


def save_text_to_file(file_path: str, text_content: str):
    """Save the provided text content to a local file."""
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    logging.info("Text successfully saved to %s", file_path)


def main():
    api_key = os.environ.get(PROVIDER_ENV)
    if not api_key:
        raise SystemExit(f"Set {PROVIDER_ENV} (or change PROVIDER_ENV/MODEL above for another provider).")

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)

    schedule_type = "Window"  # or "Door"
    docs_to_analyze = [
        ("BCA Approved Doc", os.path.join(repo, "regulatory_requirements", "approveddoc.pdf")),
        ("SCDF Chapter 4",   os.path.join(repo, "regulatory_requirements", "scdf chapter 4.pdf")),
    ]
    output_path = os.path.join(repo, "parsed_output", "Requirements.txt")

    all_extracted_info = ""
    for doc_name, pdf_path in docs_to_analyze:
        content = read_document_content(pdf_path)
        if not content:
            logging.error("No content extracted from %s. Skipping.", doc_name)
            continue
        prompt = REQUIREMENTS_EXTRACT_PROMPT_TEMPLATE.format(
            schedule_type=schedule_type, doc_name=doc_name, content=content,
        )
        extracted = extract_info_with_llm(prompt, api_key)
        logging.info("Extracted information from %s.", doc_name)
        all_extracted_info += f"## From {doc_name}\n\n{extracted}\n\n"

    if not all_extracted_info:
        logging.error("No information extracted from any document. Cannot summarise.")
        return

    summary_prompt = REQUIREMENTS_SUMMARY_PROMPT_TEMPLATE.format(
        schedule_type=schedule_type, combined_extracted=all_extracted_info,
    )
    final_summary = extract_info_with_llm(summary_prompt, api_key)
    logging.info("Final summary of most stringent requirements generated.")
    save_text_to_file(output_path, final_summary)


if __name__ == "__main__":
    main()
