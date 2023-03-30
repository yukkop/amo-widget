python=cat <<EOF import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# args - 1: doc id, 2: email address

# Set up credentials and API client
creds = service_account.Credentials.from_service_account_file\('/home/yukkop/projects/gwp/google/docspatterns-5d2c00d24c0f.json'\)
drive_service = build\('drive', 'v3', credentials=creds\)

# Get the ID of the document you want to share
document_id = '17qmsgC0UBobi2WJWoMLyISDsgkHyQnT_j1nRp8l6_es'

# Define the permission to be granted \(in this case, view permission\)
permission = {
    'type': 'user',
    'role': 'reader',
    'emailAddress': 'hectic.yukkop@gmail.com'
}

# Add the permission to the document
try:
    permission = drive_service.permissions\(\).create\(
        fileId=document_id,
        body=permission,
        sendNotificationEmail=False
    \).execute\(\)
    print\('Permission ID: %s' % permission.get\('id'\)\)

except HttpError as error:
    print\('An error occurred: %s' % error\)
EOF 


cat $python | python
