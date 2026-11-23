"""
Analyzing FarmBurg's A/B Test
Codecademy - Master Statistics with Python (Hypothesis Testing project)

FarmBurg tested 3 prices for an in-game upgrade package for one week:
group A = $0.99, group B = $1.99, group C = $4.99.
The feature is only worth building if it earns at least $1,000 per week.

1. Does the purchase rate differ between the 3 groups?          -> Chi-Square test
2. For each price, is the purchase rate significantly above the
   rate needed to earn $1,000 per week?                         -> one-sided binomial test

Run: python farmburg_ab_test.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, chi2_contingency

DATA_PATH = Path(__file__).parent / "clicks.csv"
ALPHA = 0.05
REVENUE_TARGET = 1000  # dollars per week
PRICES = {"A": 0.99, "B": 1.99, "C": 4.99}


def load_data(path: Path) -> pd.DataFrame:
    """Load one week of A/B test data and check the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    clicks = pd.read_csv(path)
    missing = {"group", "is_purchase"} - set(clicks.columns)
    if missing:
        raise ValueError(f"Missing columns in data: {sorted(missing)}")
    return clicks


def purchase_rate_by_group(clicks: pd.DataFrame) -> None:
    """Tasks 1-3: Chi-Square test of group vs purchase (the first, less useful question)."""
    xtab = pd.crosstab(clicks.group, clicks.is_purchase)
    rates = (xtab["Yes"] / xtab.sum(axis=1) * 100).round(2)
    p_value = chi2_contingency(xtab).pvalue

    print("Purchases by group:")
    print(xtab.to_string())
    print("\nPurchase rate (%): " + ", ".join(f"{g} {r}%" for g, r in rates.items()))
    print("\nChi-Square test: group vs purchase")
    print("  H0: the purchase rate is the same in all 3 groups")
    print("  H1: the purchase rate is different in at least one group")
    print(f"  p-value: {p_value:.3g}")
    if p_value < ALPHA:
        print("  Decision: reject H0. Purchase rates differ between groups: cheaper prices sell more often.")
    else:
        print("  Decision: cannot reject H0. No evidence that purchase rates differ between groups.")
    print("  Note: this does not tell us which price earns enough money, so we test each price next.")


def price_vs_target(clicks: pd.DataFrame) -> None:
    """Tasks 4-13: for each price, one-sided binomial test against the rate needed for $1,000."""
    num_visits = len(clicks)
    print(f"\nVisitors per week: {num_visits}")

    passing = []
    for group, price in PRICES.items():
        in_group = clicks.group == group
        samp_size = int(in_group.sum())
        sales = int((in_group & (clicks.is_purchase == "Yes")).sum())
        sales_needed = np.ceil(REVENUE_TARGET / price)
        rate_needed = sales_needed / num_visits
        observed_rate = sales / samp_size
        expected_revenue = observed_rate * num_visits * price
        p_value = binomtest(sales, samp_size, rate_needed, alternative="greater").pvalue

        print(f"\nGroup {group} (${price}): needs {sales_needed:.0f} sales a week = {rate_needed:.2%} of visitors")
        print(f"  Observed: {sales}/{samp_size} = {observed_rate:.2%} "
              f"(about ${expected_revenue:,.0f} a week if all visitors saw this price)")
        print(f"  H0: purchase rate = {rate_needed:.2%}   H1: purchase rate > {rate_needed:.2%}")
        print(f"  p-value: {p_value:.3g}")
        if p_value < ALPHA:
            passing.append(f"${price}")
            print(f"  Decision: reject H0. The rate is significantly above the target, so ${price} "
                  f"should earn more than ${REVENUE_TARGET:,} a week.")
        else:
            print(f"  Decision: cannot reject H0. There is not enough evidence that ${price} "
                  f"earns more than ${REVENUE_TARGET:,} a week.")

    if passing:
        print(f"\nRecommendation: charge {' or '.join(passing)}. Only this price is significantly above its target.")
    else:
        print("\nRecommendation: no price is significantly above its target; the feature may not pay off.")


def main() -> None:
    clicks = load_data(DATA_PATH)
    print(f"Significance threshold (alpha): {ALPHA}\n")
    purchase_rate_by_group(clicks)
    price_vs_target(clicks)


if __name__ == "__main__":
    main()
