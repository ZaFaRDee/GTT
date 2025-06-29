import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


def get_put_call_volume(ticker: str):
    url = f"https://www.barchart.com/stocks/quotes/{ticker}/put-call-ratios"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(random.uniform(5, 7))

        rows = driver.find_elements(By.CSS_SELECTOR, "div.bc-futures-options-quotes-totals__data-row")

        put_volume = call_volume = put_call_ratio = None

        for row in rows:
            text = row.text.strip().lower()
            value_el = row.find_element(By.CSS_SELECTOR, "strong.right")
            value_raw = value_el.text.strip().replace(',', '')

            if "put volume total" in text:
                put_volume = int(value_raw)
            elif "call volume total" in text:
                call_volume = int(value_raw)
            elif "put/call ratio" in text:
                try:
                    put_call_ratio = float(value_raw)
                except ValueError:
                    continue

        if put_volume is not None and call_volume is not None:
            ratio = put_call_ratio if put_call_ratio is not None else round(put_volume / call_volume, 2)
            return {
                "Put Volume": put_volume,
                "Call Volume": call_volume,
                "Put/Call Ratio": ratio
            }
        else:
            return {
                "Put Volume": "?",
                "Call Volume": "?",
                "Put/Call Ratio": "?"
            }

    except Exception as e:
        return {
            "Put Volume": "?",
            "Call Volume": "?",
            "Put/Call Ratio": "?"
        }
    finally:
        driver.quit()

def screenshot_barchart_putcall(ticker: str) -> str | None:
    import os
    import time
    import random
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager

    url = f"https://www.barchart.com/stocks/quotes/{ticker}/put-call-ratios"
    screenshot_path = f"images/{ticker.upper()}_putcall.png"

    options = Options()
    # Barqaror va eng kam xatolik beradigan sozlamalar
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,3000")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--blink-settings=imagesEnabled=true")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

    try:
        print(f"[🔍] Sahifa ochilmoqda: {url}")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(90)
        driver.set_script_timeout(90)

        driver.get(url)

        # Insondek harakat — yuklash uchun kutish
        time.sleep(random.uniform(9, 12))
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        os.makedirs("images", exist_ok=True)

        # Reklama bannerlar yopilishi (agar mavjud bo‘lsa)
        try:
            banner = driver.find_element(By.CSS_SELECTOR, ".qc-cmp2-summary-buttons")
            btn = banner.find_element(By.CSS_SELECTOR, "button[mode='primary']")
            btn.click()
            time.sleep(1)
            print("[✖] Popup/banner'lar yopildi.")
        except:
            print("[ℹ️] Popup/banner topilmadi — davom etamiz.")

        # Jadvalni topib screenshot olish
        target = driver.find_element(By.CSS_SELECTOR, "div.one-column-block")
        target.screenshot(screenshot_path)

        print(f"[📸] Jadval saqlandi: {screenshot_path}")
        return screenshot_path

    except TimeoutException:
        print("❌ Timeout: Sahifa yuklanmadi.")
        return None

    except WebDriverException as e:
        print(f"❌ WebDriver xatolik: {e}")
        return None

    except Exception as e:
        print(f"❌ Screenshot xatoligi: {e}")
        return None

    finally:
        try:
            driver.quit()
        except:
            pass
