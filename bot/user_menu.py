from telegram import ReplyKeyboardMarkup

def get_user_keyboard():
    keyboard = [
        ["🔍 Askiya haqida to'liq ma'lumot olish:"],
        ["🔙 Ortga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
