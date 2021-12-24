import os.path
import re
import extension

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=5818)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def make_service(creds):
    try:
        return build("drive", "v3", credentials=creds)
    except HttpError as err:
        print(err)


SERVICE = make_service(get_credentials())


def download_drive_file(file_id, path=None):
    meta = SERVICE.files().get(fileId=file_id).execute()
    print(meta)
    filename = "".join([c for c in meta["name"] if re.match(r"\w", c)]) + "."

    if meta["mimeType"] in extension.MIME_EXT:
        req = SERVICE.files().get_media(fileId=file_id)
        filename = filename + extension.MIME_EXT[meta["mimeType"]]
    else:
        req = SERVICE.files().export_media(fileId=file_id, mimeType="application/pdf")
        filename = filename + "pdf"

    filepath = path + "/" + filename if path else filename
    fh = open(filepath, "wb")
    downloader = MediaIoBaseDownload(fh, req)
    done = False
    while done is False:
        status, done = downloader.next_chunk()