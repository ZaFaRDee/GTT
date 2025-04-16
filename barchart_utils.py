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
