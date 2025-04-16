# chart_utils.py

import os
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import get_tradingview_symbol


def dismiss_popups(driver):
    """Sahifadagi reklama/popup'larni avtomatik yopish"""
    try:
        # Modal (dialog) oynalar
        dialogs = driver.find_elements(By.CLASS_NAME, "tv-dialog__close")
        if dialogs:
            dialogs[0].click()
            time.sleep(1)

        # Bannerlarni yopish
        banners = driver.find_elements(By.CLASS_NAME, "tv-banner__close")
        if banners:
            banners[0].click()
            time.sleep(1)

        # Umumiy dialoglar (upgrade, pro)
        close_buttons = driver.find_elements(By.CSS_SELECTOR, "div[role='dialog'] button[aria-label='Close']")
        if close_buttons:
            close_buttons[0].click()
            time.sleep(1)

        print("[✖] Popup/banner'lar yopildi.")
    except Exception as e:
        print(f"[!] Popup yopishda xatolik: {e}")


def tradingview_chart_only_screenshot(ticker):
    """TradingView sahifasidan faqat candlestick grafikni screenshot qilib saqlaydi"""
    try:
        tv_symbol = get_tradingview_symbol(ticker)
        url = f"https://www.tradingview.com/chart/?symbol={tv_symbol}"
        print(f"[🔍] Sahifa ochilmoqda: {url}")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1280,800')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Bannerlarni yopish
        time.sleep(5)
        dismiss_popups(driver)

        # Grafik div yuklanishini kutamiz
        chart_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'chart-container-border'))
        )

        # Screenshot + crop
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        x = int(chart_element.location['x'])
        y = int(chart_element.location['y'])
        w = int(chart_element.size['width'])
        h = int(chart_element.size['height'])

        cropped = image.crop((x, y, x + w, y + h))

        # Faylni images papkaga saqlaymiz
        image_dir = "images"
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, f"{ticker}_chart.png")
        cropped.save(image_path)

        print(f"[✓] Grafik saqlandi: {image_path}")
        return image_path

    except TimeoutException:
        print(f"[X] {ticker} grafik topilmadi (timeout).")
        return None

    except Exception as e:
        print(f"[X] {ticker} grafik olishda xatolik: {e}")
        return None

    finally:
        try:
            driver.quit()
        except:
            pass
