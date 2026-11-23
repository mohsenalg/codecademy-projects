# Analyzing FarmBurg's A/B Test

Hypothesis testing project from the Codecademy **Master Statistics with Python** skill path.

## Goal

FarmBurg is a fictional farming game. Brian, a product manager, wants to sell a small upgrade package (a microtransaction) and tested **3 prices** for one week:

| Group | Price |
|---|---|
| A | $0.99 |
| B | $1.99 |
| C | $4.99 |

The feature is only worth building if it earns **at least $1,000 per week**. Which price should Brian charge?

## Data

`clicks.csv` has 4,998 visitors from one typical week (1,666 per group).

| Column | Meaning |
|---|---|
| `user_id` | Unique visitor ID |
| `group` | A, B or C (the price the visitor saw) |
| `is_purchase` | Yes or No |

The data is fictional and comes from Codecademy.

## Step 1: Do purchase rates differ? (Chi-Square test)

| Group | Price | Purchases | Visitors | Purchase rate |
|---|---|---|---|---|
| A | $0.99 | 316 | 1,666 | 18.97% |
| B | $1.99 | 183 | 1,666 | 10.98% |
| C | $4.99 | 83 | 1,666 | 4.98% |

- **H0:** the purchase rate is the **same** in all 3 groups.
- **H1:** the purchase rate is **different** in at least one group.
- **p-value = 2.41e-35**, so p < 0.05 and we reject H0.

**Conclusion:** Purchase rates are significantly different: the cheaper the price, the more people buy.

**But this is the wrong question.** Brian first wanted to charge $0.99 because "more people bought it". More buyers does not mean more money. What matters is whether each price earns at least $1,000 a week.

## Step 2: Can each price reach $1,000 a week? (binomial tests)

**The rate each price needs** (4,998 visitors per week):

| Price | Sales needed for $1,000 | Purchase rate needed |
|---|---|---|
| $0.99 | 1,011 | 20.23% |
| $1.99 | 503 | 10.06% |
| $4.99 | 201 | 4.02% |

A higher price needs fewer sales, so the target rate is lower.

**One-sided binomial test for each group.** For each price:
- **H0:** the purchase rate **equals** the rate needed for $1,000 a week.
- **H1:** the purchase rate is **greater** than the rate needed.

We use a one-sided test ("greater") because Brian only cares whether the price earns **more** than the target.

| Price | Observed rate | Needed rate | p-value | Conclusion |
|---|---|---|---|---|
| $0.99 | 18.97% | 20.23% | 0.906 | **Not significant.** The rate is actually *below* the target. Not enough evidence it reaches $1,000 |
| $1.99 | 10.98% | 10.06% | 0.114 | **Not significant.** The rate is a little above the target, but this could be random chance |
| $4.99 | 4.98% | 4.02% | 0.0296 | **Significant.** The rate is significantly above the target |

**Expected weekly revenue** if every visitor saw that price (observed rate × 4,998 visitors × price):

| Price | Expected revenue |
|---|---|
| $0.99 | about $939 |
| $1.99 | about $1,093 |
| $4.99 | about $1,243 |

## Recommendation

**Brian should charge $4.99.** It is the only price where the purchase rate is significantly above what is needed to earn $1,000 a week. It also brings in the most expected revenue (about $1,243), even though the fewest people buy it.

$0.99 is the most popular price but would probably **not** reach the target. $1.99 might reach it, but the evidence is not strong enough (p = 0.114).

**Limitations:**
- The test ran for one week, which may not represent every week.
- The rule "revenue at least $1,000" ignores other effects of price, such as player satisfaction or how many players come back.

## What I learned

- **Ask the business question before choosing the test.** The Chi-Square test answered "does price change how many people buy?", but Brian needed "which price earns enough money?".
- **More buyers is not more revenue.** The most popular price ($0.99) earned the least.
- **Turn a money goal into a rate:** $1,000 / price = sales needed; sales needed / visitors = rate needed.
- **Use a one-sided test when only one direction matters.** Brian only needs to know if the rate is *greater* than the target.
- **"Not significant" is not "fails".** $1.99 looked above target, but with this sample size we cannot be confident.

## How to run

```bash
pip install -r requirements.txt
python farmburg_ab_test.py
```

The script prints each test with its hypotheses, p-value and conclusion in plain words.

## Note on the code

Codecademy uses the older `binom_test()` function. This repo uses `binomtest()`, because `binom_test` was removed in SciPy 1.12. The results are the same.

## Files

| File | Description |
|---|---|
| `farmburg_ab_test.py` | Analysis script (all 13 project tasks) |
| `clicks.csv` | A/B test data (4,998 visitors) |
| `requirements.txt` | Python packages |

**Skills:** A/B testing, Chi-Square test, one-sided binomial test, converting a revenue goal into a target rate, pandas, NumPy, SciPy.

Project from Codecademy's Master Statistics with Python skill path.
