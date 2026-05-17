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
    
    # Дефолтные значения
    utm_data = {
        'utm_source': 'direct',
        'utm_medium': 'direct',
        'utm_campaign': '',
        'utm_content': '',
        'utm_term': ''
    }
    visit_id = 'direct'

    if args:
        # Парсим формат: visit_id|source|medium|campaign|content|term
        parts = args.split('|')
        visit_id = parts[0] if len(parts) > 0 else 'direct'
        
        if len(parts) > 1 and parts[1]: utm_data['utm_source'] = parts[1]
        if len(parts) > 2 and parts[2]: utm_data['utm_medium'] = parts[2]
        if len(parts) > 3 and parts[3]: utm_data['utm_campaign'] = parts[3]
        if len(parts) > 4 and parts[4]: utm_data['utm_content'] = parts[4]
        if len(parts) > 5 and parts[5]: utm_data['utm_term'] = parts[5]

    try:
        self.sheets.log_lead(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            utm_data=utm_data,
            visit_id=visit_id
        )
        print(f"✅ Записан лид: {visit_id}, UTM: {utm_data}")
        
        if visit_id != 'direct':
            await message.answer(
                "Здравствуйте! 👋\n"
                "Наш менеджер уже получил уведомление и скоро ответит вам."
            )
            return
                
    except Exception as e:
        print(f"❌ Ошибка при записи: {e}")
    
    await message.answer(
        "Здравствуйте! Чем можем помочь?\n"
        "Опишите ваш запрос, и мы свяжемся с вами."
    )
