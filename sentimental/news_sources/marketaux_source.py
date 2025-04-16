import requests
from datetime import datetime

def get_marketaux_headlines(ticker, api_key, max_count=30):
    url = "https://api.marketaux.com/v1/news/all"

    params = {
        "symbols": ticker,
        "language": "en",
        "filter_entities": "true",
        "api_token": api_key,
        "limit": max_count
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[Marketaux] Xato: {e}")
        return []

    articles = response.json().get("data", [])
    headlines = []

    for article in articles:
        title = article.get("title")
        published = article.get("published_at")
        if title and published:
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                time_str = dt.strftime("%Y-%m-%d %H:%M")
                headlines.append((title.strip(), time_str))
            except:
                continue

    return headlines
