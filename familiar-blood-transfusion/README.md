# Familiar: A Study in Data Analysis

Hypothesis testing project from the Codecademy **Master Statistics with Python** skill path.

## Goal

Familiar is a fictional blood transfusion startup with two products: the basic **Vein Pack** and the premium **Artery Pack**. The company wants evidence to use in marketing and to warn customers about side effects. Three questions:

1. Do Vein Pack subscribers live **longer than the 73-year average**?
2. Do Artery Pack subscribers live **longer than Vein Pack** subscribers?
3. Is the pack **linked to iron level** (a possible side effect)?

## Data

| File | Rows | Columns |
|---|---|---|
| `familiar_lifespan.csv` | 40 subscribers (20 Vein, 20 Artery) | `pack` (vein / artery), `lifespan` (years) |
| `familiar_iron.csv` | 345 subscribers (200 Vein, 145 Artery) | `pack` (vein / artery), `iron` (low / normal / high) |

The data is fictional and comes from Codecademy.

## Choosing the test

| Question | Data | Test |
|---|---|---|
| Vein Pack vs 73 years | One group's mean vs a fixed number | One-sample t-test (`ttest_1samp`) |
| Vein Pack vs Artery Pack | Means of 2 independent groups | Two-sample t-test (`ttest_ind`) |
| Pack vs iron level | Two categorical variables | Chi-Square test (`chi2_contingency`) |

Significance threshold (alpha) = **0.05** for every test.

## Results

### 1. Vein Pack vs the 73-year average (one-sample t-test)

- **H0:** the average lifespan of Vein Pack subscribers is **73 years**.
- **H1:** the average lifespan of Vein Pack subscribers is **not 73 years**.

| Group | Subscribers | Mean lifespan | p-value |
|---|---|---|---|
| Vein Pack | 20 | 76.17 years | 5.97e-07 |

**Conclusion:** p < 0.05, so we reject H0. Vein Pack subscribers live **significantly longer** than 73 years, about **3.2 years longer** on average. The test is two-sided, but the sample mean is above 73, so a one-sided "longer than" test gives the same answer (p = 2.99e-07).

### 2. Vein Pack vs Artery Pack (two-sample t-test)

- **H0:** the average lifespan is the **same** for both packs.
- **H1:** the average lifespan is **different** for the two packs.

| Group | Subscribers | Mean lifespan |
|---|---|---|
| Vein Pack | 20 | 76.17 years |
| Artery Pack | 20 | 74.87 years |
| **Difference** | | **1.30 years (Vein higher)** |

**p-value = 0.0559**

**Conclusion:** p ≥ 0.05, so we **cannot reject H0**. The 1.3-year difference could be due to random chance. There is **no evidence that the premium Artery Pack helps people live longer** than the cheaper Vein Pack. In this sample, Artery Pack subscribers actually had a slightly **lower** average.

This does not prove the two packs are the same. The p-value is close to 0.05 and each group has only 20 people, so a bigger sample could show a difference.

### 3. Pack vs iron level (Chi-Square test)

- **H0:** there is **no association** between the pack and iron level.
- **H1:** there **is an association** between the pack and iron level.

| Pack | Low iron | Normal iron | High iron | Total |
|---|---|---|---|---|
| Vein | 140 (70%) | 40 (20%) | 20 (10%) | 200 |
| Artery | 29 (20%) | 29 (20%) | 87 (60%) | 145 |

**p-value = 9.36e-25**

**Conclusion:** p < 0.05, so we reject H0. Iron level is **strongly associated** with the pack. Most **Vein Pack** subscribers have **low** iron (70%), and most **Artery Pack** subscribers have **high** iron (60%). Only 20% in each pack have normal iron.

## Recommendations for Familiar

| Finding | What Familiar can do |
|---|---|
| Vein Pack subscribers live about 3 years longer than average | Use this in marketing for the Vein Pack |
| Artery Pack shows no lifespan benefit over Vein Pack | Do not claim the premium pack makes people live longer |
| Vein Pack linked to low iron, Artery Pack to high iron | Warn customers about this side effect and suggest iron monitoring for both packs |

**Limitations:**
- These are associations, not proof of cause. People who choose to subscribe may already be healthier than average.
- The lifespan sample is small (20 per pack).
- 73 years is a general population average, which may not match the subscribers' background.

## What I learned

- **Pick the test from the question:** one mean vs a number is a one-sample t-test, two group means is a two-sample t-test, two categories is Chi-Square.
- **"Not significant" is not "no difference".** The Vein vs Artery p-value (0.056) was just above 0.05 with a small sample, so the honest conclusion is "not enough evidence", not "the packs are the same".
- **A two-sided test can answer a one-sided question** when the sample mean is on the expected side: the one-sided p-value is half the two-sided one.
- **Percentages make a contingency table easier to read** than raw counts, because the two packs have different group sizes (200 vs 145).

## How to run

```bash
pip install -r requirements.txt
python familiar_analysis.py
```

The script prints each test with its hypotheses, p-value and conclusion in plain words.

## Files

| File | Description |
|---|---|
| `familiar_analysis.py` | Analysis script (all 13 project tasks) |
| `familiar_lifespan.csv` | Lifespan data |
| `familiar_iron.csv` | Iron level data |
| `requirements.txt` | Python packages |

**Skills:** one-sample t-test, two-sample t-test, Chi-Square test, contingency tables, p-value interpretation, pandas, SciPy.

Project from Codecademy's Master Statistics with Python skill path.
