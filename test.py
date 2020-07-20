from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from datetime import datetime
import _thread
import pprint
import io
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'xstorage1.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list(pageSize=1000, fields="files(id, name, mimeType)").execute()
print(results)

stamp1 = datetime.now().timestamp()
request = service.files().get_media(fileId='1D-ADlExV279xUbN6F-1tRH3yIDpu6v9F')
fh = io.FileIO('glow.db', 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))
stamp2 = datetime.now().timestamp()
print(stamp2-stamp1)
