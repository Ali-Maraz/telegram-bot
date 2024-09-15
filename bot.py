import os
import json
from google.oauth2.service_account import Credentials

creds_data = os.environ.get('GOOGLE_CREDENTIALS')
creds_dict = json.loads(creds_data)
creds = Credentials.from_service_account_info(creds_dict, scopes=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
])

