from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
docs_service = build('docs', 'v1', credentials=creds)

document = docs_service.documents().create(
    body={
        'title': 'My New Document',
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
print('Created document with title: {0} and document ID: {1}'.format(
    document.get('title'), document_id))

document_url = f'https://docs.google.com/document/d/{document_id}/edit'
print('Document URL:', document_url)
