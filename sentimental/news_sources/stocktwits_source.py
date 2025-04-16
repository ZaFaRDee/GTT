import requests
from datetime import datetime

def get_stocktwits_headlines(ticker, max_count=30):
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"
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
        print(f"[Stocktwits] Xato: {e}")
        return []

    data = response.json().get("messages", [])
    headlines = []

    for msg in data[:max_count]:
        body = msg.get("body")
        created_at = msg.get("created_at")
        if body and created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                time_str = dt.strftime("%Y-%m-%d %H:%M")
                headlines.append((body.strip(), time_str))
            except:
                continue

    return headlines
