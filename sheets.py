import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

class GoogleSheetsManager:
    def __init__(self, sheet_id: str, credentials_json: str):
        scope = ['https://spreadsheets.google.com/feeds', 
                 'https://www.googleapis.com/auth/drive']
        
        # Преобразуем JSON строку в словарь
        creds_dict = json.loads(credentials_json)
        
        # Создаем креды из словаря
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(sheet_id).sheet1

  def log_lead(self, telegram_id: int, username: str, utm_data: dict, visit_id: str):
        row = [
            telegram_id,
            username or '',
            utm_data.get('utm_source', ''),
            utm_data.get('utm_medium', ''),
            utm_data.get('utm_campaign', ''),
            utm_data.get('utm_term', ''),
            utm_data.get('utm_content', ''),
            visit_id,
        ]
        self.sheet.append_row(row)
