# Gmail to Telegram Stock Alert Bot 📬 → 🤖

Bu loyiha ThinkOrSwim (TOS) orqali kelgan Gmail xabarlaridan stock signal (alert) larni avtomatik o‘qib,
ularni Telegram guruhiga yuboradigan Python dasturidir.

## 🧠 Asosiy funksiyalar

- Gmail'dan `alerts@thinkorswim.com` dan kelgan xabarlarni o‘qiydi
- Xabardagi ticker va algoritm nomini ajratib oladi
- `yfinance` orqali quyidagilarni oladi:
  - Narxi (Price)
  - RSI (14)
  - Hajm (Volume)
  - Support va Resistance zonalari
- Ma'lumotlarni Telegram bot orqali xabar shaklida yuboradi

---

## 🔐 Maxfiy ma'lumotlar

Loyihada `.env` fayl orqali quyidagi ma'lumotlar yashirin saqlanadi:

- Gmail logini va app parol
- Telegram bot tokeni va chat ID

**Iltimos! `.env` faylni GitHub’ga joylamang.**

`.env.example` fayli namunasi mavjud — uni to‘ldirib, `.env` nomi bilan nusxa oling:

```bash
cp .env.example .env
