#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Build the Docker image
docker build -t document-create:latest "${SCRIPT_DIR}"

# Parse command line arguments
clear_image=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--title) title="$2"; shift ;;
        -C|--creditation-file) cred_file="$2"; shift ;;
        -r|--clear-image) clear_image=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if required parameters are set
if [[ -z "${title}" ]]; then
    echo "Error: Title must be provided."
    exit 1
fi

if [[ -z "${cred_file}" ]]; then
    echo "Error: Creditation file must be provided."
    exit 1
fi

# Run the Docker container with the provided parameters
docker run --rm \
    -v "$(realpath "${cred_file}"):/app/creditations.json" \
    document-create:latest \
    python document_create.py \
    -t "${title}" \
    -C '/app/creditations.json'

# Remove the Docker image if specified
if $clear_image; then
    docker rmi create-document:latest
fi
