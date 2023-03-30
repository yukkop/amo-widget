#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PYTHON_DIR="${SCRIPT_DIR}/document-share"

# Initialize variables
email_addresses=()

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -D|--document-id) document_id="$2"; shift ;;
        -e|--email) email_addresses+=("$2"); shift ;;
        -r|--role) role="$2"; shift ;;
        -C|--creditation-file) cred_file="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check if required parameters are set
if [[ -z "${document_id}" ]]; then
    echo "Error: Document ID must be provided."
    exit 1
fi

if [[ ${#email_addresses[@]} -eq 0 ]]; then
    echo "Error: At least one email address must be provided."
    exit 1
fi

if [[ -z "${cred_file}" ]]; then
    echo "Error: Creditation file must be provided."
    exit 1
fi

# Set default role if not provided
role="${role:-reader}"

# Prepare email arguments
email_args=""
for email in "${email_addresses[@]}"; do
    email_args="${email_args} -e ${email}"
done
email_args=$(echo "$email_args" | sed 's/^[[:space:]]*//')

echo "$email_args"

# Run the Docker container with the provided parameters
docker run --rm \
    -v "$(realpath "${cred_file}"):/app/credentials.json" \
    document-share:latest \
    python document_share.py \
    -D "${document_id}" \
    ${email_args} \
    -r "${role}" \
    -C "/app/credentials.json"
