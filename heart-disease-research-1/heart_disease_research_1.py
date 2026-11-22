"""
Heart Disease Research Part I
Codecademy - Master Statistics with Python (Hypothesis Testing)

Questions:
1. Do patients with heart disease have an average cholesterol level
   significantly above 240 mg/dl? And patients without heart disease?
2. Is the rate of high fasting blood sugar (fbs > 120 mg/dl) in this
   sample significantly higher than the 8% US diabetes rate (1988)?
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, ttest_1samp

DATA_PATH = Path(__file__).parent / "heart_disease.csv"
ALPHA = 0.05
HIGH_CHOLESTEROL = 240      # mg/dl
US_DIABETES_RATE = 0.08     # about 8% in 1988


def load_data(path: Path) -> pd.DataFrame:
    """Load the dataset and check that the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    data = pd.read_csv(path)
    required = {"chol", "fbs", "heart_disease"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns in data: {sorted(missing)}")
    return data


def decision(p_value: float) -> str:
    return "Significant (reject the null)" if p_value < ALPHA else "Not significant (cannot reject the null)"


def cholesterol_test(chol: pd.Series, group: str) -> None:
    """One-sample t-test. H0: mean = 240 mg/dl, H1: mean > 240 mg/dl."""
    chol = chol.dropna()
    result = ttest_1samp(chol, HIGH_CHOLESTEROL, alternative="greater")
    print(f"\nCholesterol: patients {group} heart disease (n = {len(chol)})")
    print(f"  Mean cholesterol: {chol.mean():.1f} mg/dl")
    print(f"  One-sided p-value: {result.pvalue:.4f}")
    print(f"  Result: {decision(result.pvalue)}")


def fasting_blood_sugar_test(heart: pd.DataFrame) -> None:
    """Binomial test. H0: rate = 8%, H1: rate > 8%."""
    num_patients = len(heart)
    num_highfbs_patients = int(np.sum(heart.fbs == 1))
    expected = num_patients * US_DIABETES_RATE
    result = binomtest(num_highfbs_patients, num_patients, US_DIABETES_RATE, alternative="greater")

    print("\nFasting blood sugar > 120 mg/dl")
    print(f"  Number of patients: {num_patients}")
    print(f"  Patients with high fbs: {num_highfbs_patients} ({num_highfbs_patients / num_patients:.1%})")
    print(f"  Expected at 8%: {expected:.1f}")
    print(f"  One-sided p-value: {result.pvalue:.6f}")
    print(f"  Result: {decision(result.pvalue)}")


def main() -> None:
    heart = load_data(DATA_PATH)
    yes_hd = heart[heart.heart_disease == "presence"]
    no_hd = heart[heart.heart_disease == "absence"]

    print(f"Significance threshold (alpha): {ALPHA}")
    cholesterol_test(yes_hd.chol, "with")
    cholesterol_test(no_hd.chol, "without")
    fasting_blood_sugar_test(heart)


if __name__ == "__main__":
    main()
