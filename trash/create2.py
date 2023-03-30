from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
docs_service = build('docs', 'v1', credentials=creds)


# Create a new document
document = docs_service.documents().create(body={
    'title': 'My New Document'
}).execute()

document_id = document.get('documentId')

# Batch update the document to add new content
requests = [
    {
        'insertText': {
            'location': {
                'index': 1
            },
            'text': 'Hello, World!\n'
        }
    }
]

docs_service.documents().batchUpdate(documentId=document_id, body={
    'requests': requests
}).execute()

document_id = document.get('documentId')
print('Created document with title: {0} and document ID: {1}'.format(
    document.get('title'), document_id))

# Retrieve the document content
doc_content = docs_service.documents().get(documentId=document_id).execute()
body_content = doc_content.get('body').get('content')

# Check if the body content is not empty
if len(body_content) > 0:
    print('Document body is not empty')
    print(body_content)
else:
    print('Document body is empty')


document_id = document.get('documentId')
print('\n\nCreated document with title: {0} and document ID: {1}'.format(
    document.get('title'), document_id))

document_url = f'https://docs.google.com/document/d/{document_id}/edit'
print('Document URL:', document_url)

