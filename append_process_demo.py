import requests
import boto3
import time
import os
from ini import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    s3_client = boto3.client('s3', region_name=AWS_REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             endpoint_url=f'https://{AWS_ENDPOINT}')
    try:
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        logging.info(f"Uploading file {file_path} to S3 bucket {bucket_name} as {object_name}...")
        s3_client.upload_file(file_path, bucket_name, object_name)
        logging.info(f"File {file_path} uploaded to S3 as {object_name}.")
        return True
    except Exception as e:
        logging.info(f"Upload to S3 failed: {e}")
        return False

def get_access_token():
    headers = {
        'clientId': CLIENT_ID,
        'clientSecret': CLIENT_SECRET,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Content-Type': 'application/json'
    }
    payload = {
        "itemId": "ogc.iudx.io",
        "itemType": "resource_server",
        "role": "provider"
    }
    logging.info("Requesting access token from authentication server...")
    response = requests.post(AUTH_SERVER_URL, headers=headers, json=payload)
    if response.status_code == 200:
        logging.info("Access token obtained successfully.")
        logging.info(response.json())
        token = response.json()['results']['accessToken']
        # logging.info(f"Token: {token}")
        return token
    else:
        logging.info(f"Failed to get access token: {response.text}")
        return None

def start_append_process(token, file_name):
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {
            "fileName": file_name,
            "title": "append_process_adapter_test",
            "description": "Testing collection appending process demo adapter",
            "resourceId": RESOURCE_ID,
            "version": "1.0.0"
        },
        "response": "raw"
    }
    logging.info(f"Starting append process for file {file_name}...")
    response = requests.post(PROCESS_ENDPOINT, headers=headers, json=payload)
    if response.status_code == 201:
        job_api_url = response.headers.get('Location')
        logging.info(f"Append process started successfully. Job URL: {job_api_url}")
        return job_api_url
    else:
        logging.info(f"Failed to start append process: {response.text}")
        return None

def poll_job_status(job_api_url, token):
    headers = {'Authorization': f'Bearer {token}'}
    while True:
        logging.info("Polling job status...")
        response = requests.get(job_api_url, headers=headers)
        if response.status_code == 200:
            job_status = response.json()
            status = job_status.get('status')
            if status == 'SUCCESSFUL':
                logging.info("Append process completed successfully.")
                return True
            elif status == 'FAILED':
                logging.info("Append process failed.")
                return False
            else:
                logging.info("Append process running... Checking again in 5 seconds.")
                time.sleep(5)
        else:
            logging.info(f"Failed to get job status: {response.text}")
            return False

def delete_file_from_s3(bucket_name, object_name):
    s3_client = boto3.client('s3', region_name=AWS_REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY,
                             endpoint_url=f'https://{AWS_ENDPOINT}')
    try:
        logging.info(f"Deleting file {object_name} from S3 bucket {bucket_name}...")
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        logging.info(f"File {object_name} deleted from S3.")
    except Exception as e:
        logging.info(f"Failed to delete file from S3: {e}")

def main(iudx_date_format):
    file_path = "data_niruthi_latest.json"  # Local path to your JSON file
    file_name = f"niruthi_live_weather_data/niruthi_data_{iudx_date_format}.json"  # Desired S3 object name

    # Step 1: Upload the file to S3
    if upload_file_to_s3(file_path, S3_BUCKET_URL, file_name):
        logging.info("File uploaded to S3 successfully.")
        
        # Step 2: Get the access token
        token = get_access_token()
        if token:
            # Step 3: Start the append process
            job_api_url = start_append_process(token, file_name)
            if job_api_url:
                # Step 4: Poll the job status until it completes
                if poll_job_status(job_api_url, token):
                    # Step 5: Delete the file from S3 after successful process completion
                    delete_file_from_s3(S3_BUCKET_URL, file_name)
                else:
                    logging.info("Append process did not complete successfully.")
            else:
                logging.info("Failed to start append process.")
        else:
            logging.info("Failed to obtain access token.")
    else:
        logging.info("Failed to upload file to S3.")
