# parser.py

import re

pattern = r'Alert: New symbols?: (.+?) (?:was|were) added to (.+?)\.?$'

def parse_subject(subject):
    subject_cleaned = " ".join(subject.strip().split())
    match = re.search(pattern, subject_cleaned)
    if match:
        tickers_str = match.group(1).strip()
        algo_name = match.group(2).strip()
        tickers = [ticker.strip() for ticker in tickers_str.split(',')]
        return tickers, algo_name
    return None, None
