# Append Process Demo Script

## Description:

This repository contains a Python script (`append_process_demo.py`) that demonstrates an automated append process for GeoJSON files using AWS S3 and an authentication server. The script handles uploading a GeoJSON file to S3, obtaining an access token from the authentication server, initiating an append process, and monitoring the job status until completion. Optionally, the script can delete the uploaded file from S3 after successful processing.

## Key Features:

- **Upload:** Uploads GeoJSON files to AWS S3.
- **Authentication:** Retrieves access tokens from an authentication server.
- **Process Initiation:** Initiates append processes via specified endpoints.
- **Monitoring:** Monitors job status until completion.
- **Cleanup:** Provides optional functionality to delete uploaded files after successful processing.
  
## Usage:

Users can clone the repository, configure the script with their AWS credentials and authentication server details, and follow the instructions in the README to execute the append process demo.

## Setup

### Prerequisites

- Python 3.x
- Install required packages:
  ```bash
  pip install boto3 requests

### Configuration
- Clone the repository
  ```bash
  git clone https://github.com/your-repo/append-process-demo.git
  
- Update ini.py:
  Configure the script with your AWS credentials, S3 bucket details, and authentication server details by updating the ini.py file:
  ```bash
  S3_BUCKET_URL = "your-aws-s3-bucket-url"
  AWS_REGION = "your-aws-region"
  AWS_ACCESS_KEY = "your-aws-access-key"
  AWS_SECRET_KEY = "your-aws-secret-key"
  AWS_ENDPOINT = "your-aws-endpoint"

  AUTH_SERVER_URL = "https://authvertx.iudx.io/auth/v1/token"
  CLIENT_ID = "your-client-id"
  CLIENT_SECRET = "your-client-secret"

  PROCESS_ENDPOINT = "https://ogc.iudx.io/processes/b118b4d4-0bc1-4d0b-b137-fdf5b0558c1d/execution"
  RESOURCE_ID = "your-resource-id"


  
