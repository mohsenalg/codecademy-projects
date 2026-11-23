"""
A/B Testing at Nosh Mish Mosh
Codecademy - Master Statistics with Python (Sample Size Determination)

Question: How many visitors must see the new "artisanal vegetables" photos
before we can tell if they bring in at least $1,240 more revenue per week?

A sample size needs 3 inputs:
1. Baseline conversion rate  - from one week of visitor data
2. Minimum detectable effect - the lift needed to earn $1,240 more per week
3. Significance threshold    - 10% (a small business decision)

Run: python nosh_mish_mosh_ab_test.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

DATA_PATH = Path(__file__).parent / "customer_visits.csv"
TARGET_EXTRA_REVENUE = 1240   # dollars per week
SIGNIFICANCE_THRESHOLD = 0.10
POWER = 0.80                  # the calculator aims for 80% power
CALCULATOR_SAMPLE_SIZE = 490  # from Codecademy's A/B sample size calculator


def load_data(path: Path) -> pd.DataFrame:
    """Load one week of site visits and check the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    visits = pd.read_csv(path)
    required = {"purchased", "moneyspent"}
    missing = required - set(visits.columns)
    if missing:
        raise ValueError(f"Missing columns in data: {sorted(missing)}")
    return visits


def baseline_conversion(visits: pd.DataFrame) -> float:
    """Percent of visitors who bought something (tasks 4-8)."""
    total_visitor_count = len(visits)
    paying_visitor_count = int(visits.purchased.sum())
    baseline_percent = paying_visitor_count / total_visitor_count * 100.0
    print(f"Visitors in a typical week: {total_visitor_count}")
    print(f"Paying visitors:            {paying_visitor_count}")
    print(f"Baseline conversion rate:   {baseline_percent:.2f}%")
    return baseline_percent


def minimum_detectable_effect(visits: pd.DataFrame, baseline_percent: float) -> float:
    """Relative lift needed to earn TARGET_EXTRA_REVENUE more per week (tasks 9-14)."""
    payment_history = visits.loc[visits.purchased, "moneyspent"]
    average_payment = np.mean(payment_history)
    new_customers_needed = np.ceil(TARGET_EXTRA_REVENUE / average_payment)
    percentage_point_increase = new_customers_needed / len(visits) * 100
    mde = percentage_point_increase / baseline_percent * 100.0

    print(f"\nAverage payment per paying customer: ${average_payment:.2f}")
    print(f"New customers needed for ${TARGET_EXTRA_REVENUE}: {new_customers_needed:.0f}")
    print(f"Needed increase in conversion: {percentage_point_increase:.2f} percentage points "
          f"({baseline_percent:.2f}% -> {baseline_percent + percentage_point_increase:.2f}%)")
    print(f"Minimum detectable effect (relative lift): {mde:.2f}%")
    return mde


def check_sample_size(baseline_percent: float, mde: float) -> None:
    """Compare the calculator's answer with a standard power calculation (tasks 15-16)."""
    p_control = baseline_percent / 100
    p_new = p_control * (1 + mde / 100)
    effect_size = proportion_effectsize(p_new, p_control)
    per_group = NormalIndPower().solve_power(
        effect_size=effect_size, alpha=SIGNIFICANCE_THRESHOLD, power=POWER, alternative="two-sided"
    )

    print(f"\nSignificance threshold: {SIGNIFICANCE_THRESHOLD:.0%}, power: {POWER:.0%}")
    print(f"Calculator sample size (ab_sample_size): {CALCULATOR_SAMPLE_SIZE} visitors in total "
          f"(about {CALCULATOR_SAMPLE_SIZE // 2} per version)")
    print(f"statsmodels check: {np.ceil(per_group):.0f} per version, "
          f"{2 * np.ceil(per_group):.0f} in total")


def main() -> None:
    visits = load_data(DATA_PATH)
    baseline_percent = baseline_conversion(visits)
    mde = minimum_detectable_effect(visits, baseline_percent)
    check_sample_size(baseline_percent, mde)


if __name__ == "__main__":
    main()
