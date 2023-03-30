#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PYTHON_DIR="${SCRIPT_DIR}/document-duplicate"

# Parse command line arguments
clear_image=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -D|--document-id) document_id="$2"; shift ;;
        -t|--title) title="$2"; shift ;;
        -C|--creditation-file) cred_file="$2"; shift ;;
        -r|--clear-image) clear_image=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if required parameters are set
if [[ -z "${document_id}" ]]; then
    echo "Error: Document ID must be provided."
    exit 1
fi

if [[ -z "${title}" ]]; then
    echo "Error: Title must be provided."
    exit 1
fi

if [[ -z "${cred_file}" ]]; then
    echo "Error: Creditation file must be provided."
    exit 1
fi

# Build the Docker image
docker build -t document-duplicate:latest "${PYTHON_DIR}" >> "${PYTHON_DIR}/tmp"  

# Run the Docker container with the provided parameters
docker run --rm \
    -v "$(realpath "${cred_file}"):/app/credentials.json" \
    document-duplicate:latest \
    python duplicate_document.py \
    -D "${document_id}" \
    -t "${title}" \
    -C "/app/credentials.json"

# Remove the Docker image if specified
if $clear_image; then
    docker rmi duplicate-document:latest
fi
