# FetchMaker

Hypothesis testing project from the Codecademy **Master Statistics with Python** skill path.

## Goal

FetchMaker is a fictional startup that matches people with adoptable dogs. Using data on 800 dogs, this project answers three questions:

1. Are **whippets** more or less likely than other dogs to be **rescues** (8% for all dogs)?
2. Do **whippets, terriers and pitbulls** have the same average **weight**?
3. Do **poodles and shihtzus** come in the same mix of **colors**?

## Data

`dog_data.csv` has 800 dogs: 100 each of 8 breeds (chihuahua, greyhound, pitbull, poodle, rottweiler, shihtzu, terrier, whippet).

| Column | Meaning |
|---|---|
| `is_rescue` | 1 = rescue dog, 0 = not |
| `weight` | Weight in pounds |
| `tail_length` | Tail length in inches |
| `age` | Age in years |
| `color` | black, brown, gold, grey or white |
| `likes_children` | 1 = yes, 0 = no |
| `is_hypoallergenic` | 1 = yes, 0 = no |
| `name` | Dog's name |
| `breed` | Dog breed |

The data is fictional and comes from Codecademy.

## Choosing the test

| Question | Data | Test |
|---|---|---|
| Whippet rescue rate vs 8% | One group's rate (yes/no) vs an expected rate | Binomial test (`binomtest`) |
| Weight of 3 breeds | Numeric variable, 3 groups | ANOVA (`f_oneway`), then Tukey's range test (`pairwise_tukeyhsd`) |
| Poodle vs shihtzu colors | Two categorical variables | Chi-Square test (`chi2_contingency`) |

Significance threshold (alpha) = **0.05** for every test.

## Results

### 1. Whippet rescue rate (binomial test)

- **H0:** 8% of whippets are rescues (the same as all dogs).
- **H1:** the whippet rescue rate is **more or less** than 8%.

| Whippets | Rescues | Rescue rate | Expected | p-value |
|---|---|---|---|---|
| 100 | 6 | 6% | 8% | 0.581 |

**Conclusion:** p ≥ 0.05, so we **cannot reject H0**. 6% is a little below 8%, but a gap this small could easily be random chance with 100 dogs. There is **no evidence** that whippets are more or less likely to be rescues than other dogs.

### 2. Weight of whippets, terriers and pitbulls (ANOVA + Tukey)

| Breed | Mean weight |
|---|---|
| Pitbull | 44.2 lb |
| Whippet | 40.8 lb |
| Terrier | 30.9 lb |

**ANOVA**
- **H0:** all 3 breeds have the **same** average weight.
- **H1:** **at least one pair** of breeds has a different average weight.
- **p-value = 3.28e-17**, so p < 0.05 and we reject H0. At least one pair of breeds has a different average weight. ANOVA does not say which pair, so we run Tukey's test next.

**Tukey's range test** compares all 3 pairs and keeps the overall Type I error rate at 0.05.

| Pair | Mean difference | Adjusted p-value | Conclusion |
|---|---|---|---|
| pitbull vs terrier | 13.2 lb | < 0.001 | **Significant:** pitbulls are heavier |
| terrier vs whippet | 9.9 lb | < 0.001 | **Significant:** whippets are heavier |
| pitbull vs whippet | 3.3 lb | 0.064 | Not significant |

**Conclusion:** **Terriers are significantly lighter** than both pitbulls (by about 13 lb) and whippets (by about 10 lb). Pitbulls and whippets are not significantly different: the 3.3 lb gap could be random chance (p = 0.064, just above 0.05).

### 3. Poodle vs shihtzu colors (Chi-Square test)

- **H0:** there is **no association** between breed and color (both breeds have the same color mix).
- **H1:** there **is an association** between breed and color.

| Color | Poodle | Shihtzu |
|---|---|---|
| black | 17 (17%) | 10 (10%) |
| brown | 13 (13%) | **36 (36%)** |
| gold | 8 (8%) | 6 (6%) |
| grey | **52 (52%)** | 41 (41%) |
| white | 10 (10%) | 7 (7%) |

**p-value = 0.0053**

**Conclusion:** p < 0.05, so we reject H0. Poodles and shihtzus come in **significantly different color mixes**. The biggest difference is **brown**: 36% of shihtzus but only 13% of poodles. Poodles are more often grey (52% vs 41%) and black (17% vs 10%).

**Note:** The Codecademy task text swaps the two hypotheses for this test (it lists "there is an association" as the null). The Chi-Square test always uses **"no association"** as the null, so this README uses the correct version.

## Summary for FetchMaker

| Question | Answer |
|---|---|
| Are whippets rescued more or less often? | No evidence of a difference (6% vs 8%) |
| Do the 3 mid-sized breeds weigh the same? | No. Terriers are lighter; pitbulls and whippets are similar |
| Do poodles and shihtzus have the same colors? | No. Shihtzus are much more often brown |

**Limitations:** The data is a sample of 100 dogs per breed. The results describe FetchMaker's dogs, not all dogs of these breeds.

## What I learned

- **Pick the test from the data type:** a yes/no rate vs a known rate is a binomial test, a number across 3+ groups is ANOVA, two categories is Chi-Square.
- **ANOVA only says "at least one pair differs".** Tukey's test is needed to find which pairs, and it keeps the overall false positive rate at 0.05.
- **"Not significant" means "no evidence", not "the same".** 6% vs 8% rescues, and the 3.3 lb pitbull vs whippet gap, could both be random chance with these sample sizes.
- **Always check the hypotheses.** In a Chi-Square test the null is always "no association", even if a task describes it the other way round.
- **Percentages make a contingency table easier to compare**, and they show where the difference comes from (here, brown dogs).

## How to run

```bash
pip install -r requirements.txt
python fetchmaker_analysis.py
```

The script prints each test with its hypotheses, p-value and conclusion in plain words.

## Files

| File | Description |
|---|---|
| `fetchmaker_analysis.py` | Analysis script (all project tasks) |
| `dog_data.csv` | Dog data (800 dogs) |
| `requirements.txt` | Python packages |

**Skills:** binomial test, ANOVA, Tukey's range test, Chi-Square test, contingency tables, p-value interpretation, pandas, SciPy, statsmodels.

Project from Codecademy's Master Statistics with Python skill path.
