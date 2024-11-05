import os
import json
import logging
import pandas as pd
import PyPDF2
from google.cloud import storage
from google.cloud import vision
from vertexai.preview.generative_models import GenerativeModel
from google.oauth2 import service_account
import sys
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("compliance_analysis.log", encoding='utf-8'),
        logging.StreamHandler(stream=sys.stdout)
    ]
)

# Configuration parameters
BUCKET_NAME = 'data_parsing'
DESIGN_INTENT_BLOB = 'design_intent/Window Schedule.pdf'
REQUIREMENTS_BLOB = 'parsed_output/Requirements.txt'
CREDENTIALS_BLOB = 'key.json' 

# Local path where the credentials file will be saved
CREDENTIALS_LOCAL_PATH = 'key.json'

# Initialize Google Cloud Storage Client to Download the Credentials
storage_client = storage.Client()

def download_credentials(bucket_name, blob_name, destination):
    """Download a credentials file from Google Cloud Storage to a local path."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(destination)
        logging.info(f"Downloaded credentials file {blob_name} to {destination}")
    except Exception as e:
        logging.error(f"Failed to download credentials file {blob_name}: {e}")
        raise

# Download the credentials file locally
download_credentials(BUCKET_NAME, CREDENTIALS_BLOB, CREDENTIALS_LOCAL_PATH)

# Initialize Google Cloud clients with credentials
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_LOCAL_PATH)
storage_client = storage.Client(credentials=credentials)
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

# Initialize Vertex AI Gemini model
gemini_model = GenerativeModel("gemini-1.5-pro-002")

def download_file(bucket_name, blob_name, destination):
    """Download a file from Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(destination)
        logging.info(f"Downloaded {blob_name} to {destination}")
    except Exception as e:
        logging.error(f"Failed to download {blob_name}: {e}")
        raise

def upload_file_to_gcs(local_path, bucket_name, blob_name):
    """Upload a file to Google Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_path)
        logging.info(f"Uploaded {local_path} to {bucket_name}/{blob_name}")
    except Exception as e:
        logging.error(f"Failed to upload {local_path}: {e}")
        raise

def read_text_file(file_path):
    """Read a text file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logging.info(f"Read text file {file_path}")
            return content
    except Exception as e:
        logging.error(f"Failed to read text file {file_path}: {e}")
        raise

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyPDF2."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        logging.info(f"Extracted text from PDF {file_path}")
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from PDF {file_path}: {e}")
        raise

def agent_1_compliance_checker(design_intent_path, requirements_path):
    """Agent 1: Compliance Checker (Design Intent vs. Requirements)"""
    design_intent = extract_text_from_pdf(design_intent_path)
    requirements = read_text_file(requirements_path)

    prompt = f"""
    Analyze the following design intent data against the provided requirements.
    Identify non-compliances or potential issues related to BCA and SCDF regulations.
    
    Design Intent: {design_intent}
    
    Requirements: {requirements}
    
    Provide a structured analysis in JSON format with the following fields:
    - Item
    - Design Intent Details
    - BCA Non-compliances
    - SCDF Non-compliances
    """

    response = gemini_model.generate_content(prompt).text.strip()
    logging.info(f"Received response: {response}")
    
    # Clean response by removing markdown formatting if present
    cleaned_response = re.sub(r'```[a-zA-Z]*\n|```', '', response)
    
    # Parse the response and convert it into a DataFrame
    analysis = parse_response(cleaned_response)
    
    # Split multi-line entries into separate rows for easier readability
    analysis = split_multiline_entries(analysis)
    
    analysis.to_excel('check_1.xlsx', index=False)
    upload_file_to_gcs('check_1.xlsx', BUCKET_NAME, 'parsed_output/check_1.xlsx')
    logging.info("Agent 1 analysis completed and saved to check_1.xlsx and uploaded to Google Cloud Storage")
    
    return analysis

def split_multiline_entries(df):
    """Split multi-line strings in DataFrame cells into separate rows for easier readability."""
    rows = []
    for _, row in df.iterrows():
        max_len = max(len(str(row['BCA Non-compliances']).split('\n')), len(str(row['SCDF Non-compliances']).split('\n')))
        for i in range(max_len):
            new_row = row.copy()
            new_row['BCA Non-compliances'] = str(row['BCA Non-compliances']).split('\n')[i] if i < len(str(row['BCA Non-compliances']).split('\n')) else ""
            new_row['SCDF Non-compliances'] = str(row['SCDF Non-compliances']).split('\n')[i] if i < len(str(row['SCDF Non-compliances']).split('\n')) else ""
            rows.append(new_row)
    return pd.DataFrame(rows)

def parse_response(response):
    """Parse the AI model's response and convert it into a DataFrame."""
    try:
        if response and response != '':
            data = json.loads(response)
            df = pd.DataFrame(data)
            logging.info("Parsed Agent response successfully.")
            return df
        else:
            logging.error("Empty response received from the AI model.")
            raise ValueError("Empty response received from AI model.")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse Agent response: {e}")
        raise

def main():
    try:
       # Download necessary files from Google Cloud Storage 
       download_file(BUCKET_NAME, DESIGN_INTENT_BLOB, 'Window Schedule.pdf')
       download_file(BUCKET_NAME, REQUIREMENTS_BLOB, 'requirements.txt')

       # Execute Agent 1 
       agent1_result = agent_1_compliance_checker('Window Schedule.pdf', 'requirements.txt')

       logging.info("Compliance analysis workflow completed successfully.")

    except Exception as e:
       logging.error(f"Workflow failed: {e}")

if __name__ == "__main__":
   main()