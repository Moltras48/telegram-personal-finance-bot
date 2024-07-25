import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
BOT_PASSWORD = os.getenv("TELEGRAM_BOT_PASSWORD")