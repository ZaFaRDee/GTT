# stock_analysis.py

import yfinance as yf

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1d')
    current_price = hist['Close'].iloc[-1]
    volume = hist['Volume'].iloc[-1] // 1000

    period = 14
    hist_rsi = stock.history(period='1mo')['Close']
    delta = hist_rsi.diff(1).dropna()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    current_rsi = round(rsi.iloc[-1], 2)

    return current_price, current_rsi, volume

def calculate_support_resistance_from_range(ticker):
    data = yf.download(ticker, period='1mo', interval='1d', progress=False, auto_adjust=True)
    data.dropna(inplace=True)
    if data.empty or len(data) < 5:
        raise ValueError(f"{ticker} uchun yetarli data topilmadi.")
    resistance = round(data['High'].max().item(), 2)
    support = round(data['Low'].min().item(), 2)
    return support, resistance
