# Append Process Demo Script

Append Process Demo

# Description:

This repository contains a Python script (append_process_demo.py) that demonstrates an automated append process for GeoJSON files using AWS S3 and an authentication server. The script handles uploading a GeoJSON file to S3, obtaining an access token from the authentication server, initiating an append process, and monitoring the job status until completion.

# Key Features:

    Uploads GeoJSON files to AWS S3.
    Retrieves access tokens from an authentication server.
    Initiates and monitors append processes via specified endpoints.
    Provides optional functionality to delete uploaded files after successful processing.

# Usage:

Users can clone the repository, configure the script with their AWS credentials and authentication server details, and follow the instructions in the README to execute the append process demo.

## Setup

### Prerequisites

- Python 3.x
- Install required packages:
  ```bash
  pip install boto3 requests
