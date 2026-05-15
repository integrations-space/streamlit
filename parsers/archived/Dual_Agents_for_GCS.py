# Dual Vertex Agents Python Script for Data Parsing, Extraction, Cleaning and Export to GCS
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image
from google.cloud import storage
import pandas as pd
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Vertex AI
PROJECT_ID = 'project-ants-440005'
REGION = 'asia-southeast1'
vertexai.init(project=PROJECT_ID, location=REGION)

# Define agent_parsing for image processing and content extraction
def agent_parsing(bucket_name, blob_name):
    """Downloads an image from GCS and extracts structured schedule data using Vertex AI."""
    # Download image from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    image_bytes = blob.download_as_bytes()
    image = Image.from_bytes(image_bytes)

    # Initialize the generative model
    generative_multimodal_model = GenerativeModel("gemini-1.5-pro-002")

    # Extract table data based on image content (window or door schedule)
    logging.info("Extracting content with multimodal model.")
    response = generative_multimodal_model.generate_content([
    """
    Extract and tabulate the details of building components shown in the image. Identify if the schedule is for windows or doors.

    For a window schedule, include columns:
    | Component Name | Width (mm) | Height (mm) | Panel Width (mm) | Mullion Size (mm) | Panel Number | Sill Distance (mm) | Area (mÂ²) | Max. Room Area (10% Ventilation) (mÂ²) |

    For a door schedule, include columns:
    | Door Type | Width (mm) | Height (mm) | Material | Thickness (mm) | Frame Type |

    Provide only visible data from the image, formatted accordingly.
    """,
    image
    ])

    # Return the table text from the response
    table_text = response.text
    logging.info(f"Extracted table text:\n{table_text}")
    return table_text

# Define agent_export for exporting parsed data to Excel in GCS
def agent_export(table_text, output_gcs_path):
    """Uses GenerativeModel to standardize the extracted table text, format it, and export it to an Excel file in GCS."""
    # Initialize the generative model
    generative_multimodal_model = GenerativeModel("gemini-1.5-pro-002")

    # Use the model to reformat and validate the table data
    response = generative_multimodal_model.generate_content(f"""
    Take the following extracted table data and format it for export.
    Generally, the content to include
        - Component Name (e.g., W1, W2, etc.)
        - Width (in mm)
        - Height (in mm)
        - Window/Door Panel Width (in mm) (clear width for window/door opening)
        - Mullion Size / Door Jam (in mm)
        - Window/Door Panel Number [(Width - all window mullion or door jam widths shown in elevation) / Panel Width]
        - Sill Distance (in mm) (applicable to window)
        - Window/Door area (in mÂ²) Width x Height
        - Max. Room Area (in mÂ²) assuming 10% ventilation requirement (application for window)

    Extracted Data:
    {table_text}

    If the data represents a window schedule, ensure the columns are:
    | Component Name | Width (mm) | Height (mm) | Panel Width (mm) | Mullion Size (mm) | Panel Number | Sill Distance (mm) | Area (mÂ²) | Max. Room Area (10% Ventilation) (mÂ²) |

    If the data represents a door schedule, ensure the columns are:
    | Door Name | Width (mm) | Height (mm) | Door Panel Width (mm) | Door Jam Size (mm) | Door Panel Number | Area (mÂ²) |

    Return the formatted table with consistent units, and validate each column so there are no missing or invalid entries.
    """)

    # Extract the formatted table text from the model response
    formatted_table_text = response.text

    # Determine the schedule type based on keywords in the formatted text
    if "Component Name" in formatted_table_text:
        output_filename = "data_parsing/parsed_output/window_schedule.xls"
        columns = ["Component Name", "Width (mm)", "Height (mm)", "Panel Width (mm)", 
                   "Mullion Size (mm)", "Panel Number", "Sill Distance (mm)", "Area (m2)", 
                   "Max. Room Area (10% Ventilation)(m2)"]
    elif "Door Type" in formatted_table_text:
        output_filename = "data_parsing/parsed_output/Door Schedule.xls"
        columns = ["Door Type", "Width (mm)", "Height (mm)", "Material", "Thickness (mm)", "Frame Type"]
    else:
        logging.error("Unknown schedule type. Cannot parse table.")
        return

    # Parse the formatted text into rows and filter out any malformed or unnecessary rows
    data_lines = formatted_table_text.splitlines()

    # Initialize a flag to track whether we have passed the header section
    passed_header = False
    data = []

    for line in data_lines:
        # Skip lines that contain '---' or are empty
        if '---' in line or not line.strip():
            continue

        # If we encounter the header again, skip it
        if "Component Name" in line and passed_header:
            continue

        # Mark that we've passed the header section
        if "Component Name" in line:
            passed_header = True
            continue

        # Split each line into columns and clean up whitespace
        row = [item.strip() for item in line.split('|') if item.strip()]

        # Ensure row has the correct number of columns before adding it to data
        if len(row) == len(columns):
            data.append(row)
        else:
            logging.warning(f"Skipping malformed row: {row}")

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(data, columns=columns)

    # Save the DataFrame to an Excel file in memory
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    # Upload the Excel file to GCS
    storage_client = storage.Client()
    bucket_name, blob_name = output_filename.split('/', 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(excel_buffer, content_type='application/vnd.ms-excel')
    logging.info(f"Excel file uploaded to gs://{output_filename}")

# Using the agents
if __name__ == "__main__":
    # Set GCS paths
    input_gcs_uri = 'gs://data_parsing/design_intent/Window Schedule.jpg'

    # Parse the GCS URI for the input file
    bucket_name = input_gcs_uri.split('//')[1].split('/')[0]
    blob_name = '/'.join(input_gcs_uri.split('//')[1].split('/')[1:])

    # Use agent_parsing to extract the table text from the image
    table_text = agent_parsing(bucket_name, blob_name)

    # Use agent_export to format and save the extracted data to an Excel file in GCS
    agent_export(table_text, 'data_parsing/parsed_output')
    print(f"Excel file successfully saved.")
