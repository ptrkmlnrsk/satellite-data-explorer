import ee # Earth Engine API
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
from typing import Any
# To store/load credentials securely

# Define the scopes your application needs.
# For Earth Engine, typically 'https://www.googleapis.com/auth/earthengine'
# or 'https://www.googleapis.com/auth/cloud-platform' might be suitable
# depending on your specific needs. Start with Earth Engine specific scope.
SCOPES = ['https://www.googleapis.com/auth/earthengine']

# The path to your client_secret.json file downloaded from Google Cloud Console.
CLIENT_SECRET_FILE = '../client_secret.json'
# The file where user credentials will be stored securely. Add this to .gitignore!
TOKEN_PICKLE_FILE = '../token.pickle'

def authenticate_google_api():
    """Authenticates the user and returns valid credentials."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0) # port=0 lets the system pick a free port

        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def initialize_earth_engine(creds: Any) -> Any:
    """Initializes Earth Engine with the provided credentials."""
    # This tells the Earth Engine API to use the Google Auth credentials
    ee.Initialize(credentials=creds)
    print("Earth Engine initialized successfully!")

#if __name__ == '__main__':
#    # Step 1: Authenticate and get credentials
#    credentials = authenticate_google_api()
#
#    # Step 2: Initialize Earth Engine with the obtained credentials
#    initialize_earth_engine(credentials)
#
#    # Now you can use Earth Engine APIs, for example, to get a simple image:
#    try:
#        image = ee.Image('LANDSAT/LE07/C01/T1_SR/LE07_038029_20030810')
#        print(f"Successfully loaded a Landsat image: {image.getInfo()['id']}")
#    except ee.EEException as e:
#        print(f"Error accessing Earth Engine: {e}")

