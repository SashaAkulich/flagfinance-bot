from fastapi import FastAPI, Request
from bot import FinanceBot
from sheets import GoogleSheetsManager
from storage import VisitStorage
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

sheets = GoogleSheetsManager(
    sheet_id=os.getenv('GOOGLE_SHEET_ID'),
    credentials_json=os.getenv('GOOGLE_CREDENTIALS_JSON')
)
storage = VisitStorage()
bot = FinanceBot(
    token=os.getenv('TELEGRAM_BOT_TOKEN'),
    sheets=sheets,
    storage=storage
)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = types.Update(**update_data)
    await bot.dp.process_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "ok", "bot": "running"}
