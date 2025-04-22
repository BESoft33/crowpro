import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()
# Replace with your actual values
APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")

# URL for Dropbox OAuth2 token request
url = "https://api.dropboxapi.com/oauth2/token"

# Data to be sent in the POST request
data = {
    'code': AUTHORIZATION_CODE,
    'grant_type': 'authorization_code'
}

# Send POST request with basic auth and form data
response = requests.post(url,
                         data=data,
                         auth=HTTPBasicAuth(APP_KEY, APP_SECRET),
                         headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Print the response (JSON)
print(response.json())
