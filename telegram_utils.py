# telegram_utils.py

import os
import datetime
from telegram import Bot
from stock_analysis import get_stock_info, calculate_support_resistance_from_range
from chart_utils import tradingview_chart_only_screenshot
from utils import get_tradingview_symbol
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from finviz_analysis import get_finviz_fundamentals
from barchart_utils import get_put_call_volume
from sentimental.news_sentiment import get_sentiment_summary


def send_alerts_to_telegram(alerts):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    for alert in alerts:
        algo_name = alert['algo']

        for ticker in alert['tickers']:
            image_path = None
            now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')
            tv_symbol = get_tradingview_symbol(ticker)

            try:
                # Asosiy ma'lumotlar yfinance
                price, rsi, yf_volume = get_stock_info(ticker)
                support, resistance = calculate_support_resistance_from_range(ticker)
                image_path = tradingview_chart_only_screenshot(ticker)

                # Fundamental tahlil (Finviz orqali)
                summary, evaluated_lines, display_lines, rsi_finviz, volume = get_finviz_fundamentals(ticker)

                # Put va Call Volume (Barchart orqali)
                volume_data = get_put_call_volume(ticker)
                call_vol = volume_data.get("Call Volume", "?")
                put_vol = volume_data.get("Put Volume", "?")

                if call_vol != "?":
                    call_vol = f"{int(call_vol):,}"
                if put_vol != "?":
                    put_vol = f"{int(put_vol):,}"

                # Sentimental Analysis
                sentiment_block = get_sentiment_summary(ticker)

                caption = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> {algo_name}\n"
                    f"--------------------------------\n"
                    f"📈 <b>RSI (14):</b> {rsi_finviz}\n"
                    f"📊 <b>Volume:</b> {yf_volume}k\n"
                    f"--------------------------------\n"
                    f"🔽 <b>Resistance Zone:</b> ${resistance}\n"
                    f"💵 <b>Price:</b> ${price:.2f}\n"
                    f"🔼 <b>Support Zone:</b> ${support}\n"
                    f"--------------------------------\n"
                    f"📊 <b>Fundamental Info:</b>\n"
                    f"{chr(10).join(display_lines)}\n"
                    f"📉 <b>Put Volume:</b> {put_vol}\n"
                    f"📈 <b>Call Volume:</b> {call_vol}\n"
                    f"--------------------------------\n"
                    f"{summary}\n"
                    f"{chr(10).join(evaluated_lines)}\n"
                    f"--------------------------------\n"
                    f"{sentiment_block}\n\n"
                    f"🕒 <b>Time:</b> {now}\n\n"
                    f"<a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
                )

                if image_path:
                    with open(image_path, 'rb') as photo:
                        bot.send_photo(
                            chat_id=TELEGRAM_CHAT_ID,
                            photo=photo,
                            caption=caption,
                            parse_mode='HTML',
                            timeout=120
                        )
                else:
                    raise Exception("Grafik yuklanmadi")

                print(f"✅ {ticker} haqida grafik bilan xabar yuborildi.")

            except Exception as e:
                print(f"❌ {ticker} xabar yuborishda xato: {e}")

                # Fallback qiymatlar
                try:
                    price_display = f"${float(price):.2f}"
                except:
                    price_display = "?"

                rsi_display = rsi if 'rsi' in locals() else "?"
                vol_display = f"{volume}k" if 'volume' in locals() else "?"
                support_display = support if 'support' in locals() else "?"
                resist_display = resistance if 'resistance' in locals() else "?"

                fallback_message = (
                    f"💹 <b>Ticker:</b> #{ticker}\n"
                    f"🧠 <b>Algorithm:</b> {algo_name}\n"
                    f"--------------------------------\n"
                    f"📈 <b>RSI (14):</b> {rsi_finviz}\n"
                    f"📊 <b>Volume:</b> {volume}k\n"
                    f"--------------------------------\n"
                    f"🔽 <b>Resistance Zone:</b> ${resistance}\n"
                    f"💵 <b>Price:</b> ${price:.2f}\n"
                    f"🔼 <b>Support Zone:</b> ${support}\n"
                    f"--------------------------------\n"
                    f"📊 <b>Fundamental Info:</b>\n"
                    f"{chr(10).join(display_lines)}\n"
                    f"--------------------------------\n"
                    f"{summary}\n"
                    f"{chr(10).join(evaluated_lines)}\n\n"
                    f"🕒 <b>Time:</b> {now}\n\n"
                    f"⚠️ Grafik topilmadi: <a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
                )

                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=fallback_message, parse_mode='HTML')

            finally:
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
