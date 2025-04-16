import praw
from datetime import datetime

def get_reddit_headlines(ticker, client_id, client_secret, user_agent, max_count=30):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    query = f"{ticker} OR ${ticker}"
    headlines = []
    subreddits = ['stocks', 'wallstreetbets', 'investing']

    try:
        for sub in subreddits:
            for post in reddit.subreddit(sub).search(query, sort='new', time_filter='month', limit=max_count):
                if not post.stickied:
                    dt = datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M')
                    headlines.append((post.title.strip(), dt))
    except Exception as e:
        print(f"[Reddit] Xato: {e}")
        return []

    return headlines
