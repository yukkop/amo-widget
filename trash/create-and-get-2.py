import uuid
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Authenticate with the Google Drive API using a service account
creds = service_account.Credentials.from_service_account_file('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json')
service = build('drive', 'v3', credentials=creds)

# Generate a new GUID
new_guid = uuid.uuid4()

# Convert the GUID to a string
guid_str = str(new_guid)

# Set the document title
doc_title = 'Document #' + guid_str

# Create the document
try:
    doc = service.files().create(body={
        'name': doc_title,
        'parents': ['17ovX6AEazr2tQWgILE8L7rlQ8c0_TfoG'],
        'mimeType': 'application/vnd.google-apps.document'
    }).execute()
except HttpError as error:
    print(f"An error occurred: {error}")
    doc_url = None
else:
    # Get the document URL
    try:
        doc_url = doc['webViewLink']
    except KeyError:
        print("Document was not created successfully.")
        doc_url = None

print(doc_url)
