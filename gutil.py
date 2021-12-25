import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from yt_dlp import YoutubeDL

MIME_EXT = {
    "audio/aac": "aac",
    "video/x-msvideo": "avi",
    "image/bmp": "bmp",
    "application/x-bzip": "bz",
    "application/x-bzip2": "bz2",
    "text/css": "css",
    "text/csv": "csv",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/epub+zip": "epub",
    "application/gzip": "gz",
    "image/gif": "gif",
    "text/html": "html",
    "image/vnd.microsoft.icon": "ico",
    "text/calendar": "ics",
    "application/java-archive": "jar",
    "image/jpeg": "jpeg",
    "text/javascript": "js",
    "application/json": "json",
    "audio/midi": "mid",
    "audio/x-midi": "midi",
    "audio/mpeg": "mp3",
    "video/mp4": "mp4",
    "video/mpeg": "mpeg",
    "font/otf": "otf",
    "image/png": "png",
    "application/pdf": "pdf",
    "application/x-httpd-php": "php",
    "application/vnd.ms-powerpoint": "ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.rar": "rar",
    "application/rtf": "rtf",
    "image/svg+xml": "svg",
    "application/x-tar": "tar",
    "image/tiff": "tiff",
    "video/mp2t": "ts",
    "font/ttf": "ttf",
    "text/plain": "txt",
    "audio/wav": "wav",
    "video/webm": "webm",
    "application/xhtml+xml": "xhtml",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/xml": "xml",
    "application/zip": "zip",
    "application/x-7z-compressed": "7z"
}
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
GSERVICE = None


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=5818)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def make_service(creds):
    try:
        global GSERVICE
        GSERVICE = build("drive", "v3", credentials=creds)
        return GSERVICE
    except HttpError as err:
        print(err)


def download_drive_file(file_id, path=None):
    if not GSERVICE:
        make_service(get_credentials())
    meta = GSERVICE.files().get(fileId=file_id).execute()
    filename = "".join([c for c in meta["name"] if re.match(r"\w", c)]) + "."

    if meta["mimeType"] in MIME_EXT:
        req = GSERVICE.files().get_media(fileId=file_id)
        filename = filename + MIME_EXT[meta["mimeType"]]
    else:
        req = GSERVICE.files().export_media(fileId=file_id, mimeType="application/pdf")
        filename = filename + "pdf"

    filepath = path + "/" + filename if path else filename
    fh = open(filepath, "wb")
    downloader = MediaIoBaseDownload(fh, req)
    done = False
    while done is False:
        status, done = downloader.next_chunk()


def fileid_from_url(url):
    return url[url.rindex("/d/") + 3:url.rindex("/")]


YTDLP_OPTS = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
    "cookiesfrombrowser": ("chrome",),
    "quiet": "True"
}
YTDL = None


def init_ytdl():
    global YTDL
    input("WARNING: Some videos may be private and require Berkeley authentication. \n" +
          "Please sign in to your Berkeley Youtube account within Chrome to ensure videos download.\n" +
          "Press enter to continue...")
    YTDL = YoutubeDL(YTDLP_OPTS)
    return YTDL


def download_youtube_video(url):
    if not YTDL:
        init_ytdl()
    YTDL.download([url])