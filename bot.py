import os
import json
from google.oauth2.service_account import Credentials

creds_data = os.environ.get('GOOGLE_CREDENTIALS')
if creds_data is None:
    print("GOOGLE_CREDENTIALS переменная окружения не найдена.")
else:
    creds_dict = json.loads(creds_data)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
