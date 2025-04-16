from telegram import Update
from telegram.ext import CallbackContext

from config import ADMIN_ID
from .admin_menu import get_admin_keyboard
from .user_menu import get_user_keyboard


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("👑 Admin menyusi:", reply_markup=get_admin_keyboard())
    else:
        update.message.reply_text("👤 Foydalanuvchi menyusi:", reply_markup=get_user_keyboard())
