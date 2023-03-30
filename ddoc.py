import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import sys

def duplicate_document(source_document_id, new_title):
    try:
        creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
        drive_service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': new_title,
            'mimeType': 'application/vnd.google-apps.document'
        }

        result = drive_service.files().copy(
            fileId=source_document_id,
            body=file_metadata
        ).execute()

        return result['id']

    except HttpError as error:
        sys.stderr.write(f'An error occurred: {error}\n')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Duplicate a Google Document.')
    parser.add_argument('-D', '--document-id', required=True, help='The ID of the source document to be duplicated.')
    parser.add_argument('-t', '--title', required=True, help='The title of the new duplicated document.')

    args = parser.parse_args()

    new_document_id = duplicate_document(args.document_id, args.title)
    print(new_document_id)
