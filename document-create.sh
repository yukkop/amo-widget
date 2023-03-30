#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Parse command line arguments
clear_image=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--title) title="$2"; shift ;;
        -C|--creditation-file) cred_file="$2"; shift ;;
        -r|--clear-image) clear_image=true ;;
        -h|--help) help=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

print_help() {
	echo "Usage: $(basename ${0%%.${0##*.}}) [OPTIONS]"
    echo ""
    echo "Create a new Google Document."
    echo ""
    echo "Options:"
    echo "  -t, --title TITLE             The title of the new document."
    echo "  -C, --creditation-file FILE   Path to the service account credentials file."
    echo "  -r, --clear-image             Remove the Docker image after execution."
    echo "  -h, --help                    Show this help message and exit."
}

# Check if required parameters are set
if [[ "${help}" == "true" ]]; then
    print_help
    exit 0
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
docker build -t document-create:latest "${SCRIPT_DIR}/document-create" > "${SCRIPT_DIR}/tmp"

# Run the Docker container with the provided parameters
docker run --rm \
	-v "$(realpath "${cred_file}"):/app/creditations.json" \
	document-create:latest \
	python document_create.py \
	-t "${title}" \
	-C "/app/creditations.json"

# Remove the Docker image if specified
if $clear_image; then
    docker rmi create-document:latest
fi
