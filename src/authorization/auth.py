import ee  # Earth Engine API
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle  # nosec B403
from typing import Any
from src.config import CLIENT_SECRET_FILE


SCOPES = [
    "https://www.googleapis.com/auth/earthengine",
    "https://www.googleapis.com/auth/drive",
]

CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
TOKEN_PICKLE_FILE = "../token.pickle"  # nosec B105


def authenticate_google_api():
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)  # nosec B301

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(
                port=0
            )  # port=0 lets the system pick a free port

        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


def initialize_earth_engine(creds: Any) -> Any:
    ee.Initialize(credentials=creds)
