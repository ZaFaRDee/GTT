import asyncio
from config import ALLOWED_USERS, refresh_allowed_users
from telegram import Update
from telegram.ext import CallbackContext
from telegram_utils import send_stock_info_to_user

awaiting_ticker = set()

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

        try:
            asyncio.run(send_stock_info_to_user(ticker, update.effective_chat.id))
        except Exception as e:
            update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")
        return

    if text.lower() == "🔍 askiya haqida to'liq ma'lumot olish:":
        awaiting_ticker.add(user_id)
        update.message.reply_text("📝 Iltimos, aksiya tickerini kiriting (masalan: AAPL)")
        return
