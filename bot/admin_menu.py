from telegram import ReplyKeyboardMarkup

def get_admin_keyboard():
    keyboard = [
        ["🛰 Monitoring holati", "📩 Oxirgi signal"],
        ["📊 Ish vaqti", "📡 Bot holati"],
        ["⏸ Pauza", "▶️ Davom et"],
        ["⏱ Intervalni sozlash", "✉️ Gmail test"],
        ["⚙️ Konfiguratsiya", "♻️ Qayta yuklash"],
        ["💾 Xotira holati", "🔁 Qayta ishga tushirish"],
        ["🧪 Simulyatsiya (ticker)", "👤 User qo'shish"],
        ["📋 Foydalanuvchilar ro‘yxati", "➖ Userni o‘chirish"],
        ["🔙 Ortga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
