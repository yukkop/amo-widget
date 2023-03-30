# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install the required packages
RUN pip install --no-cache-dir google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Copy the script into the container
COPY document_share.py /app/document_share.py

# Set the entrypoint to run the script
ENTRYPOINT ["python", "document_share.py"]
