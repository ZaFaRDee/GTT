# bot/back_handler.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

# Ortga tugmasi bosilganda rol tanlash paneliga qaytaradi
def handle_back(update: Update, context: CallbackContext):
    keyboard = [["👑 Admin", "👤 User"]]
    update.message.reply_text(
        "Rolni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
