"""Small helpers for the fraud decision-tree lab."""
import numpy as np
import pandas as pd

from config import CATEGORICAL, DATA_PATH, FEATURES, TARGET, TRAIN_END_DAY, VALID_END_DAY


def gini(p):
    """Gini impurity of a node with fraud share p:  1 - p^2 - (1-p)^2"""
    p = np.asarray(p, dtype=float)
    return 1 - p**2 - (1 - p)**2


def entropy(p):
    """Entropy (bits) of a node with fraud share p. A pure node (p = 0 or 1) has entropy 0."""
    p = np.asarray(p, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return np.nan_to_num(h)


def split_gain(y, goes_left, criterion="gini"):
    """gain = impurity(parent) - weighted average impurity of the two children"""
    f = gini if criterion == "gini" else entropy
    y, goes_left = np.asarray(y), np.asarray(goes_left, dtype=bool)
    left, right = y[goes_left], y[~goes_left]
    children = len(left) / len(y) * f(left.mean()) + len(right) / len(y) * f(right.mean())
    return float(f(y.mean()) - children)


def load_data():
    if not DATA_PATH.exists():                      # first run: create the dataset
        from generate_data import generate
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        generate(60000).to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)


def make_X_y(df):
    X = pd.get_dummies(df[FEATURES + CATEGORICAL], columns=CATEGORICAL, dtype=int)
    return X, df[TARGET]


def time_split(df, X, y):
    """Train = days 0-59, validation = 60-74, test = 75-89."""
    tr = df.day < TRAIN_END_DAY
    va = (df.day >= TRAIN_END_DAY) & (df.day < VALID_END_DAY)
    te = df.day >= VALID_END_DAY
    return X[tr], y[tr], X[va], y[va], X[te], y[te]
