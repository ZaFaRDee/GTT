import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_finviz_headlines(ticker, max_count=30):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Finviz] Xato: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find("table", class_="fullview-news-outer")
    headlines = []
    if not news_table:
        return []

    rows = news_table.find_all("tr")
    last_date = None

    for row in rows:
        if row.td and row.a:
            datetime_text = row.td.text.strip()
            headline = row.a.text.strip()

            if len(datetime_text.split()) == 2:
                last_date = datetime_text
            else:
                datetime_text = f"{last_date.split()[0]} {datetime_text}"

            try:
                dt = datetime.strptime(datetime_text, "%b-%d-%y %I:%M%p")
                formatted_time = dt.strftime('%Y-%m-%d %H:%M')
                headlines.append((headline, formatted_time))
            except:
                continue

            if len(headlines) >= max_count:
                break

    return headlines