from telegram import ReplyKeyboardMarkup

def get_user_keyboard():
    keyboard = [
        ["📊 Fundamental tahlil"],
        ["📰 Sentimental tahlil"],
        # ["📈 Put/Call ma'lumot"],
        ["🔙 Ortga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
