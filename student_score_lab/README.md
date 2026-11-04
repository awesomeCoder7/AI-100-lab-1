# AI-100 section 1 Lab2 data preprocessing, linear regression/classifier by Siyu Wu

You are given a data pipeline that **runs but is missing 9 data-processing steps**.
You patch it piece by piece and watch a scoreboard improve. Then you use the cleaned data to predict each
student's **final score** (linear regression) and whether they **pass** with 70+ (logistic regression),
and look inside what each model/s learning objectives (what they are optimizing).

All data is synthetic. No real student records.

## Folder layout
```
student_score_lab/
├── README.md
├── requirements.txt
├── src/
│   ├── make_data.py              # synthetic data generator
│   └── quiz.py                   # checks your answers to the Checkpoint questions
├── data/                         # filled by notebook 01
├── outputs/                      # scoreboard.csv is written here
└── notebooks/
    ├── 01_fix_the_pipeline.ipynb
    ├── 02_linear_regression.ipynb
    └── 03_logistic_regression.ipynb
```

## How to work
```bash
cd in to your folder
pip install -r requirements.txt
jupyter lab            
```
Google Colab also works: upload the whole folder and open the notebooks from it.

1. **Notebook 01 - Fix the pipeline.** Run it once as it is and look at the Scoreboard at the bottom.
   Then, for each **Patch** box: read the symptom, write your prediction, copy the code into the empty
   cell below the box, and **Restart & Run All**. The scoreboard keeps every run.
   Goal: R² ≈ 0.87 and AUC ≈ 0.97 (the baseline is ≈ 0.75 and ≈ 0.91).
2. **Notebook 02 - Linear regression.** The least-squares objective (MSE), the gradient descent
   written by hand (optional), outliers, coefficients, MAE / RMSE / R².
3. **Notebook 03 - Logistic regression.** The sigmoid, the log-loss objective, why we don't train on
   accuracy, gradient descent with and without scaling, confusion matrix, thresholds, ROC / AUC, odds ratios.

Notebooks 02 and 03 use what notebook 01 saves, so **finish 01 first**. If you go on with patches still
missing, 02 and 03 will warn you and their numbers will be worse.

## Checkpoint questions
Each notebook has **Checkpoint** questions (21 in total). Replace the `?` and run the cell:
```python
check("P1", "B")      # multiple choice -> a letter
check("O2", 16.7)     # numeric -> a number
summary()             # how many you have right
```
You get a hint when you're wrong and an explanation when you're right.

| Prefix | Notebook | Topic |
|---|---|---|
| P1-P9 | 01 | data preprocessing |
| O1-O6 | 02 | least-squares objective, gradient descent, R² |
| L1-L6 | 03 | sigmoid, log-loss objective, scaling and optimization, thresholds |
