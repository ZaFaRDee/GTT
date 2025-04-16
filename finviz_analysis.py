# Yangi finviz_analysis.py – uch darajali baholash tizimiga moslashtirilgan versiya

import yfinance as yf
from finviz_wrapper import get_finviz_data
from sector_standards import SECTOR_STANDARDS

EVALUATED_KEYS = [
    "Income", "P/E", "P/B", "P/S", "EPS (ttm)",
    "Insider Own", "Inst Own", "Short Float", "ROA", "ROE"
]

DISPLAY_ONLY_KEYS = [
    "Market Cap", "Avg Volume", "Target Price", "Earnings"
]

ICON_MAP = {
    "Market Cap": "💰",
    "Avg Volume": "📊",
    "Target Price": "🎯",
    "Earnings": "📅",
}

GRADE_ICONS = {
    "good": "🟢",
    "average": "🟡",
    "bad": "🔴"
}

def get_sector(ticker):
    try:
        return yf.Ticker(ticker).info.get("sector", "Generic")
    except Exception:
        return "Generic"

def parse_finviz_value(value_str):
    try:
        if value_str.endswith("B"):
            return float(value_str[:-1]) * 1_000_000_000
        elif value_str.endswith("M"):
            return float(value_str[:-1]) * 1_000_000
        elif value_str.endswith("K"):
            return float(value_str[:-1]) * 1_000
        elif "%" in value_str:
            return float(value_str.replace("%", ""))
        else:
            return float(value_str)
    except:
        return None

def apply_suffix(key, value_str):
    if value_str == "?":
        return "?"
    if key in ["EPS (ttm)", "Income", "Market Cap", "Target Price"]:
        return f"${value_str}"
    if key in ["Insider Own", "Inst Own", "Short Float", "ROA", "ROE"]:
        return f"{value_str}%"
    return value_str

def evaluate_grade(metric, value, sector):
    standards = SECTOR_STANDARDS.get(sector, SECTOR_STANDARDS["Generic"])
    if metric not in standards or value is None:
        return "unknown"
    try:
        value = float(value)
    except:
        return "unknown"

    ranges = standards[metric]
    for grade, (min_val, max_val) in ranges.items():
        if min_val is None and max_val is not None and value < max_val:
            return grade
        elif min_val is not None and max_val is None and value >= min_val:
            return grade
        elif min_val is not None and max_val is not None and min_val <= value < max_val:
            return grade
    return "unknown"

def format_large_number(value):
    try:
        num = float(value)
        sign = "-" if num < 0 else ""
        abs_num = abs(num)
        if abs_num >= 1_000_000_000:
            return f"{sign}{abs_num / 1_000_000_000:.1f}B"
        elif abs_num >= 1_000_000:
            return f"{sign}{abs_num / 1_000_000:.1f}M"
        elif abs_num >= 1_000:
            return f"{sign}{abs_num / 1_000:.1f}k"
        else:
            return f"{sign}{abs_num:.2f}"
    except:
        return value

def get_finviz_fundamentals(ticker):
    data = get_finviz_data(ticker)
    if not data:
        return None, None, None, None

    sector = get_sector(ticker)
    evaluated = []
    display = []
    grade_counts = {"good": 0, "average": 0, "bad": 0}
    rsi_finviz = data.get("RSI (14)", "?")
    volume = data.get("Volume", "?")

    for key in EVALUATED_KEYS:
        raw = data.get(key, "?")
        value = parse_finviz_value(raw)
        grade = evaluate_grade(key, value, sector)
        icon = GRADE_ICONS.get(grade, "⚪")
        if grade in grade_counts:
            grade_counts[grade] += 1
        formatted_val = format_large_number(value) if value is not None else "?"
        formatted_val = apply_suffix(key, formatted_val)
        name = key.replace("Inst Own", "Institutional Own").replace("Insider Own", "Insider Ownership")
        evaluated.append(f"{icon} <b>{name}:</b> {formatted_val}")

    for key in DISPLAY_ONLY_KEYS:
        raw = data.get(key, "?")
        value = parse_finviz_value(raw)
        formatted = format_large_number(value) if value is not None else raw
        formatted = apply_suffix(key, formatted)
        name = key.replace("Inst Own", "Inst Own").replace("Insider Own", "Insider Ownership")
        icon = ICON_MAP.get(key, "")
        display.append(f"{icon} <b>{name}:</b> {formatted}")

    summary = f"📊 <b>Fundamental Score:</b> {grade_counts['good']} / {grade_counts['average'] + grade_counts['bad'] + grade_counts['good']}"
    return summary, evaluated, display, rsi_finviz, volume

