"""
make_data.py - create a SYNTHETIC (fake) dataset.
"""
from pathlib import Path

import numpy as np
import pandas as pd

N_STUDENTS = 400
N_HOMEWORK = 6
SEED = 100


def make_students(n=N_STUDENTS, seed=SEED):
    rng = np.random.default_rng(seed)

    # A hidden "effort" level drives most habits, so features are correlated
    # with each other, just like in real classes.
    effort = rng.normal(0, 1, n)

    # ---- attendance (true values, 0-1) ----------------------------------
    att_mid = np.clip(0.80 + 0.10 * effort + rng.normal(0, 0.08, n), 0.2, 1.0)
    # attendance tends to drop after the midterm
    att_final = np.clip(att_mid - 0.07 + 0.06 * effort + rng.normal(0, 0.10, n), 0.05, 1.0)

    # ---- exercise habit ---------------------------------------------------
    exercises = (rng.random(n) < 1 / (1 + np.exp(-(0.3 + 0.5 * effort)))).astype(int)

    # ---- homework ---------------------------------------------------------
    hw_scores = np.full((n, N_HOMEWORK), np.nan)
    hw_status = np.empty((n, N_HOMEWORK), dtype=object)
    p_submit = 1 / (1 + np.exp(-(2.2 + 1.0 * effort)))
    p_on_time = 1 / (1 + np.exp(-(1.0 + 0.9 * effort)))
    for j in range(N_HOMEWORK):
        submitted = rng.random(n) < p_submit
        on_time = rng.random(n) < p_on_time
        score = np.clip(np.round(7.2 + 1.1 * effort + rng.normal(0, 1.2, n), 1), 0, 10)
        score = np.where(on_time, score, np.maximum(score - 1.0, 0))  # late penalty
        hw_scores[submitted, j] = score[submitted]
        hw_status[:, j] = np.where(~submitted, "missing", np.where(on_time, "on time", "late"))

    # ---- true final score --------------------------------------------------
    hw_avg_true = np.nan_to_num(hw_scores, nan=0.0).mean(axis=1)
    on_time_rate_true = (hw_status == "on time").mean(axis=1)
    final_score = (
        18
        + 3.2 * hw_avg_true
        + 10 * on_time_rate_true
        + 22 * att_mid
        + 16 * att_final
        + 4 * exercises
        + rng.normal(0, 6, n)
    )
    final_score = np.clip(np.round(final_score, 1), 0, 100)

    # ---- build the table students will see ---------------------------------
    df = pd.DataFrame({"student_id": [f"S{1000 + i}" for i in range(n)]})
    df["section"] = rng.choice(["A", "B", "C"], n)
    for j in range(N_HOMEWORK):
        df[f"hw{j + 1}_score"] = hw_scores[:, j]
        df[f"hw{j + 1}_status"] = hw_status[:, j]
    df["midterm_attendance"] = att_mid
    df["final_attendance"] = att_final
    df["exercises"] = np.where(exercises == 1, "Yes", "No")
    df["seat_row"] = rng.integers(1, 13, n)  # noise: unrelated to score
    df["final_score"] = final_score
    # LEAKY column: computed FROM the final score -> must be dropped
    df["letter_grade"] = pd.cut(
        final_score, [-1, 59.99, 69.99, 79.99, 89.99, 101], labels=["F", "D", "C", "B", "A"]
    ).astype(str)

    df = _make_messy(df, rng)
    return df


def _make_messy(df, rng):
    """Add the kinds of problems real exported spreadsheets have."""
    df = df.copy()
    n = len(df)

    # 1. inconsistent text in section and homework status
    df["section"] = [rng.choice([s, s.lower(), f"Sec {s}", f" {s} "]) for s in df["section"]]
    status_variants = {
        "on time": ["on time", "On time", "on-time", "ON TIME"],
        "late": ["late", "Late", "LATE", "late "],
        "missing": ["missing", "Missing", "not submitted", ""],
    }
    for j in range(1, N_HOMEWORK + 1):
        col = f"hw{j}_status"
        df[col] = [rng.choice(status_variants[v]) for v in df[col]]

    # 2. exercise answer in many spellings, plus some blanks
    ex_variants = {"Yes": ["Yes", "yes", "Y", "yes "], "No": ["No", "no", "N", "NO"]}
    df["exercises"] = [rng.choice(ex_variants[v]) for v in df["exercises"]]
    df.loc[rng.random(n) < 0.06, "exercises"] = np.nan

    # 3. attendance exported as percent strings, some blanks, a few impossible values
    for col in ["midterm_attendance", "final_attendance"]:
        pct = np.round(df[col] * 100).astype(int)
        df[col] = [f"{p}%" for p in pct]
        df.loc[rng.random(n) < 0.05, col] = np.nan
        bad = rng.choice(n, 4, replace=False)
        df.loc[bad, col] = rng.choice(["120%", "135%", "-5%"], 4)

    # 4. a few homework scores typed wrong (out of 10, but 15 or -1)
    for _ in range(6):
        i, j = rng.integers(0, n), rng.integers(1, N_HOMEWORK + 1)
        if not pd.isna(df.loc[i, f"hw{j}_score"]):
            df.loc[i, f"hw{j}_score"] = rng.choice([15.0, -1.0, 99.0])

    # 5. duplicate rows (the export ran twice for some students)
    dups = df.sample(8, random_state=1)
    df = pd.concat([df, dups]).sample(frac=1, random_state=2).reset_index(drop=True)
    return df


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "ai100_students_raw.csv"
    out.parent.mkdir(exist_ok=True)
    data = make_students()
    data.to_csv(out, index=False)
    print(f"Wrote {len(data)} rows x {data.shape[1]} columns to {out}")
