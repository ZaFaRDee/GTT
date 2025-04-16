# bot/role_handler.py

from telegram import Update
from telegram.ext import CallbackContext
from bot.admin_menu import get_admin_keyboard
from bot.user_menu import get_user_keyboard
from config import ADMIN_ID

# Foydalanuvchi roli tanlagach chaqiriladi
def role_handler(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "👑 Admin":
        if user_id == ADMIN_ID:
            update.message.reply_text("👑 Admin menyusi:", reply_markup=get_admin_keyboard())
        else:
            update.message.reply_text("⛔ Sizda admin huquqlari mavjud emas.")

    elif text == "👤 User":
        update.message.reply_text("👤 Foydalanuvchi menyusi:", reply_markup=get_user_keyboard())
