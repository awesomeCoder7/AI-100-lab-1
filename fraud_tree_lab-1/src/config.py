"""Shared settings: paths, columns, time split, and business costs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
DATA_PATH = DATA_DIR / "transactions.csv"
SCOREBOARD_PATH = OUT_DIR / "scoreboard.csv"

RANDOM_SEED = 42

# Split by time: learn from the past, test on the "future".
TRAIN_END_DAY = 60      # days 0-59  -> train
VALID_END_DAY = 75      # days 60-74 -> validation (pick depth + threshold)
                        # days 75-89 -> test (touched once at the end)

FEATURES = [
    "amount",                   # payment amount in $
    "amount_vs_merchant_avg",   # amount / this shop type's typical ticket
    "country_mismatch",         # 1 if IP country != card country
    "n_countries_card_24h",     # countries this card was used in, last 24h
    "n_txn_card_24h",           # payments by this card, last 24h
    "n_cards_ip_24h",           # different cards seen from this IP, last 24h
    "card_age_days",            # days since the card was first seen
    "card_seen_before",         # 1 if the card was seen before
    "hour_of_day",
    "day_of_week",
    "issuer_risk_score",        # historical fraud rate of the card's bank
    "disposable_email",         # 1 if throw-away email domain
    "billing_zip_mismatch",     # 1 if billing ZIP doesn't match the card
]
CATEGORICAL = ["merchant_category", "card_country"]
TARGET = "is_fraud"

# Business costs (Stripe primer worked example)
MARGIN = 0.08            # profit margin on a good sale
CHARGEBACK_FEE = 15.0    # dispute fee on a missed fraud
AVG_SALE = 26.0
