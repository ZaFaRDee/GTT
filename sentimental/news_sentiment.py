from sentimental.finbert_sentiment import analyze_with_finbert
from sentimental.news_sources.reddit_source import get_reddit_headlines
from sentimental.news_sources.finviz_source import get_finviz_headlines
from sentimental.news_sources.stocktwits_source import get_stocktwits_headlines
from sentimental.news_sources.marketaux_source import get_marketaux_headlines
from sentimental.news_sources.newsapi_source import get_newsapi_headlines
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, MARKETAUX_API_KEY, NEWSAPI_KEY

def analyze_and_summarize_source(name, headlines):
    sentiments = []
    for title, _ in headlines:
        label, _ = analyze_with_finbert(title)
        sentiments.append(label)

    pos = sentiments.count("🟢 Positive")
    neu = sentiments.count("🟡 Neutral")
    neg = sentiments.count("🔴 Negative")

    overall = "Positive" if pos > neg else ("Negative" if neg > pos else "Neutral")
    return name, pos, neu, neg, overall

def get_sentiment_summary(ticker):
    sources = []
    total_pos = 0
    total_neg = 0

    # Finviz
    finviz_headlines = get_finviz_headlines(ticker)
    if finviz_headlines:
        name, pos, neu, neg, overall = analyze_and_summarize_source("Finviz.com", finviz_headlines)
        sources.append((name, pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    # Reddit
    reddit_headlines = get_reddit_headlines(ticker, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
    if reddit_headlines:
        name, pos, neu, neg, overall = analyze_and_summarize_source("Reddit.com", reddit_headlines)
        sources.append((name, pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    # Stocktwits
    stocktwits_headlines = get_stocktwits_headlines(ticker)
    if stocktwits_headlines:
        name, pos, neu, neg, overall = analyze_and_summarize_source("Stocktwits.com", stocktwits_headlines)
        sources.append((name, pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    # Marketaux
    marketaux_headlines = get_marketaux_headlines(ticker, MARKETAUX_API_KEY)
    if marketaux_headlines:
        name, pos, neu, neg, overall = analyze_and_summarize_source("Marketaux.com", marketaux_headlines)
        sources.append((name, pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    # NewsAPI
    newsapi_headlines = get_newsapi_headlines(ticker, NEWSAPI_KEY)
    if newsapi_headlines:
        name, pos, neu, neg, overall = analyze_and_summarize_source("NewsAPI.com", newsapi_headlines)
        sources.append((name, pos, neu, neg, overall))
        total_pos += pos
        total_neg += neg

    if not sources:
        return "\U0001F4F0 Sentimental Analysis:\n\tMa'lumot topilmadi."

    lines = [f"\U0001F4F0 <b>Sentimental Score: {total_pos} / {total_pos + total_neg}</b>"]
    for name, pos, neu, neg, overall in sources:
        name_padded = name.ljust(12)
        lines.append(f"\U0001F310 <b>{name_padded}</b> → <b>{overall}</b>")
        lines.append(f"🟢 {str(pos).ljust(3)} 🟡 {str(neu).ljust(3)} 🔴 {str(neg).ljust(3)}")

    return "\n".join(lines)
