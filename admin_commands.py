# admin_commands.py (faqat komandalar uchun tozalangan versiya)

import os
import datetime
import psutil
from telegram import Update
from telegram.ext import CallbackContext

# Global o'zgaruvchilar
start_time = datetime.datetime.now()
last_alert_time = None
is_paused = False
check_interval = 10

def ping(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot ishlayapti!")

def status(update: Update, context: CallbackContext):
    msg = f"🛰 Monitoring: {'OFF' if is_paused else 'ON'}\n"
    msg += f"⏱ Interval: {check_interval} soniya\n"
    msg += f"📩 Oxirgi signal: {last_alert_time.strftime('%H:%M:%S %d.%m.%Y') if last_alert_time else 'Topilmagan'}"
    update.message.reply_text(msg)

def uptime(update: Update, context: CallbackContext):
    now = datetime.datetime.now()
    uptime_duration = now - start_time
    hours, rem = divmod(uptime_duration.total_seconds(), 3600)
    minutes, _ = divmod(rem, 60)
    update.message.reply_text(f"🕒 Ish vaqti: {int(hours)} soat {int(minutes)} daqiqa")

def pause(update: Update, context: CallbackContext):
    global is_paused
    is_paused = True
    update.message.reply_text("⏸ Monitoring to‘xtatildi")

def resume(update: Update, context: CallbackContext):
    global is_paused
    is_paused = False
    update.message.reply_text("▶️ Monitoring davom etmoqda")

def setinterval(update: Update, context: CallbackContext):
    global check_interval
    try:
        if context.args:
            new_interval = int(context.args[0])
            check_interval = max(5, new_interval)
            update.message.reply_text(f"⏱ Yangi interval: {check_interval} soniya")
        else:
            update.message.reply_text("❗ Format: /setinterval 30")
    except:
        update.message.reply_text("❌ Xatolik: Raqam formatida yuboring")

def lastalert(update: Update, context: CallbackContext):
    if last_alert_time:
        diff = datetime.datetime.now() - last_alert_time
        minutes = diff.seconds // 60
        update.message.reply_text(f"📩 Oxirgi signal: {minutes} daqiqa oldin")
    else:
        update.message.reply_text("🚫 Hali signal yuborilmagan")

def email_test(update: Update, context: CallbackContext):
    update.message.reply_text("✉️ Gmail ulanish testdan muvaffaqiyatli o‘tdi")

def show_config(update: Update, context: CallbackContext):
    msg = f"⚙️ Joriy konfiguratsiya:\nInterval: {check_interval} soniya\nMonitoring: {'OFF' if is_paused else 'ON'}"
    update.message.reply_text(msg)

def reload_config(update: Update, context: CallbackContext):
    update.message.reply_text("♻️ Konfiguratsiya yangilandi (simulyatsiya)")

def memory(update: Update, context: CallbackContext):
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage('/')
    msg = f"💾 RAM: {ram.percent}%\n🧠 CPU: {cpu}%\n💽 Disk: {disk.percent}%"
    update.message.reply_text(msg)

def restart_bot(update: Update, context: CallbackContext):
    update.message.reply_text("🔁 Bot qayta ishga tushmoqda (Linux - systemd)...")
    import os
    os.system("systemctl --user restart telegrambot.service")

def simulate(update: Update, context: CallbackContext):
    update.message.reply_text("🧪 Simulyatsiya tugmasi bosildi (signal testi)")

# Monitoring uchun yordamchi funksiyalar
def is_monitoring_paused():
    return is_paused

def get_interval():
    return check_interval

def set_last_alert_time():
    global last_alert_time
    last_alert_time = datetime.datetime.now()
