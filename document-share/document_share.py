import sys
import argparse
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def share_document(document_id, email_addresses, role, credentials_file):
    # Set up credentials and API client
    creds = service_account.Credentials.from_service_account_file(credentials_file)
    drive_service = build('drive', 'v3', credentials=creds)

    for email in email_addresses:
        # Define the permission to be granted (in this case, view permission)
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }

        # Add the permission to the document
        try:
            permission = drive_service.permissions().create(
                fileId=document_id,
                body=permission,
                sendNotificationEmail=False
            ).execute()
            print(f'{email} {permission.get("id")}')

        except HttpError as error:
            sys.stderr.write(f'An error occurred for {email}: {error}\n')

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Share a Google document with multiple email addresses.')
    parser.add_argument('-D', '--document-id', required=True, help='The ID of the document to be shared.')
    parser.add_argument('-e', '--email', action='append', required=True, help='The email address to share the document with. Use multiple -e flags for multiple addresses.')
    parser.add_argument('-r', '--role', default='reader', choices=['reader', 'writer', 'owner'], help='The role to grant the email addresses. (default: reader)')
    parser.add_argument('-C', '--creditation-file', required=True, help='Path to the JSON file containing the service account credentials.')

    args = parser.parse_args()

    if not args.document_id:
        sys.stderr.write('Error: Document ID must be provided.\n')
        sys.exit(1)

    email_addresses = [arg.strip() for arg in args.email]
    print(email_addresses)

    if not email_addresses or not all(is_valid_email(email) for email in email_addresses):
        sys.stderr.write('Error: A valid list of email addresses must be provided.\n')
        sys.exit(1)

    share_document(args.document_id, args.email, args.role, args.creditation_file)
