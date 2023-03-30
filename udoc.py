import argparse
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import sys

def update_document(document_id, requests):
    try:
        creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
        docs_service = build('docs', 'v1', credentials=creds)

        result = docs_service.documents().batchUpdate(
            documentId=document_id,
            body={
                'requests': requests
            }
        ).execute()

        return result

    except HttpError as error:
        sys.stderr.write(f'An error occurred: {error}\n')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update a Google Document.')
    parser.add_argument('-D', '--document-id', required=True, help='The ID of the document to be updated.')
    parser.add_argument('-r', '--requests', required=True, help='JSON string containing the update requests.')

    args = parser.parse_args()

    try:
        requests = json.loads(args.requests)
    except json.JSONDecodeError as error:
        sys.stderr.write(f'Error decoding JSON: {error}\n')
        sys.exit(1)

    result = update_document(args.document_id, requests)
    print(result)
