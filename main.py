# main.py

import os
import sys
import time

import asyncio
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,
    MessageHandler, Filters
)

from admin_commands import (
    is_monitoring_paused, get_interval, set_last_alert_time
)
from bot.admin_actions import handle_admin_command
from bot.back_handler import handle_back
from bot.role_handler import role_handler
from config import TELEGRAM_BOT_TOKEN
from gmail_utils import get_new_alerts
from telegram_utils import send_alerts_to_telegram

# Global holat: tanlangan foydalanuvchi rollari
user_roles = {}

def start(update: Update, context: CallbackContext):
    keyboard = [["👑 Admin", "👤 User"]]
    from telegram import ReplyKeyboardMarkup
    update.message.reply_text(
        "Iltimos, rolingizni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


def check_for_restart_signal():
    return os.path.exists("RESTART_SIGNAL")

def clear_restart_signal():
    if os.path.exists("RESTART_SIGNAL"):
        os.remove("RESTART_SIGNAL")

async def main():
    print("✅ Bot ishga tushdi...")

    # updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    # dispatcher = updater.dispatcher
    #
    # # /start bosilganda rol tanlash menyusi chiqadi
    # dispatcher.add_handler(CommandHandler("start", start))
    #
    # # Roldan keyingi tugma menyuni ko‘rsatish
    # dispatcher.add_handler(MessageHandler(Filters.regex("^(👑 Admin|👤 User)$"), role_handler))
    # dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex("^.*"), handle_admin_command))
    # dispatcher.add_handler(MessageHandler(Filters.text("🔙 Ortga"), handle_back))
    #
    # updater.start_polling()

    if check_for_restart_signal():
        print("♻️ Restart signal topildi, qayta ishga tushiryapman...")
        clear_restart_signal()
        os.execv(sys.executable, ['python'] + sys.argv)

    # === Monitoring sikli ===
    while True:
        try:
            if not is_monitoring_paused():
                alerts = get_new_alerts()
                if alerts:
                    await send_alerts_to_telegram(alerts)
                    set_last_alert_time()
                    print(f"📤 {len(alerts)} ta alert yuborildi.")
                else:
                    print("📭 Yangi alert topilmadi.")
            else:
                print("⏸ Monitoring vaqtincha to‘xtatilgan.")

        except Exception as e:
            print(f"❗ Kutilmagan xato: {e}")

        time.sleep(get_interval())

    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())