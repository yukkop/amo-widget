import uuid
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# Set up the credentials and API client
creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
docs_service = build('docs', 'v1', credentials=creds)

# Generate a new GUID
new_guid = uuid.uuid4()

# Define the properties of the new document
doc_title = 'Document #' + str(new_guid)
body = {
    'title': doc_title
}

# Create the new document
doc = docs_service.documents().create(body=body).execute()

# Get the webViewLink for the new document
doc_url = doc['webViewLink']

print(f'The URL for the new document is: {doc_url}')
