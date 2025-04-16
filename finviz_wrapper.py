# finviz_wrapper.py

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

FINVIZ_URL_TEMPLATE = "https://finviz.com/quote.ashx?t={ticker}"


def get_finviz_data(ticker):
    """
    Ticker uchun Finviz sahifasidan barcha ko‘rsatkichlarni dict ko‘rinishida qaytaradi.
    """
    url = FINVIZ_URL_TEMPLATE.format(ticker=ticker.upper())
    data = {}

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[X] Finviz sahifasi yuklanmadi ({ticker}): {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="snapshot-table2")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            for i in range(0, len(cells) - 1, 2):
                key = cells[i].text.strip()
                val = cells[i + 1].text.strip()
                data[key] = val

    return data