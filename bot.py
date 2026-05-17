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
            
            # Парсим параметры из start
            visit_id = None
            utm_data = {}
            
            if args:
                # Проверяем, есть ли UTM-параметры в ссылке
                if '&' in args or 'utm_' in args:
                    # Разбираем как URL параметры
                    from urllib.parse import parse_qs, urlparse
                    parsed = urlparse(f"http://t.me/bot?start={args}")
                    params = parse_qs(parsed.query)
                    
                    visit_id = params.get('start', [None])[0]
                    utm_data = {
                        'utm_source': params.get('utm_source', ['direct'])[0],
                        'utm_medium': params.get('utm_medium', ['direct'])[0],
                        'utm_campaign': params.get('utm_campaign', [''])[0],
                        'utm_content': params.get('utm_content', [''])[0],
                        'utm_term': params.get('utm_term', [''])[0]
                    }
                else:
                    # Простой start параметр без UTM
                    visit_id = args
                    utm_data = {
                        'utm_source': 'direct',
                        'utm_medium': 'direct',
                        'utm_campaign': '',
                        'utm_content': '',
                        'utm_term': ''
                    }
            else:
                # Нет параметров — прямой запуск
                utm_data = {
                    'utm_source': 'direct',
                    'utm_medium': 'direct',
                    'utm_campaign': '',
                    'utm_content': '',
                    'utm_term': ''
                }
            
            try:
                # Записываем в таблицу ВСЕГДА
                self.sheets.log_lead(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    utm_data=utm_data,
                    visit_id=visit_id or 'direct'
                )
                print(f"✅ Записан лид: {visit_id}, UTM: {utm_data}")
                
                # Ответ для пользователей с меткой
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
            
            # Ответ для обычных пользователей
            await message.answer(
                "Здравствуйте! Чем можем помочь?\n"
                "Опишите ваш запрос, и мы свяжемся с вами."
            )
