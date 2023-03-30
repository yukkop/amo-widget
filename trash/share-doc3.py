import sys
import argparse
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def share_document(document_id, email):
    # Set up credentials and API client
    creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
    drive_service = build('drive', 'v3', credentials=creds)

    # Define the permission to be granted (in this case, view permission)
    permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email
    }

    # Add the permission to the document
    try:
        permission = drive_service.permissions().create(
            fileId=document_id,
            body=permission,
            sendNotificationEmail=False
        ).execute()
        print(permission.get('id'))

    except HttpError as error:
        sys.stderr.write(f'An error occurred: {error}\n')

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Share a Google document with an email address.')
    parser.add_argument('-D', '--document-id', required=True, help='The ID of the document to be shared.')
    parser.add_argument('-e', '--email-address', required=True, help='The email address to share the document with.')

    args = parser.parse_args()

    if not args.document_id:
        sys.stderr.write('Error: Document ID must be provided.\n')
        sys.exit(1)

    if not args.email_address or not is_valid_email(args.email_address):
        sys.stderr.write('Error: A valid email address must be provided.\n')
        sys.exit(1)

    share_document(args.document_id, args.email_address)
