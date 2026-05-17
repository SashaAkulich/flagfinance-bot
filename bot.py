from aiogram import Bot, Dispatcher, types
from storage import VisitStorage
from sheets import GoogleSheetsManager
from urllib.parse import unquote

class FinanceBot:
    def __init__(self, token: str, sheets: GoogleSheetsManager, storage: VisitStorage):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
        self.sheets = sheets
        self.storage = storage
        
        @self.dp.message_handler(commands=['start'])
        async def handle_start(message: types.Message):
            args = message.get_args()
            
            # 🔍 DEBUG: смотрим, что реально пришло
            print(f"🔍 DEBUG: args='{args}'")
            
            visit_id = None
            
            # Дефолтные значения
            utm_data = {
                'utm_source': 'direct',
                'utm_medium': 'direct',
                'utm_campaign': '',
                'utm_content': '',
                'utm_term': ''
            }

            if args:
                # Telegram может передать всё одной строкой: "test_utm&utm_source=website"
                # Или URL-кодировать: "test_utm%26utm_source%3Dwebsite"
                decoded_args = unquote(args)
                print(f"🔍 DEBUG: decoded='{decoded_args}'")
                
                parts = decoded_args.split('&')
                visit_id = parts[0]
                print(f"🔍 DEBUG: visit_id='{visit_id}', parts={parts}")
                
                for part in parts[1:]:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        print(f"🔍 DEBUG: parsing '{key}={value}'")
                        if key in utm_data:
                            utm_data[key] = value
                            print(f"🔍 DEBUG: set {key}={value}")

            print(f"🔍 DEBUG: final utm_data={utm_data}")
            
            try:
                self.sheets.log_lead(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    utm_data=utm_data,
                    visit_id=visit_id or 'direct'
                )
                print(f"✅ Записан лид: {visit_id}, UTM: {utm_data}")
                
                if visit_id and visit_id != 'direct':
                    await message.answer(
                        "Здравствуйте! 👋\n"
                        "Наш менеджер уже получил уведомление и скоро ответит вам."
                    )
                    return
                
            except Exception as e:
                print(f"❌ Ошибка при записи: {e}")
                import traceback
                traceback.print_exc()
            
            await message.answer(
                "Здравствуйте! Чем можем помочь?\n"
                "Опишите ваш запрос, и мы свяжемся с вами."
            )
