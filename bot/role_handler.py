# bot/role_handler.py

from telegram import Update
from telegram.ext import CallbackContext

import config
from bot.admin_menu import get_admin_keyboard
from bot.user_menu import get_user_keyboard


def role_handler(update: Update, context: CallbackContext):
    config.refresh_allowed_users()  # ✅ Run-time yangilanish

    text = update.message.text
    user_id = update.effective_user.id

    if text == "👑 Admin":
        if user_id == config.ADMIN_ID:
            context.user_data["role"] = "admin"
            update.message.reply_text("👑 Admin menyusi:", reply_markup=get_admin_keyboard())
        else:
            update.message.reply_text("⛔ Sizda admin huquqlari mavjud emas.")


    elif text == "👤 User":
        # ✅ Yangilangan tekshiruv — ID dict ichida bormi?
        if any(u.get("id") == user_id for u in config.ALLOWED_USERS):
            update.message.reply_text("👤 Foydalanuvchi menyusi:", reply_markup=get_user_keyboard())
        else:
            update.message.reply_text("⛔ Sizda user huquqlari mavjud emas.")
