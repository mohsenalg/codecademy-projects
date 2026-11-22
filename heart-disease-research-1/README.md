# Heart Disease Research Part I

Hypothesis testing project from the Codecademy **Master Statistics with Python** skill path.

## Goal

Use one-sample hypothesis tests to answer two questions about patients evaluated for heart disease at the Cleveland Clinic Foundation:

1. **Cholesterol:** Do patients with heart disease have an average cholesterol level significantly above 240 mg/dl (the "high" level)? What about patients without heart disease?
2. **Fasting blood sugar:** Is the share of patients with fasting blood sugar above 120 mg/dl significantly higher than the 8% US diabetes rate in 1988 (when the data was collected)?

## Data

`heart_disease.csv` has 303 patients and 9 columns:

| Column | Meaning |
|---|---|
| `age` | Age in years |
| `sex` | male / female |
| `trestbps` | Resting blood pressure (mm Hg) |
| `chol` | Serum cholesterol (mg/dl) |
| `cp` | Chest pain type |
| `exang` | Exercise-induced angina (1 = yes, 0 = no) |
| `fbs` | Fasting blood sugar > 120 mg/dl (1 = true, 0 = false) |
| `thalach` | Maximum heart rate achieved |
| `heart_disease` | `presence` or `absence` |

**Source:** [UCI Machine Learning Repository: Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease), cleaned by Codecademy. Principal investigators: Andras Janosi, M.D. (Hungarian Institute of Cardiology, Budapest); William Steinbrunn, M.D. (University Hospital, Zurich); Matthias Pfisterer, M.D. (University Hospital, Basel); Robert Detrano, M.D., Ph.D. (V.A. Medical Center, Long Beach and Cleveland Clinic Foundation).

## Methods

Significance threshold (alpha) = **0.05** for all tests.

| Question | Test | Null hypothesis (H0) | Alternative (H1) |
|---|---|---|---|
| Cholesterol (with / without heart disease) | One-sample t-test (`ttest_1samp`) | Mean cholesterol = 240 mg/dl | Mean cholesterol > 240 mg/dl |
| Fasting blood sugar | Binomial test (`binomtest`) | Rate of fbs > 120 mg/dl = 8% | Rate > 8% |

## Results

| Test | Sample result | One-sided p-value | Conclusion |
|---|---|---|---|
| Cholesterol, **with** heart disease (n = 139) | Mean 251.5 mg/dl | 0.0035 | **Significant:** average is above 240 mg/dl |
| Cholesterol, **without** heart disease (n = 164) | Mean 242.6 mg/dl | 0.2640 | **Not significant:** cannot say it is above 240 mg/dl |
| Fasting blood sugar > 120 mg/dl (n = 303) | 45 patients (14.9%), expected 24.2 at 8% | 0.000047 | **Significant:** rate is above 8% |

## Interpretation

- Patients **with** heart disease have an average cholesterol level significantly above the 240 mg/dl "high" level.
- Patients **without** heart disease have a sample mean slightly above 240 mg/dl, but the difference could be due to random chance.
- The share of patients with high fasting blood sugar (about 15%) is significantly higher than the 8% national rate. So this sample is **not representative** of the general US population for this measure. This makes sense: these are patients referred for heart disease testing, not random people.

## What I learned

- **One-sample t-test** compares a sample **mean** with a fixed value (numeric data, like cholesterol).
- **Binomial test** compares a sample **rate** with an expected probability (yes/no data, like fbs > 120).
- **One-sided vs two-sided:** the alternative hypothesis decides which tail counts. For "greater than", use `alternative="greater"`. With an old two-sided only function, you can divide the two-sided p-value by 2, but only when the sample mean is on the same side as the alternative.
- **A sample mean above 240 is not enough.** The no-heart-disease group has a mean of 242.6, but the p-value (0.26) shows this difference could easily be luck.
- **Compare a sample with the population** to check if it is representative before drawing general conclusions.

## How to run

```bash
pip install -r requirements.txt
python heart_disease_research_1.py
```

## Note on the code

The Codecademy version divides a two-sided t-test p-value by 2 and uses `binom_test`, because of the older SciPy in their workspace. This repo uses the current SciPy API instead: `ttest_1samp(..., alternative="greater")` and `binomtest` (`binom_test` was removed in SciPy 1.12). The results are the same.

## Files

| File | Description |
|---|---|
| `heart_disease_research_1.py` | Analysis script |
| `heart_disease.csv` | Dataset |
| `requirements.txt` | Python packages |

**Skills:** hypothesis testing, one-sample t-test, binomial test, p-values, significance thresholds, pandas, SciPy.

Project from Codecademy's Master Statistics with Python skill path.
