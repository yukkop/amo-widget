#!/bin/bash

# Check if there are enough arguments
if [[ "$#" -lt 1 ]]; then
    echo "Error: At least one argument must be provided."
    exit 1
fi

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Get the action (create or duplicate)
action=$1
shift

case $action in
    create)
        bash "${SCRIPT_DIR}/document-create.sh" "$@"
        ;;
    duplicate)
        bash "${SCRIPT_DIR}/document-duplicate.sh" "$@"
        ;;
    *)
        echo "Error: Invalid action. Available actions: create, duplicate."
        exit 1
        ;;
esac
