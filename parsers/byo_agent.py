# BYO (Bring Your Own) API key agent for Design Intent parsing.
# Uses LiteLLM under the hood so the same code path can later be pointed at
# Groq / OpenAI / Mistral by changing the model string and provider env var.
import base64
import io
import logging

import pandas as pd
import PyPDF2
from litellm import completion

logger = logging.getLogger(__name__)

PARSE_PROMPT = """
Extract and tabulate the details of building components shown in the image. Identify if the schedule is for windows or doors.

For a window schedule, include columns:
| Component Name | Width (mm) | Height (mm) | Panel Width (mm) | Mullion Size (mm) | Panel Number | Sill Distance (mm) | Area (m2) | Max. Room Area (10% Ventilation) (m2) |

For a door schedule, include columns:
| Door Type | Width (mm) | Height (mm) | Material | Thickness (mm) | Frame Type |

Provide only visible data from the image, formatted accordingly. Return only the markdown table, no commentary.
""".strip()

FORMAT_PROMPT_TEMPLATE = """
Take the following extracted table data and format it for export.
Generally, the content to include:
    - Component Name (e.g., W1, W2, etc.)
    - Width (in mm)
    - Height (in mm)
    - Window/Door Panel Width (in mm)
    - Mullion Size / Door Jam (in mm)
    - Window/Door Panel Number
    - Sill Distance (in mm) (applicable to window)
    - Window/Door area (in m2) = Width x Height
    - Max. Room Area (in m2) assuming 10% ventilation requirement (window only)

Extracted Data:
{table_text}

If window schedule, use columns:
| Component Name | Width (mm) | Height (mm) | Panel Width (mm) | Mullion Size (mm) | Panel Number | Sill Distance (mm) | Area (m2) | Max. Room Area (10% Ventilation) (m2) |

If door schedule, use columns:
| Door Name | Width (mm) | Height (mm) | Door Panel Width (mm) | Door Jam Size (mm) | Door Panel Number | Area (m2) |

Return only the markdown table. No commentary, no preamble.
""".strip()


def _image_to_data_url(image_bytes: bytes, mime: str = "image/jpeg") -> str:
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime};base64,{b64}"


def parse_schedule_image(image_bytes: bytes, api_key: str, model: str = "gemini/gemini-2.5-flash") -> str:
    """Agent 1: vision model extracts a markdown table from the schedule image."""
    response = completion(
        model=model,
        api_key=api_key,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PARSE_PROMPT},
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image_bytes)}},
                ],
            }
        ],
    )
    return response.choices[0].message.content


def format_table(table_text: str, api_key: str, model: str = "gemini/gemini-2.5-flash") -> str:
    """Agent 2: text model cleans/standardises the table."""
    response = completion(
        model=model,
        api_key=api_key,
        messages=[{"role": "user", "content": FORMAT_PROMPT_TEMPLATE.format(table_text=table_text)}],
    )
    return response.choices[0].message.content


def table_text_to_dataframe(table_text: str) -> tuple[pd.DataFrame, str]:
    """Parse a markdown-table string into a DataFrame. Returns (df, schedule_type)."""
    if "Component Name" in table_text:
        columns = [
            "Component Name", "Width (mm)", "Height (mm)", "Panel Width (mm)",
            "Mullion Size (mm)", "Panel Number", "Sill Distance (mm)",
            "Area (m2)", "Max. Room Area (10% Ventilation) (m2)",
        ]
        schedule_type = "window"
    elif "Door" in table_text:
        columns = ["Door Name", "Width (mm)", "Height (mm)", "Door Panel Width (mm)",
                   "Door Jam Size (mm)", "Door Panel Number", "Area (m2)"]
        schedule_type = "door"
    else:
        raise ValueError("Could not determine schedule type from output.")

    rows = []
    passed_header = False
    for line in table_text.splitlines():
        if "---" in line or not line.strip():
            continue
        if columns[0] in line and not passed_header:
            passed_header = True
            continue
        if columns[0] in line and passed_header:
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) == len(columns):
            rows.append(cells)
        else:
            logger.warning("Skipping malformed row: %s", cells)

    return pd.DataFrame(rows, columns=columns), schedule_type


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf.read()


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract all text content from a PDF file (bytes)."""
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def run_text_prompt(prompt: str, api_key: str, model: str) -> str:
    """Generic single-turn text completion — no image input."""
    response = completion(
        model=model,
        api_key=api_key,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


REQUIREMENTS_EXTRACT_PROMPT_TEMPLATE = """
Extract and summarize the key requirements for {schedule_type} from the following regulatory document ({doc_name}).

For each requirement, provide:
1. Requirement description
2. Source document and specific clause/section
3. Applicable measurements or specifications
4. Any exceptions or special conditions

Organize the information under the following categories:
a) Ventilation requirements
b) Opening sizes and dimensions
c) Positioning and placement
d) Area calculations and requirements
e) Safety and security features
f) Accessibility considerations
g) Energy efficiency standards
h) Other relevant specifications

Present the information in a structured format using markdown, with clear headings and bullet points for easy readability. Highlight any stringent requirements or potential non-compliances.

Document content:
{content}
""".strip()


REQUIREMENTS_SUMMARY_PROMPT_TEMPLATE = """
Summarize the most stringent {schedule_type} requirements based on the extracted information below.
Highlight any non-compliances or regulatory concerns.
Provide the summary in a structured format using markdown, with clear headings and bullet points for quick understanding.

Include sections on:
1. Most Stringent Requirements
2. Potential Non-Compliances
3. Areas Requiring Further Investigation
4. Recommendations for Compliance

Extracted information from regulatory documents:
{combined_extracted}
""".strip()


MAX_PDF_CHARS = 200_000  # ~50k tokens — safe for modern 128k-context models
