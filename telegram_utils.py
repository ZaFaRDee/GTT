# telegram_utils.py

import asyncio
import os
import yfinance as yf
import datetime
from telegram import Bot
from stock_analysis import get_stock_info, calculate_support_resistance_from_range
from chart_utils import tradingview_chart_only_screenshot
from utils import get_tradingview_symbol
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from finviz_analysis import get_finviz_fundamentals
from barchart_utils import get_put_call_volume
from sentimental.news_sentiment import get_sentiment_summary
from barchart_utils import screenshot_barchart_putcall
from deep_translator import GoogleTranslator
import time


async def send_alerts_to_telegram(alerts):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    start_all = time.time()

    for alert in alerts:
        algo_name = alert['algo']

        for ticker in alert['tickers']:
            image_path = None
            now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')
            tv_symbol = get_tradingview_symbol(ticker)

            try:
                # Asosiy ma'lumotlar yfinance
                print(f"[⏱] 📊 get_stock_info: {time.time() - start_all:.2f}s")
                t1 = time.time()
                price, rsi, yf_volume = get_stock_info(ticker)
                print(f"[⏱] 🔼 calc_support_resistance: {time.time() - t1:.2f}s")
                t2 = time.time()
                support, resistance = calculate_support_resistance_from_range(ticker)
                print(f"[⏱] 🖼️ chart_screenshot: {time.time() - t2:.2f}s")
                t3 = time.time()
                image_path = tradingview_chart_only_screenshot(ticker)

                # Fundamental tahlil (Finviz orqali)

                print(f"[⏱] 🧾 fundamental_analysis: {time.time() - t3:.2f}s")
                t4 = time.time()
                summary, evaluated_lines, display_lines, rsi_finviz, volume = get_finviz_fundamentals(ticker)

                # Put va Call Volume (Barchart orqali)
                print(f"[⏱] 📉 barchart_volume: {time.time() - t4:.2f}s")
                t5 = time.time()
                volume_data = get_put_call_volume(ticker)
                call_vol = volume_data.get("Call Volume", "?")
                put_vol = volume_data.get("Put Volume", "?")

                if call_vol != "?":
                    call_vol = f"{int(call_vol):,}"
                if put_vol != "?":
                    put_vol = f"{int(put_vol):,}"

                # Sentimental Analysis
                print(f"[⏱] 🤖 sentiment_analysis: {time.time() - t5:.2f}s")
                t6 = time.time()
                sentiment_block = await get_sentiment_summary(ticker)

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
                print(f"[⏱] ✉️ send_photo: {time.time() - t6:.2f}s")
                t7 = time.time()
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=fallback_message, parse_mode='HTML')

            finally:
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
                print(f"[✅] Umumiy vaqt: {time.time() - start_all:.2f}s")

async def send_stock_info_to_user(ticker: str, chat_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    start_all = time.time()

    tv_symbol = get_tradingview_symbol(ticker)
    image_path = None
    now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')

    try:
        # Ma'lumotlarni olish
        price, rsi, yf_volume = get_stock_info(ticker)
        support, resistance = calculate_support_resistance_from_range(ticker)
        image_path = tradingview_chart_only_screenshot(ticker)

        summary, evaluated_lines, display_lines, rsi_finviz, volume = get_finviz_fundamentals(ticker)
        volume_data = get_put_call_volume(ticker)
        call_vol = volume_data.get("Call Volume", "?")
        put_vol = volume_data.get("Put Volume", "?")

        if call_vol != "?":
            call_vol = f"{int(call_vol):,}"
        if put_vol != "?":
            put_vol = f"{int(put_vol):,}"

        sentiment_block = await get_sentiment_summary(ticker)  # asinxron chaqiriq

        caption = (
            f"💹 <b>Ticker:</b> #{ticker}\n"
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
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='HTML',
                    timeout=120
                )
        else:
            raise Exception("Grafik yuklanmadi")

    except Exception as e:
        fallback_message = (
            f"❌ {ticker} ma'lumotlarni olishda xatolik yuz berdi: {str(e)}"
        )
        await bot.send_message(chat_id=chat_id, text=fallback_message)

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

async def send_fundamental_info_to_user(ticker: str, chat_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')
    image_path = None

    try:
        price, rsi, yf_volume = get_stock_info(ticker)
        support, resistance = calculate_support_resistance_from_range(ticker)
        image_path = tradingview_chart_only_screenshot(ticker)

        summary, evaluated_lines, display_lines, rsi_finviz, volume = get_finviz_fundamentals(ticker)

        tv_symbol = get_tradingview_symbol(ticker)

        caption = (
            f"💹 <b>Ticker:</b> #{ticker}\n"
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
            f"--------------------------------\n"
            f"{summary}\n"
            f"{chr(10).join(evaluated_lines)}\n\n"
            f"🕒 <b>Time:</b> {now}\n\n"
            f"<a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
        )

        if image_path:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='HTML'
                )
        else:
            await bot.send_message(chat_id=chat_id, text=caption, parse_mode='HTML')

    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"❌ Xatolik: {str(e)}")

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

async def send_sentimental_info_to_user(ticker: str, chat_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')
    image_path = None

    try:
        price, rsi, yf_volume = get_stock_info(ticker)
        support, resistance = calculate_support_resistance_from_range(ticker)
        image_path = tradingview_chart_only_screenshot(ticker)
        sentiment_block = await get_sentiment_summary(ticker)

        tv_symbol = get_tradingview_symbol(ticker)

        caption = (
            f"💹 <b>Ticker:</b> #{ticker}\n"
            f"--------------------------------\n"
            f"{sentiment_block}\n\n"
            f"🕒 <b>Time:</b> {now}\n\n"
            f"<a href='https://www.tradingview.com/chart/?symbol={tv_symbol}'>TradingView</a>"
        )

        if image_path:
            with open(image_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode='HTML'
                )
        else:
            await bot.send_message(chat_id=chat_id, text=caption, parse_mode='HTML')

    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"❌ Xatolik: {str(e)}")

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

async def send_barchart_options_screenshot_to_user(ticker: str, chat_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    now = datetime.datetime.now().strftime('%H:%M, %d.%m.%Y')

    try:
        image_path = screenshot_barchart_putcall(ticker)

        if image_path:
            caption = (
                f"📊 <b>#{ticker.upper()} Put/Call Options Analysis</b>\n\n"
                f"The chart and table are taken from Barchart.com\n\n"
                f"🕒 <b>Time:</b> {now}\n\n"
                f"<a href='https://www.barchart.com/stocks/quotes/{ticker}/put-call-ratios'>View details</a>"
            )
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, parse_mode='HTML')
        else:
            bot.send_message(chat_id=chat_id, text="❌ Jadvalni yuklab bo‘lmadi.")

    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ Xatolik yuz berdi: {str(e)}")

    finally:
        # Faylni o‘chirish
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

import json

def send_halal_info_to_user(ticker: str, chat_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        info = stock.info

        # ✅ Faqat halol tickerlar ro'yxatini yuklaymiz
        try:
            with open("halal_tickers.json", "r", encoding="utf-8") as f:
                halal_tickers = json.load(f)
        except Exception as e:
            halal_tickers = []

        is_halal = ticker in halal_tickers
        halal_status = "🟢 Halol" if is_halal else "🔴 Halol emas"

        # 📊 Ma'lumotlar
        price = info.get("currentPrice") or info.get("regularMarketPrice", "?")
        sector = info.get("sector", "Nomaʼlum")
        volume = info.get("volume", "?")
        # description = info.get("longBusinessSummary", "Maʼlumot topilmadi.")[:500] + "..."
        uzbek_summary = GoogleTranslator(source='en', target='uz').translate(info.get("longBusinessSummary", ""))[:500] + "..."

        # 📤 Format
        caption = (
            f"📌 Aksiya haqida umumiy ma'lumot:\n\n"
            f"💹 Ticker: <b>{ticker}</b>\n"
            f"🗄 Sektor: {sector}\n"
            f"💵 Narx: ${price}\n"
            f"📊 Volume: {volume:,}\n\n"
            f"🧮 Halollik tekshiruvi: {halal_status}\n\n"
            f"📝 Faoliyat: {uzbek_summary}\n\n"
            f"❗️ Eslatma: Halollik maʼlumotlari faqat oldindan tasdiqlangan ro'yxatga asoslangan. Savdoga kirishdan oldin ishonchli manbalardan tekshirishingiz tavsiya etiladi."
        )

        bot.send_message(chat_id=chat_id, text=caption, parse_mode="HTML")

    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ Xatolik: {str(e)}")
