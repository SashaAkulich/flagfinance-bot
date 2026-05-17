import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

class GoogleSheetsManager:
    def __init__(self, sheet_id: str, credentials_json: str):
        print(f"🔍 [Sheets] Инициализация: sheet_id={sheet_id}")
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds_dict = json.loads(credentials_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(sheet_id).sheet1
            print("✅ [Sheets] Подключение к таблице успешно!")
        except Exception as e:
            print(f"❌ [Sheets] Ошибка подключения: {type(e).__name__}: {e}")
            raise
    
    def log_lead(self, telegram_id: int, username: str, utm_data: dict, visit_id: str):
        print(f"🔍 [Sheets] log_lead вызван: telegram_id={telegram_id}, visit_id={visit_id}")
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row = [
                telegram_id,                           # A: Telegram ID
                f"@{username}" if username else "N/A", # B: Username
                utm_data.get('utm_source', ''),        # C: UTM Source
                utm_data.get('utm_medium', ''),        # D: UTM Medium
                utm_data.get('utm_campaign', ''),      # E: UTM Campaign
                utm_data.get('utm_term', ''),          # F: UTM Term
                utm_data.get('utm_content', ''),       # G: UTM Content
                visit_id,                              # H: Visit ID
                timestamp                              # I: Timestamp
            ]
            
            print(f"🔍 [Sheets] Отправляю строку: {row}")
            self.sheet.append_row(row)
            print("✅ [Sheets] Строка успешно добавлена!")
            
        except Exception as e:
            print(f"❌ [Sheets] Ошибка записи: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
