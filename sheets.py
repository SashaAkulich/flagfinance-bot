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
            
            # Открываем таблицу по ID
            spreadsheet = self.client.open_by_key(sheet_id)
            print(f"📄 [Sheets] Таблица найдена: {spreadsheet.title}")
            
            # Получаем ПЕРВЫЙ лист (по индексу 0)
            self.sheet = spreadsheet.get_worksheet(0)
            print(f"📋 [Sheets] Используем лист: {self.sheet.title}")
            
            # Проверяем заголовки
            headers = self.sheet.row_values(1)
            print(f"📝 [Sheets] Заголовки: {headers}")
            
            if not headers:
                print("⚠️ [Sheets] Заголовков нет, создаю...")
                self.sheet.append_row([
                    "Telegram ID", "Username", "UTM Source", "UTM Medium",
                    "UTM Campaign", "UTM Term", "UTM Content", "Visit ID", "Timestamp"
                ])
            
            print("✅ [Sheets] Подключение готово!")
            
        except Exception as e:
            print(f"❌ [Sheets] Ошибка: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def log_lead(self, telegram_id: int, username: str, utm_data: dict, visit_id: str):
        print(f"🔍 [Sheets] Запись: telegram_id={telegram_id}")
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row = [
                telegram_id,
                f"@{username}" if username else "N/A",
                utm_data.get('utm_source', ''),
                utm_data.get('utm_medium', ''),
                utm_data.get('utm_campaign', ''),
                utm_data.get('utm_term', ''),
                utm_data.get('utm_content', ''),
                visit_id,
                timestamp
            ]
            
            print(f"📤 [Sheets] Отправляю: {row}")
            result = self.sheet.append_row(row)
            print(f"✅ [Sheets] Записано! Range: {result}")
            
        except Exception as e:
            print(f"❌ [Sheets] Ошибка записи: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
