# utils.py

import yfinance as yf

def get_tradingview_symbol(ticker):
    try:
        info = yf.Ticker(ticker).info
        exchange = info.get('exchange', None)
        exchange_map = {
            'NMS': 'NASDAQ', 'NGM': 'NASDAQ', 'NYQ': 'NYSE',
            'ASE': 'AMEX', 'PCX': 'ARCA', 'BATS': 'BATS', 'OTC': 'OTC'
        }
        if exchange and exchange in exchange_map:
            return f"{exchange_map[exchange]}:{ticker}"
        return ticker
    except:
        return ticker
