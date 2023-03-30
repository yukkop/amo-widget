import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import sys

def create_document(title, return_link=False):
    try:
        creds = service_account.Credentials.from_service_account_file('./creditations.json')
        docs_service = build('docs', 'v1', credentials=creds)

        document = docs_service.documents().create(
            body={
                'title': title,
                'body': {
                    'content': [
                        {
                            'paragraph': {
                                'elements': [
                                    {
                                        'textRun': {
                                            'content': 'This is my first paragraph.'
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            'paragraph': {
                                'elements': [
                                    {
                                        'textRun': {
                                            'content': 'This is my second paragraph.'
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ).execute()

        document_id = document.get('documentId')

        if return_link:
            document_url = f'https://docs.google.com/document/d/{document_id}/edit'
            return document_url
        else:
            return document_id

    except HttpError as error:
        sys.stderr.write(f'An error occurred: {error}\n')
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Google Document.')
    parser.add_argument('-t', '--title', required=True, help='The title of the new document.')
    parser.add_argument('-l', '--link', action='store_true', help='Return the document link instead of the document ID.')

    args = parser.parse_args()

    result = create_document(args.title, args.link)
    print(result)
