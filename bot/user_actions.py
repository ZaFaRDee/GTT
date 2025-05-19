import asyncio

import yfinance as yf
from config import ALLOWED_USERS, refresh_allowed_users
from telegram import Update
from telegram.ext import CallbackContext
from telegram_utils import send_stock_info_to_user

awaiting_ticker = set()

def is_valid_ticker(ticker):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        return bool(info.get("shortName"))  # mavjud kompaniya nomi borligini tekshirish
    except Exception:
        return False

def handle_user_command(update: Update, context: CallbackContext):
    refresh_allowed_users()
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not any(u.get("id") == user_id for u in ALLOWED_USERS):
        update.message.reply_text("🚫 Sizga ruxsat berilmagan.")
        return

    if user_id in awaiting_ticker:
        awaiting_ticker.remove(user_id)
        ticker = text.upper()
        update.message.reply_text("⏳ Iltimos, kuting... Aksiya ma'lumotlari olinmoqda...")

        if not is_valid_ticker(ticker):
            update.message.reply_text(
                "❌ Kiritilgan ticker topilmadi. Iltimos, mavjud birja kodini kiriting (masalan: AAPL, MSFT, TSLA).")
            return

        try:
            asyncio.run(send_stock_info_to_user(ticker, update.effective_chat.id))
        except Exception as e:
            update.message.reply_text("❌ Ichki xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.")
            # logger.error(f"Xatolik: {e}")
        return

    if text.lower() == "🔍 askiya haqida to'liq ma'lumot olish:":
        awaiting_ticker.add(user_id)
        update.message.reply_text("📝 Iltimos, aksiya tickerini kiriting (masalan: AAPL)")
        return
