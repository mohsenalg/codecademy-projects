# Heart Disease Research Part II

Hypothesis testing project from the Codecademy **Master Statistics with Python** skill path (Hypothesis Testing: Associations).

## Goal

Find which patient measurements are **associated with heart disease**, using data from patients evaluated at the Cleveland Clinic Foundation. Three kinds of questions:

1. Is a **number** (heart rate, age, blood pressure, cholesterol) different for patients with and without heart disease?
2. Is **maximum heart rate** different across the 4 **chest pain types**?
3. Is a **category** (chest pain type, sex, exercise-induced angina) linked to heart disease?

## Data

`heart_disease.csv` has 303 patients (139 with heart disease, 164 without) and 9 columns:

| Column | Meaning |
|---|---|
| `age` | Age in years |
| `sex` | male / female |
| `trestbps` | Resting blood pressure (mm Hg) |
| `chol` | Serum cholesterol (mg/dl) |
| `cp` | Chest pain type: typical angina, atypical angina, non-anginal pain, asymptomatic |
| `exang` | Exercise-induced angina (1 = yes, 0 = no) |
| `fbs` | Fasting blood sugar > 120 mg/dl (1 = yes, 0 = no) |
| `thalach` | Maximum heart rate in an exercise test (bpm) |
| `heart_disease` | `presence` or `absence` |

**Source:** [UCI Machine Learning Repository: Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease), cleaned by Codecademy. Principal investigators: Andras Janosi, M.D. (Hungarian Institute of Cardiology, Budapest); William Steinbrunn, M.D. (University Hospital, Zurich); Matthias Pfisterer, M.D. (University Hospital, Basel); Robert Detrano, M.D., Ph.D. (V.A. Medical Center, Long Beach and Cleveland Clinic Foundation).

## Choosing the test

| Question type | Test | Python |
|---|---|---|
| Number vs 2 groups | Two-sample t-test | `scipy.stats.ttest_ind` |
| Number vs 3+ groups | ANOVA, then Tukey's range test | `scipy.stats.f_oneway`, `statsmodels pairwise_tukeyhsd` |
| Category vs category | Chi-Square test | `scipy.stats.chi2_contingency` |

Significance threshold (alpha) = **0.05** for every test.

## Results

### 1. Numbers vs heart disease (two-sample t-test)

For each variable:
- **H0:** the average is the **same** for patients with and without heart disease.
- **H1:** the average is **different** for the two groups.

| Variable | With heart disease | Without | Difference | p-value | Conclusion |
|---|---|---|---|---|---|
| `thalach` max heart rate | 139.3 bpm | 158.4 bpm | -19.1 | 3.46e-14 | p < 0.05, reject H0. Patients with heart disease reach a **significantly lower** maximum heart rate (about 19 bpm lower). |
| `age` | 56.6 years | 52.6 years | +4.0 | 8.96e-05 | p < 0.05, reject H0. Patients with heart disease are **significantly older** (about 4 years). |
| `trestbps` resting blood pressure | 134.6 mm Hg | 129.2 mm Hg | +5.3 | 0.0085 | p < 0.05, reject H0. Patients with heart disease have **significantly higher** resting blood pressure (about 5 mm Hg). |
| `chol` cholesterol | 251.5 mg/dl | 242.6 mg/dl | +8.8 | 0.139 | p ≥ 0.05, cannot reject H0. The 8.8 mg/dl difference **could be random chance**. Not enough evidence that average cholesterol differs. |

### 2. Maximum heart rate vs chest pain type (ANOVA + Tukey)

Average `thalach`: asymptomatic 140.7, atypical angina 162.4, typical angina 156.0, non-anginal pain 155.4.

**ANOVA**
- **H0:** all 4 chest pain types have the **same** average maximum heart rate.
- **H1:** **at least one pair** of chest pain types has a different average.
- **p-value = 1.91e-10**, so p < 0.05 and we reject H0. At least one pair of chest pain types has a significantly different average maximum heart rate. ANOVA does not say which pair, so we run Tukey's test next.

**Tukey's range test** compares all 6 pairs and keeps the overall Type I error rate at 0.05 (running 6 separate t-tests would raise the chance of a false positive).

| Pair | Mean difference | Adjusted p-value | Conclusion |
|---|---|---|---|
| asymptomatic vs atypical angina | 21.7 | < 0.001 | Significant |
| asymptomatic vs non-anginal pain | 14.7 | < 0.001 | Significant |
| asymptomatic vs typical angina | 15.3 | 0.008 | Significant |
| atypical angina vs non-anginal pain | -7.0 | 0.248 | Not significant |
| atypical angina vs typical angina | -6.5 | 0.621 | Not significant |
| non-anginal pain vs typical angina | 0.5 | 0.999 | Not significant |

**Conclusion:** **Asymptomatic** patients have a significantly **lower** maximum heart rate than each of the other 3 chest pain types. The other 3 types are not significantly different from each other.

### 3. Categories vs heart disease (Chi-Square test)

For each variable:
- **H0:** there is **no association** between the variable and heart disease.
- **H1:** there **is an association**.

**Chest pain type (`cp`)**

| Chest pain type | No heart disease | Heart disease | Heart disease rate |
|---|---|---|---|
| asymptomatic | 39 | 105 | 72.9% |
| atypical angina | 41 | 9 | 18.0% |
| non-anginal pain | 68 | 18 | 20.9% |
| typical angina | 16 | 7 | 30.4% |

| Variable | Heart disease rate | p-value | Conclusion |
|---|---|---|---|
| `cp` chest pain type | 18% to 73% (table above) | 1.25e-17 | p < 0.05, reject H0. Chest pain type is **significantly associated** with heart disease. Asymptomatic patients have by far the highest rate (73%). |
| `sex` | male 55.3%, female 25.8% | 2.67e-06 | p < 0.05, reject H0. Sex is **significantly associated** with heart disease. Men in this sample have about twice the rate of women. |
| `exang` exercise-induced angina | yes 76.8%, no 30.9% | 1.41e-13 | p < 0.05, reject H0. Exercise-induced angina is **significantly associated** with heart disease. |

## Summary

| Linked to heart disease | Not enough evidence |
|---|---|
| Lower max heart rate, older age, higher resting blood pressure, chest pain type, sex, exercise-induced angina | Cholesterol |

The most surprising result: patients with **no chest pain** (asymptomatic) were the most likely to have heart disease. Having no symptoms does not mean having no disease.

**Limitations:** These are associations, not causes. The patients were referred for heart disease testing, so they are not a random sample of the general population.

## What I learned

- **Pick the test from the data types:** number vs 2 groups is a t-test, number vs 3+ groups is ANOVA, category vs category is Chi-Square.
- **ANOVA only says "at least one pair is different".** A post-hoc test like Tukey's is needed to find which pairs.
- **Tukey's test controls the overall error rate.** Six separate t-tests at 0.05 would give a much higher chance of at least one false positive.
- **A difference in the sample is not enough.** Cholesterol was 8.8 mg/dl higher in the heart disease group, but p = 0.139 means this could easily be random chance.
- **"Cannot reject H0" is not "H0 is true".** It only means there is not enough evidence of a difference.

## How to run

```bash
pip install -r requirements.txt
python heart_disease_research_2.py
```

The script prints each test with its hypotheses, p-value and conclusion, and saves the box plots to a `plots/` folder.

## Files

| File | Description |
|---|---|
| `heart_disease_research_2.py` | Analysis script (all 14 project tasks) |
| `heart_disease.csv` | Dataset |
| `requirements.txt` | Python packages |

**Skills:** two-sample t-test, ANOVA, Tukey's range test, Chi-Square test, contingency tables, box plots, pandas, SciPy, statsmodels, seaborn.

Project from Codecademy's Master Statistics with Python skill path.
