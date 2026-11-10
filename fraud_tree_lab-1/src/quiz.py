"""Checkpoint questions. Answers are stored as hashes, so you can't peek.

Usage in a notebook:
    from quiz import check
    check("I1", 0.42)      # numbers: rounded for you to the decimals the question asks for
    check("I3", "A")       # multiple choice: a letter
"""
import hashlib
import json
from pathlib import Path

_ANSWERS = json.loads((Path(__file__).with_name("quiz_answers.json")).read_text())


def _digest(qid, answer):
    return hashlib.sha256(f"fraud-tree-lab|{qid}|{answer}".encode()).hexdigest()


def check(qid, answer):
    qid = qid.upper()
    if qid not in _ANSWERS:
        print(f"Unknown checkpoint {qid!r}.")
        return
    if answer is None or (isinstance(answer, str) and answer.strip() in ("", "?")):
        print(f"{qid}: replace the ? with your answer, then run the cell again.")
        return
    decimals = _ANSWERS[qid]["decimals"]
    try:
        given = str(answer).strip().upper() if decimals is None else f"{float(answer):.{decimals}f}"
    except ValueError:
        print(f"{qid}: this question needs a number.")
        return
    ok = _digest(qid, given) == _ANSWERS[qid]["hash"]
    print(f"{qid}: {'✅ correct' if ok else '❌ not yet - re-read the cell above and try again'}  (you answered {given})")
