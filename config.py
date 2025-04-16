# config.py

from dotenv import load_dotenv
import os

load_dotenv()  # .env faylni yuklaydi

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_FOLDER = os.getenv('GMAIL_FOLDER', 'INBOX')  # default: INBOX

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
