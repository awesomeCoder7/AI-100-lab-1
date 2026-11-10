# Fraud detection lab: Decision Tree with Gini vs. Entropy

One notebook, 5 questions. Same synthetic fraud dataset as before (59,940 card payments, ~2.7% fraud),
based on Stripe's [Primer on machine learning for fraud protection](https://stripe.com/guides/primer-on-machine-learning-for-fraud-protection).

```
fraud_tree_lab/
├── notebooks/fraud_tree_gini_vs_entropy.ipynb   ← open this
├── data/transactions.csv                         (re-created automatically if missing)
├── src/
│   ├── tree_lab.py        gini(), entropy(), split_gain(), load/split helpers
│   ├── quiz.py            checks your answers (stored as hashes)
│   ├── config.py          features, time split
│   └── generate_data.py   creates the dataset
└── requirements.txt
```

## Run
```bash
cd into this folder
pip install -r requirements.txt
jupyter notebook notebooks/fraud_tree_gini_vs_entropy.ipynb
```
Change `CRITERION = "gini"` to `"entropy"` at the top and re-run to see the other tree.

| Section | Content | Question |
|---|---|---|
| 1 | Gini impurity by hand | Q1 |
| 2 | Gain of a split by hand | Q2 |
| 3 | Train the tree | |
| 4| Evaluate: accuracy trap, confusion matrix, precision, recall | Q4, Q5 |
| 5 | Gini vs. entropy side by side across depths | |
