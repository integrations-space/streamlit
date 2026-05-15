from google.cloud import aiplatform, storage
import pandas as pd
import logging
import io
import PyPDF2
import os
from google.api_core import exceptions
from vertexai.preview.generative_models import GenerativeModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up authentication using the key stored in GCS
KEY_FILE_PATH = 'key.json'
BUCKET_NAME = 'data_parsing'
GCS_KEY_URI = f'gs://{BUCKET_NAME}/key.json'
OUTPUT_BLOB_NAME = 'parsed_output/Requirements.txt'


def download_key_file():
    """Downloads the service account key from GCS to the local system."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob('key.json')
    blob.download_to_filename(KEY_FILE_PATH)
    logging.info(f"Service account key downloaded to {KEY_FILE_PATH}")

# Initialize Vertex AI
PROJECT_ID = 'project-ants-440005'
REGION = 'asia-southeast1'

def initialize_vertex_ai():
    """Initializes Vertex AI with the downloaded key file."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = KEY_FILE_PATH
    aiplatform.init(project=PROJECT_ID, location=REGION)

def read_agent2_output(bucket_name, blob_name):
    """Reads an Excel output from Agent 2 stored in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    try:
        content = blob.download_as_bytes()
        return pd.read_excel(io.BytesIO(content))
    except exceptions.NotFound:
        logging.error(f"The file {blob_name} was not found in bucket {bucket_name}. Please check the file path.")
        return pd.DataFrame()

def extract_info_with_gemini(prompt, content):
    """Uses Vertex AI's Gemini model to extract key information."""
    try:
        generative_model = GenerativeModel("gemini-1.5-pro-002")
        response = generative_model.generate_content(prompt + content)
        return response.text
    except Exception as e:
        logging.error(f"Error during text generation: {e}")
        return ""

def read_document_content(gcs_uri):
    """Reads and extracts text content from a PDF file stored in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket_name, blob_name = gcs_uri.split('//')[1].split('/', 1)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    try:
        pdf_content = blob.download_as_bytes()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        return text_content
    except exceptions.NotFound:
        logging.error(f"The file {blob_name} was not found in bucket {bucket_name}. Please check the file path.")
        return ""

def save_text_to_gcs(bucket_name, blob_name, text_content):
    """Saves the provided text content to Google Cloud Storage as a text file."""
    try:
        # Initialize Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Upload text content to the specified GCS location
        blob.upload_from_string(text_content, content_type='text/plain')
        logging.info(f"Text successfully saved to gs://{bucket_name}/{blob_name}")
    except Exception as e:
        logging.error(f"Error saving text to GCS: {e}")

def main():
    # Download the key file and initialize Vertex AI
    download_key_file()
    initialize_vertex_ai()
    
    # Read Agent 2 output based on schedule type
    schedule_type = 'Window'  # Set the type manually as Window or Door
    if schedule_type == 'Window':
        output_file_path = 'parsed_output/window_schedule.xls'
    else:
        output_file_path = 'parsed_output/door_schedule.xls'
    
    schedule_data = read_agent2_output('data_parsing', output_file_path)
    if schedule_data.empty:
        logging.error("No schedule data available. Exiting the workflow.")
        return
    
    # Prepare content for analysis
    if schedule_type == 'Window':
        docs_to_analyze = [
            'gs://data_parsing/regulatory_requirements/approveddoc.pdf',
            'gs://data_parsing/regulatory_requirements/scdf chapter 4.pdf'
        ]
    else:
        docs_to_analyze = [
            'gs://data_parsing/regulatory_requirements/approveddoc.pdf',
            'gs://data_parsing/regulatory_requirements/scdf chapter 4.pdf'
        ]
    
    # Extract and analyze information from relevant documents
    all_extracted_info = ""
    for doc in docs_to_analyze:
        content = read_document_content(doc)
        if not content:
            logging.error(f"No content extracted from {doc}. Skipping this document.")
            continue
        
        prompt = f"""
        Extract and summarize the key requirements for {schedule_type} from the following document:
        {doc}

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
        """
        
        extracted_info = extract_info_with_gemini(prompt, content)
        logging.info(f"Extracted information from {doc}:")
        logging.info(extracted_info)
        all_extracted_info += extracted_info + "\n\n"

    # Summarize the most stringent requirements
    if all_extracted_info:
        summary_prompt = f"""
        Summarize the most stringent {schedule_type} requirements based on the extracted information. 
        Compare these requirements with the data from {output_file_path}.
        Highlight any non-compliances or regulatory concerns.
        Provide the summary in a structured format using markdown, with clear headings and bullet points for quick understanding.
        Include sections on:
        1. Most Stringent Requirements
        2. Potential Non-Compliances
        3. Areas Requiring Further Investigation
        4. Recommendations for Compliance
        """
        final_summary = extract_info_with_gemini(summary_prompt, all_extracted_info)
        logging.info("Final summary of most stringent requirements:")
        logging.info(final_summary)
        
        # Save the final summary to GCS
        save_text_to_gcs(BUCKET_NAME, OUTPUT_BLOB_NAME, final_summary)
    else:
        logging.error("No information extracted from the documents. Unable to provide a summary.")

if __name__ == "__main__":
    main()
