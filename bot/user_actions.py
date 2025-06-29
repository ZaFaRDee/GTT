import asyncio
import yfinance as yf
import threading
import config
from config import ALLOWED_USERS, refresh_allowed_users
from telegram import Update
from telegram.ext import CallbackContext
from telegram_utils import (
    send_fundamental_info_to_user,
    send_sentimental_info_to_user,
    send_barchart_options_screenshot_to_user,
    send_halal_info_to_user  # ✅ Yangi funksiya qo‘shildi
)

# Foydalanuvchi uchun kutilyotgan ticker turi: "fundamental", "sentimental", "putcall", "halal"
awaiting_ticker = {}

def is_valid_ticker(ticker):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        return bool(info.get("shortName"))
    except Exception:
        return False

def handle_user_command(update: Update, context: CallbackContext):
    refresh_allowed_users()
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not any(u.get("id") == user_id for u in config.ALLOWED_USERS):
        update.message.reply_text("🚫 Sizga ruxsat berilmagan.")
        return

    # ✅ Ticker kutilayotgan foydalanuvchi uchun
    if user_id in awaiting_ticker:
        analysis_type = awaiting_ticker.pop(user_id)
        ticker = text.upper()
        update.message.reply_text("⏳ Iltimos, kuting... Aksiya ma'lumotlari olinmoqda...")

        if not is_valid_ticker(ticker):
            update.message.reply_text(
                "❌ Kiritilgan ticker topilmadi. Iltimos, mavjud birja kodini kiriting (masalan: AAPL, MSFT, TSLA).")
            return

        def run_analysis_thread():
            try:
                if analysis_type == "fundamental":
                    asyncio.run(send_fundamental_info_to_user(ticker, update.effective_chat.id))
                elif analysis_type == "sentimental":
                    asyncio.run(send_sentimental_info_to_user(ticker, update.effective_chat.id))
                elif analysis_type == "putcall":
                    asyncio.run(send_barchart_options_screenshot_to_user(ticker, update.effective_chat.id))
                elif analysis_type == "halal":
                    send_halal_info_to_user(ticker, update.effective_chat.id)  # ✅ Yangi funksiya
            except Exception as e:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Ichki xatolik yuz berdi. Keyinroq qayta urinib ko‘ring."
                )

        threading.Thread(target=run_analysis_thread).start()
        return

    # 📊 Fundamental tahlil
    if text == "📊 Fundamental tahlil":
        awaiting_ticker[user_id] = "fundamental"
        update.message.reply_text("📝 Iltimos, ticker kiriting (masalan: AAPL):")
        return

    # 📰 Sentimental tahlil
    if text == "📰 Sentimental tahlil":
        awaiting_ticker[user_id] = "sentimental"
        update.message.reply_text("📝 Iltimos, ticker kiriting (masalan: TSLA):")
        return

    # 📈 Put/Call ma'lumot
    if text == "📈 Put/Call ma'lumot":
        awaiting_ticker[user_id] = "putcall"
        update.message.reply_text("📝 Iltimos, ticker kiriting (masalan: TSLA):")
        return

    # 🔎 Halollikka tekshirish
    if text == "🔎 Halollikka tekshirish":
        awaiting_ticker[user_id] = "halal"
        update.message.reply_text("📝 Iltimos, ticker kiriting (masalan: GOOGL):")
        return
