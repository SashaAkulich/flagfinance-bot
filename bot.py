from aiogram import Bot, Dispatcher, types
from storage import VisitStorage
from sheets import GoogleSheetsManager

class FinanceBot:
    def __init__(self, token: str, sheets: GoogleSheetsManager, storage: VisitStorage):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
        self.sheets = sheets
        self.storage = storage
        
        @self.dp.message_handler(commands=['start'])
        async def handle_start(message: types.Message):
            args = message.get_args()
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
                # Telegram передаёт всё после ?start= одной строкой
                parts = args.split('&')
                visit_id = parts[0]  # Первый элемент всегда visit_id
                
                # Разбираем остальные параметры
                for part in parts[1:]:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        if key in utm_data:
                            utm_data[key] = value

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
                        "Здравствуйте! \n"
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
