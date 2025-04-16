from telegram import ReplyKeyboardMarkup

def get_user_keyboard():
    keyboard = [
        ["📈 Oxirgi signal", "ℹ️ Bot haqida"],
        ["🕒 Ish vaqti", "🔄 Yangilash"],
        ["🔙 Ortga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
