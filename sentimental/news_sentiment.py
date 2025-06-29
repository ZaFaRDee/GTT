import asyncio
from sentimental.finbert_sentiment import analyze_with_finbert
from sentimental.news_sources.reddit_source import get_reddit_headlines
from sentimental.news_sources.finviz_source import get_finviz_headlines
from sentimental.news_sources.stocktwits_source import get_stocktwits_headlines
from sentimental.news_sources.marketaux_source import get_marketaux_headlines
from sentimental.news_sources.newsapi_source import get_newsapi_headlines
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, MARKETAUX_API_KEY, NEWSAPI_KEY

async def get_sentiment_summary(ticker):
    async def wrap(func, *args):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args)
            else:
                # run sync function in executor
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, func, *args)
        except Exception as e:
            print(f"[❌] {func.__name__} xatolik: {e}")
            return []

    tasks = [
        wrap(get_finviz_headlines, ticker),
        wrap(get_reddit_headlines, ticker, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT),
        wrap(get_stocktwits_headlines, ticker),
        wrap(get_marketaux_headlines, ticker, MARKETAUX_API_KEY),
        wrap(get_newsapi_headlines, ticker, NEWSAPI_KEY),
    ]

    results = await asyncio.gather(*tasks)
    source_names = ["Finviz.com", "Reddit.com", "Stocktwits.com", "Marketaux.com", "NewsAPI.com"]

    sources = []
    total_pos = 0
    total_neg = 0

    for i, headlines in enumerate(results):
        if not headlines:
            continue

        sentiments = []
        for title, _ in headlines:
            label, _ = analyze_with_finbert(title)
            sentiments.append(label)

        pos = sentiments.count("🟢 Positive")
        neu = sentiments.count("🟡 Neutral")
        neg = sentiments.count("🔴 Negative")

        overall = "Positive" if pos > neg else ("Negative" if neg > pos else "Neutral")
        sources.append((source_names[i], pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    if not sources:
        return "\U0001F4F0 Sentimental Analysis:\n\tMa'lumot topilmadi."

    total = total_pos + total_neg
    lines = [f"📰 <b>Sentimental Score:</b> {total_pos} / {total}\n"]
    for name, pos, neu, neg, overall in sources:
        name_aligned = name.ljust(16)  # ustunlarni to‘g‘rilash uchun
        lines.append(f"🌐 <b>{name_aligned}</b> → <b>{overall}</b>")
        lines.append(f"🟢 {str(pos).ljust(3)} 🟡 {str(neu).ljust(3)} 🔴 {str(neg).ljust(3)}\n")

    return "\n".join(lines)

