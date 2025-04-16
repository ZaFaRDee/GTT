# Yagona sector_standards.py – barcha 11 sektor uchun 3-darajali baholash tizimi

SECTOR_STANDARDS = {
    "Technology": {
        "P/E": {"good": (None, 20), "average": (20, 35), "bad": (35, None)},
        "P/B": {"good": (None, 5), "average": (5, 10), "bad": (10, None)},
        "P/S": {"good": (None, 6), "average": (6, 12), "bad": (12, None)},
        "EPS (ttm)": {"good": (5, None), "average": (2, 5), "bad": (None, 2)},
        "Insider Own": {"good": (15, None), "average": (5, 15), "bad": (None, 5)},
        "Inst Own": {"good": (60, None), "average": (40, 60), "bad": (None, 40)},
        "Short Float": {"good": (None, 5), "average": (5, 15), "bad": (15, None)},
        "ROA": {"good": (12, None), "average": (8, 12), "bad": (None, 8)},
        "ROE": {"good": (20, None), "average": (15, 20), "bad": (None, 15)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Financial Services": {
        "P/E": {"good": (None, 12), "average": (12, 18), "bad": (18, None)},
        "P/B": {"good": (None, 1.2), "average": (1.2, 1.8), "bad": (1.8, None)},
        "P/S": {"good": (None, 3), "average": (3, 5), "bad": (5, None)},
        "EPS (ttm)": {"good": (4, None), "average": (2, 4), "bad": (None, 2)},
        "Insider Own": {"good": (8, None), "average": (3, 8), "bad": (None, 3)},
        "Inst Own": {"good": (65, None), "average": (45, 65), "bad": (None, 45)},
        "Short Float": {"good": (None, 3), "average": (3, 8), "bad": (8, None)},
        "ROA": {"good": (1.2, None), "average": (0.8, 1.2), "bad": (None, 0.8)},
        "ROE": {"good": (13, None), "average": (9, 13), "bad": (None, 9)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Healthcare": {
        "P/E": {"good": (None, 18), "average": (18, 25), "bad": (25, None)},
        "P/B": {"good": (None, 4), "average": (4, 6), "bad": (6, None)},
        "P/S": {"good": (None, 4), "average": (4, 6), "bad": (6, None)},
        "EPS (ttm)": {"good": (3, None), "average": (1.5, 3), "bad": (None, 1.5)},
        "Insider Own": {"good": (10, None), "average": (4, 10), "bad": (None, 4)},
        "Inst Own": {"good": (70, None), "average": (55, 70), "bad": (None, 55)},
        "Short Float": {"good": (None, 4), "average": (4, 10), "bad": (10, None)},
        "ROA": {"good": (10, None), "average": (6, 10), "bad": (None, 6)},
        "ROE": {"good": (18, None), "average": (12, 18), "bad": (None, 12)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Consumer Goods": {
        "P/E": {"good": (None, 22), "average": (22, 28), "bad": (28, None)},
        "P/B": {"good": (None, 8), "average": (8, 12), "bad": (12, None)},
        "P/S": {"good": (None, 3), "average": (3, 5), "bad": (5, None)},
        "EPS (ttm)": {"good": (4, None), "average": (2, 4), "bad": (None, 2)},
        "Insider Own": {"good": (5, None), "average": (2, 5), "bad": (None, 2)},
        "Inst Own": {"good": (65, None), "average": (50, 65), "bad": (None, 50)},
        "Short Float": {"good": (None, 3), "average": (3, 7), "bad": (7, None)},
        "ROA": {"good": (12, None), "average": (8, 12), "bad": (None, 8)},
        "ROE": {"good": (25, None), "average": (18, 25), "bad": (None, 18)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Energy": {
        "P/E": {"good": (None, 10), "average": (10, 15), "bad": (15, None)},
        "P/B": {"good": (None, 1.5), "average": (1.5, 2.5), "bad": (2.5, None)},
        "P/S": {"good": (None, 1.2), "average": (1.2, 2.0), "bad": (2.0, None)},
        "EPS (ttm)": {"good": (5, None), "average": (3, 5), "bad": (None, 3)},
        "Insider Own": {"good": (7, None), "average": (3, 7), "bad": (None, 3)},
        "Inst Own": {"good": (60, None), "average": (45, 60), "bad": (None, 45)},
        "Short Float": {"good": (None, 4), "average": (4, 9), "bad": (9, None)},
        "ROA": {"good": (8, None), "average": (5, 8), "bad": (None, 5)},
        "ROE": {"good": (15, None), "average": (10, 15), "bad": (None, 10)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Utilities": {
        "P/E": {"good": (None, 16), "average": (16, 22), "bad": (22, None)},
        "P/B": {"good": (None, 1.8), "average": (1.8, 2.5), "bad": (2.5, None)},
        "P/S": {"good": (None, 2.5), "average": (2.5, 3.5), "bad": (3.5, None)},
        "EPS (ttm)": {"good": (3, None), "average": (2, 3), "bad": (None, 2)},
        "Insider Own": {"good": (4, None), "average": (1, 4), "bad": (None, 1)},
        "Inst Own": {"good": (70, None), "average": (55, 70), "bad": (None, 55)},
        "Short Float": {"good": (None, 3), "average": (3, 6), "bad": (6, None)},
        "ROA": {"good": (4, None), "average": (3, 4), "bad": (None, 3)},
        "ROE": {"good": (10, None), "average": (7, 10), "bad": (None, 7)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Industrials": {
        "P/E": {"good": (None, 15), "average": (15, 22), "bad": (22, None)},
        "P/B": {"good": (None, 3), "average": (3, 5), "bad": (5, None)},
        "P/S": {"good": (None, 1.5), "average": (1.5, 2.5), "bad": (2.5, None)},
        "EPS (ttm)": {"good": (4, None), "average": (2, 4), "bad": (None, 2)},
        "Insider Own": {"good": (6, None), "average": (2, 6), "bad": (None, 2)},
        "Inst Own": {"good": (65, None), "average": (50, 65), "bad": (None, 50)},
        "Short Float": {"good": (None, 5), "average": (5, 10), "bad": (10, None)},
        "ROA": {"good": (8, None), "average": (5, 8), "bad": (None, 5)},
        "ROE": {"good": (18, None), "average": (12, 18), "bad": (None, 12)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Retail": {
        "P/E": {"good": (None, 18), "average": (18, 25), "bad": (25, None)},
        "P/B": {"good": (None, 5), "average": (5, 8), "bad": (8, None)},
        "P/S": {"good": (None, 0.8), "average": (0.8, 1.2), "bad": (1.2, None)},
        "EPS (ttm)": {"good": (6, None), "average": (4, 6), "bad": (None, 4)},
        "Insider Own": {"good": (10, None), "average": (5, 10), "bad": (None, 5)},
        "Inst Own": {"good": (70, None), "average": (55, 70), "bad": (None, 55)},
        "Short Float": {"good": (None, 4), "average": (4, 8), "bad": (8, None)},
        "ROA": {"good": (10, None), "average": (7, 10), "bad": (None, 7)},
        "ROE": {"good": (25, None), "average": (18, 25), "bad": (None, 18)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Materials": {
        "P/E": {"good": (None, 14), "average": (14, 20), "bad": (20, None)},
        "P/B": {"good": (None, 3), "average": (3, 5), "bad": (5, None)},
        "P/S": {"good": (None, 1.5), "average": (1.5, 2.5), "bad": (2.5, None)},
        "EPS (ttm)": {"good": (5, None), "average": (3, 5), "bad": (None, 3)},
        "Insider Own": {"good": (8, None), "average": (3, 8), "bad": (None, 3)},
        "Inst Own": {"good": (65, None), "average": (50, 65), "bad": (None, 50)},
        "Short Float": {"good": (None, 5), "average": (5, 10), "bad": (10, None)},
        "ROA": {"good": (9, None), "average": (6, 9), "bad": (None, 6)},
        "ROE": {"good": (20, None), "average": (15, 20), "bad": (None, 15)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Telecom": {
        "P/E": {"good": (None, 12), "average": (12, 18), "bad": (18, None)},
        "P/B": {"good": (None, 2), "average": (2, 3.5), "bad": (3.5, None)},
        "P/S": {"good": (None, 1.5), "average": (1.5, 2.5), "bad": (2.5, None)},
        "EPS (ttm)": {"good": (3, None), "average": (1.5, 3), "bad": (None, 1.5)},
        "Insider Own": {"good": (5, None), "average": (1, 5), "bad": (None, 1)},
        "Inst Own": {"good": (60, None), "average": (45, 60), "bad": (None, 45)},
        "Short Float": {"good": (None, 3), "average": (3, 7), "bad": (7, None)},
        "ROA": {"good": (6, None), "average": (4, 6), "bad": (None, 4)},
        "ROE": {"good": (15, None), "average": (10, 15), "bad": (None, 10)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Real Estate": {
        "P/E": {"good": (None, 15), "average": (15, 20), "bad": (20, None)},
        "P/B": {"good": (None, 1.8), "average": (1.8, 2.5), "bad": (2.5, None)},
        "P/S": {"good": (None, 8), "average": (8, 12), "bad": (12, None)},
        "EPS (ttm)": {"good": (4, None), "average": (2, 4), "bad": (None, 2)},
        "Insider Own": {"good": (10, None), "average": (5, 10), "bad": (None, 5)},
        "Inst Own": {"good": (75, None), "average": (60, 75), "bad": (None, 60)},
        "Short Float": {"good": (None, 6), "average": (6, 12), "bad": (12, None)},
        "ROA": {"good": (5, None), "average": (3, 5), "bad": (None, 3)},
        "ROE": {"good": (12, None), "average": (8, 12), "bad": (None, 8)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
    },
    "Generic": {
        "P/E": {"good": (None, 18), "average": (18, 25), "bad": (25, None)},
        "P/B": {"good": (None, 3), "average": (3, 6), "bad": (6, None)},
        "P/S": {"good": (None, 3), "average": (3, 6), "bad": (6, None)},
        "EPS (ttm)": {"good": (4, None), "average": (2, 4), "bad": (None, 2)},
        "Insider Own": {"good": (10, None), "average": (3, 10), "bad": (None, 3)},
        "Inst Own": {"good": (60, None), "average": (40, 60), "bad": (None, 40)},
        "Short Float": {"good": (None, 5), "average": (5, 10), "bad": (10, None)},
        "ROA": {"good": (10, None), "average": (6, 10), "bad": (None, 6)},
        "ROE": {"good": (18, None), "average": (12, 18), "bad": (None, 12)},
        "Income": {"good": (0.01, None), "average": (0,0.01), "bad": (None, 0)}
}
}
