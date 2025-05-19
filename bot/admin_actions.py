# bot/admin_actions.py

import json
from telegram import Update
from telegram.ext import CallbackContext
from admin_commands import (
    status, lastalert, uptime, ping, pause, resume, setinterval,
    email_test, show_config, reload_config, memory, restart_bot, simulate
)
from config import refresh_allowed_users

awaiting_interval = set()
awaiting_user_id = set()
awaiting_remove_user_id = set()

def handle_admin_command(update: Update, context: CallbackContext):
    global awaiting_interval, awaiting_user_id
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # 🔁 Keyingi matn ID bo‘lsa:
    if user_id in awaiting_user_id:
        if not text.isdigit():
            return update.message.reply_text("❗ Faqat raqamli Telegram ID yuboring.")

        new_user_id = int(text)
        new_username = None

        # Agar foydalanuvchi botga yozgan bo‘lsa — uning username ni olishga harakat qilamiz
        try:
            chat_member = context.bot.get_chat(new_user_id)
            new_username = chat_member.username
        except:
            pass  # topilmasa, None qoladi

        try:
            with open("allowed_users.json", "r") as f:
                allowed = json.load(f)
        except:
            allowed = []

        # ID ro‘yxatda bormi — tekshir
        if any(u['id'] == new_user_id for u in allowed):
            reply = "ℹ️ Bu foydalanuvchi allaqachon ro'yxatda."
        else:
            allowed.append({
                "id": new_user_id,
                "username": new_username
            })
            with open("allowed_users.json", "w") as f:
                json.dump(allowed, f)

            from config import refresh_allowed_users
            refresh_allowed_users()
            reply = f"✅ {new_user_id} foydalanuvchi ro'yxatga qo‘shildi."

        awaiting_user_id.remove(user_id)
        return update.message.reply_text(reply)

    # 🟢 2. Interval sozlanmoqda
    if user_id in awaiting_interval:
        context.args = [text]
        awaiting_interval.remove(user_id)
        return setinterval(update, context)

    # Bu shart ID yuborilganidan keyingi holatda ishlaydi
    if user_id in awaiting_remove_user_id:
        return remove_user(update, context)

    # 🔵 3. Oddiy admin menyu tugmalari
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
    elif text == "👤 User qo'shish":
        awaiting_user_id.add(user_id)
        return update.message.reply_text("📝 Iltimos, yangi Telegram ID raqamini yuboring:")
    elif text == "📋 Foydalanuvchilar ro‘yxati":
        return user_list(update, context)
    elif text == "➖ Userni o‘chirish":
        return remove_user(update, context)
    elif text == "🔙 Ortga":
        from .back_handler import handle_back
        return handle_back(update, context)

def user_list(update: Update, context: CallbackContext):
    try:
        with open("allowed_users.json", "r") as f:
            allowed = json.load(f)

        if not allowed:
            return update.message.reply_text("📭 Ro'yxatda foydalanuvchi yo'q.")

        reply = "📋 Ruxsat etilgan foydalanuvchilar:\n\n"
        for user in allowed:
            uid = user.get("id")
            username = user.get("username") or "Username yo'q"
            reply += f"🔹 ID: <code>{uid}</code>\n  👤 @{username}\n\n"

        return update.message.reply_text(reply, parse_mode='HTML')

    except Exception as e:
        return update.message.reply_text(f"❌ Xatolik: {str(e)}")


def remove_user(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in awaiting_remove_user_id:
        if not text.isdigit():
            return update.message.reply_text("❗ Faqat Telegram ID raqamini yuboring.")

        try:
            remove_id = int(text)
            with open("allowed_users.json", "r") as f:
                allowed = json.load(f)

            # 🔍 user ID bo‘yicha topish
            updated_allowed = [u for u in allowed if u.get("id") != remove_id]

            if len(updated_allowed) == len(allowed):
                reply = "⚠️ Bu ID ro'yxatda topilmadi."
            else:
                with open("allowed_users.json", "w") as f:
                    json.dump(updated_allowed, f, indent=2)

                from config import refresh_allowed_users
                refresh_allowed_users()

                reply = f"✅ {remove_id} foydalanuvchi ro'yxatdan o‘chirildi."

            awaiting_remove_user_id.remove(user_id)
            return update.message.reply_text(reply)

        except Exception as e:
            return update.message.reply_text(f"❌ Xatolik: {str(e)}")

    # Admin tugmani bosganda holatni belgilash
    if text == "➖ Userni o‘chirish":
        awaiting_remove_user_id.add(user_id)
        return update.message.reply_text("🗑 Iltimos, o‘chirish uchun Telegram ID raqamini yuboring:")
