# bot/admin_actions.py

from telegram import Update
from telegram.ext import CallbackContext
from admin_commands import (
    status, lastalert, uptime, ping, pause, resume, setinterval,
    email_test, show_config, reload_config, memory, restart_bot, simulate
)

awaiting_interval = set()

# Admin menyudagi tugmalarni qayta ishlash

def handle_admin_command(update: Update, context: CallbackContext):
    global awaiting_interval
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in awaiting_interval:
        context.args = [text]  # foydalanuvchi yuborgan sonni argument sifatida o‘tkazamiz
        awaiting_interval.remove(user_id)
        return setinterval(update, context)

    if text == "🛰 Monitoring holati":
        return status(update, context)
    elif text == "📩 Oxirgi signal":
        return lastalert(update, context)
    elif text == "📊 Ish vaqti":
        return uptime(update, context)
    elif text == "📡 Bot holati":
        return ping(update, context)
    elif text == "⏸ Pauza":
        return pause(update, context)
    elif text == "▶️ Davom et":
        return resume(update, context)
    elif text == "⏱ Intervalni sozlash":
        awaiting_interval.add(user_id)
        return update.message.reply_text("✏️ Iltimos, yangi intervalni soniya ko‘rinishida kiriting (masalan: 30)")
    elif text == "✉️ Gmail test":
        return email_test(update, context)
    elif text == "⚙️ Konfiguratsiya":
        return show_config(update, context)
    elif text == "♻️ Qayta yuklash":
        return reload_config(update, context)
    elif text == "💾 Xotira holati":
        return memory(update, context)
    elif text == "🔁 Qayta ishga tushirish":
        return restart_bot(update, context)
    elif text == "🧪 Simulyatsiya (ticker)":
        return simulate(update, context)
    elif text == "🔙 Ortga":
        from .back_handler import start
        return start(update, context)
