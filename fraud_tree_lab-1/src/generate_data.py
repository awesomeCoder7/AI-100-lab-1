"""
Generate a synthetic card-payments dataset inspired by the Stripe Radar primer.

Each row is one card payment with network-style features (card velocity,
countries seen in 24h, IP/card country mismatch, card history, ...) and a
binary label `is_fraud`.

Fraud is generated from four distinct "attack patterns" plus background noise,
so that some patterns are easy for hand-written rules and others are only
visible through feature *interactions* that a learned model can pick up:

  1. Stolen card, cross-border     -> big amount + IP/card country mismatch
  2. Card testing                  -> many tiny payments, high velocity
  3. Account takeover (ATO)        -> old card, new IP, unusual hour, high ticket
  4. Domestic fraud ring (drift!)  -> appears only in the last month: domestic
                                      IP, disposable email, many cards per IP.
                                      Rules written earlier will not know it.

Usage:
    python src/generate_data.py --n 60000
"""
import argparse

import numpy as np
import pandas as pd

from config import DATA_DIR, DATA_PATH, RANDOM_SEED

MERCHANT_CATEGORIES = {
    # category: (typical ticket $, base fraud multiplier)
    "digital_goods": (15, 2.0),
    "electronics": (180, 1.6),
    "fashion": (60, 1.0),
    "travel": (320, 1.3),
    "food_delivery": (25, 0.6),
    "saas": (40, 0.8),
}
COUNTRIES = ["US", "GB", "DE", "FR", "CA", "BR", "IN", "NG", "RU", "CN"]
COUNTRY_P = [0.45, 0.10, 0.08, 0.07, 0.07, 0.06, 0.06, 0.03, 0.04, 0.04]
HIGH_RISK_ISSUER_COUNTRIES = {"NG", "RU", "BR"}


def _legit(n, rng, day):
    cat = rng.choice(list(MERCHANT_CATEGORIES), n, p=[.15, .15, .2, .1, .25, .15])
    avg = np.array([MERCHANT_CATEGORIES[c][0] for c in cat])
    card_country = rng.choice(COUNTRIES, n, p=COUNTRY_P)
    travelling = rng.random(n) < 0.06          # legit travellers cause mismatches
    ip_country = np.where(travelling, rng.choice(COUNTRIES, n, p=COUNTRY_P), card_country)
    return pd.DataFrame({
        "day": day,
        "merchant_category": cat,
        "amount": np.round(avg * rng.lognormal(0, 0.6, n), 2),
        "card_country": card_country,
        "ip_country": ip_country,
        "n_countries_card_24h": np.where(travelling, rng.choice([1, 2, 3], n, p=[.55, .38, .07]), 1),
        "n_txn_card_24h": rng.poisson(1.2, n) + 1,
        # shared IPs (office / campus NAT) legitimately see many cards
        "n_cards_ip_24h": np.where(rng.random(n) < 0.015, rng.integers(4, 25, n), rng.choice([1, 1, 1, 2, 3], n)),
        "card_age_days": rng.exponential(500, n).astype(int),
        "card_seen_before": (rng.random(n) < 0.92).astype(int),   # ~90% of cards seen before
        "hour_of_day": np.clip(rng.normal(14, 4.5, n), 0, 23).astype(int),
        "disposable_email": (rng.random(n) < 0.03).astype(int),
        "billing_zip_mismatch": (rng.random(n) < 0.04).astype(int),
        "pattern": "legit",
        "is_fraud": 0,
    })


def _fraud(n, rng, day, pattern):
    cat_names = list(MERCHANT_CATEGORIES)
    w = np.array([MERCHANT_CATEGORIES[c][1] for c in cat_names]); w /= w.sum()
    cat = rng.choice(cat_names, n, p=w)
    avg = np.array([MERCHANT_CATEGORIES[c][0] for c in cat])
    risky = ["NG", "RU", "BR", "CN", "IN"]
    card_country = rng.choice(COUNTRIES, n, p=COUNTRY_P)
    df = pd.DataFrame({
        "day": day, "merchant_category": cat, "card_country": card_country,
        "ip_country": card_country,
        "amount": np.round(avg * rng.lognormal(0.3, 0.7, n), 2),
        "n_countries_card_24h": 1,
        "n_txn_card_24h": rng.poisson(2, n) + 1,
        "n_cards_ip_24h": rng.choice([1, 2, 3], n),
        "card_age_days": rng.exponential(200, n).astype(int),
        "card_seen_before": (rng.random(n) < 0.6).astype(int),
        "hour_of_day": rng.integers(0, 24, n),
        "disposable_email": (rng.random(n) < 0.15).astype(int),
        "billing_zip_mismatch": (rng.random(n) < 0.3).astype(int),
        "pattern": pattern, "is_fraud": 1,
    })
    if pattern == "stolen_cross_border":
        df["ip_country"] = rng.choice(risky, n)
        df["n_countries_card_24h"] = rng.choice([2, 3, 4, 5], n)
        df["amount"] = np.round(avg * rng.lognormal(1.2, 0.6, n), 2)
    elif pattern == "card_testing":
        df["amount"] = np.round(rng.uniform(0.5, 4.0, n), 2)
        df["n_txn_card_24h"] = rng.integers(4, 30, n)
        df["n_cards_ip_24h"] = rng.integers(3, 40, n)
        df["card_seen_before"] = 0
        df["card_age_days"] = rng.integers(0, 3, n)
    elif pattern == "account_takeover":
        df["card_age_days"] = rng.integers(400, 2500, n)
        df["card_seen_before"] = 1
        df["hour_of_day"] = rng.choice([0, 1, 2, 3, 4, 5], n)
        df["billing_zip_mismatch"] = (rng.random(n) < 0.7).astype(int)
        df["amount"] = np.round(avg * rng.lognormal(0.9, 0.5, n), 2)
        # half from a foreign IP, half domestic via proxy
        foreign = rng.random(n) < 0.5
        df.loc[foreign, "ip_country"] = rng.choice(COUNTRIES, foreign.sum())
    elif pattern == "domestic_ring":
        df["card_country"] = "US"; df["ip_country"] = "US"
        df["disposable_email"] = (rng.random(n) < 0.85).astype(int)
        df["n_cards_ip_24h"] = rng.integers(4, 15, n)
        df["amount"] = np.round(avg * rng.lognormal(0.4, 0.4, n), 2)
    return df


def generate(n_total=60000, n_days=90, fraud_rate=0.025, seed=RANDOM_SEED):
    rng = np.random.default_rng(seed)
    frames = []
    per_day = n_total // n_days
    for day in range(n_days):
        n_fraud = rng.binomial(per_day, fraud_rate)
        frames.append(_legit(per_day - n_fraud, rng, day))
        if day >= 70:   # concept drift: a new domestic fraud ring appears
            mix = {"stolen_cross_border": .25, "card_testing": .2,
                   "account_takeover": .2, "domestic_ring": .35}
        else:
            mix = {"stolen_cross_border": .4, "card_testing": .3,
                   "account_takeover": .3, "domestic_ring": 0.0}
        counts = rng.multinomial(n_fraud, list(mix.values()))
        for (pat, _), k in zip(mix.items(), counts):
            if k:
                frames.append(_fraud(k, rng, day, pat))
    df = pd.concat(frames, ignore_index=True)

    # derived features
    df["country_mismatch"] = (df["card_country"] != df["ip_country"]).astype(int)
    cat_avg = df["merchant_category"].map({k: v[0] for k, v in MERCHANT_CATEGORIES.items()})
    df["amount_vs_merchant_avg"] = (df["amount"] / cat_avg).round(3)
    base_issuer = df["card_country"].isin(HIGH_RISK_ISSUER_COUNTRIES).astype(float) * 0.04 + 0.01
    df["issuer_risk_score"] = np.clip(base_issuer + rng.normal(0, 0.01, len(df)) + df["is_fraud"] * rng.normal(0.01, 0.01, len(df)), 0, 1).round(4)
    df["day_of_week"] = df["day"] % 7
    df["merchant_id"] = df["merchant_category"] + "_" + rng.integers(1, 5, len(df)).astype(str)
    df["timestamp"] = pd.Timestamp("2026-01-01") + pd.to_timedelta(df["day"], "D") + pd.to_timedelta(df["hour_of_day"], "h") + pd.to_timedelta(rng.integers(0, 3600, len(df)), "s")

    # ~0.2% label noise: chargebacks that never get filed / friendly fraud
    flip = rng.random(len(df)) < 0.002
    df.loc[flip, "is_fraud"] = 1 - df.loc[flip, "is_fraud"]

    df = df.sort_values("timestamp").reset_index(drop=True)
    df.insert(0, "txn_id", [f"txn_{i:06d}" for i in range(len(df))])
    cols = ["txn_id", "timestamp", "day", "merchant_id", "merchant_category", "amount",
            "card_country", "ip_country", "country_mismatch", "n_countries_card_24h",
            "n_txn_card_24h", "n_cards_ip_24h", "card_age_days", "card_seen_before",
            "hour_of_day", "day_of_week", "issuer_risk_score", "amount_vs_merchant_avg",
            "disposable_email", "billing_zip_mismatch", "pattern", "is_fraud"]
    return df[cols]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60000)
    ap.add_argument("--fraud-rate", type=float, default=0.025)
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = generate(args.n, fraud_rate=args.fraud_rate)
    df.to_csv(DATA_PATH, index=False)
    print(f"Wrote {len(df):,} rows to {DATA_PATH}")
    print(f"Fraud rate: {df.is_fraud.mean():.3%}")
    print(df.groupby("pattern").size().rename("rows").to_string())
