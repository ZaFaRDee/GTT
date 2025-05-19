# config.py

import os
import json
from dotenv import load_dotenv

load_dotenv()  # .env faylni yuklaydi

GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_FOLDER = os.getenv('GMAIL_FOLDER', 'INBOX')  # default: INBOX

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
# ALLOWED_USERS = int(os.getenv("ALLOWED_USERS", "0"))

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


# ALLOWED_USERS endi JSON fayldan
def load_allowed_users():
    try:
        with open("allowed_users.json", "r") as f:
            return json.load(f)
    except:
        return []

def refresh_allowed_users():
    global ALLOWED_USERS
    try:
        with open("allowed_users.json", "r") as f:
            ALLOWED_USERS = json.load(f)
    except FileNotFoundError:
        ALLOWED_USERS = []

ALLOWED_USERS = load_allowed_users()

