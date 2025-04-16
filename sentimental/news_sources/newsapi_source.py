import requests
from datetime import datetime

def get_newsapi_headlines(ticker, api_key, max_count=30):
    url = "https://newsapi.org/v2/everything"
    query = f'"{ticker}" OR "${ticker}"'

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_count,
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[NewsAPI] Xato: {e}")
        return []

    articles = response.json().get("articles", [])
    headlines = []

    for article in articles:
        title = article.get("title")
        published_at = article.get("publishedAt")
        if title and published_at:
            try:
                dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                time_str = dt.strftime("%Y-%m-%d %H:%M")
                headlines.append((title.strip(), time_str))
            except:
                continue

    return headlines