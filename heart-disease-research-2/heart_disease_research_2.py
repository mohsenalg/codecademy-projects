"""
Heart Disease Research Part II
Codecademy - Master Statistics with Python (Hypothesis Testing: Associations)

Which patient measurements are associated with heart disease?
- Quantitative variable vs heart disease (2 groups): two-sample t-test
- thalach vs chest pain type (4 groups): ANOVA, then Tukey's range test
- Categorical variable vs heart disease: Chi-Square test

Run: python heart_disease_research_2.py
Box plots are saved to the plots/ folder.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save plots to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency, f_oneway, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "heart_disease.csv"
PLOTS_DIR = BASE_DIR / "plots"
ALPHA = 0.05

REQUIRED_COLUMNS = {"age", "sex", "trestbps", "chol", "cp", "exang", "thalach", "heart_disease"}
VARIABLE_NAMES = {
    "thalach": "maximum heart rate (bpm)",
    "age": "age (years)",
    "trestbps": "resting blood pressure (mm Hg)",
    "chol": "cholesterol (mg/dl)",
    "cp": "chest pain type",
    "sex": "sex",
    "exang": "exercise-induced angina",
}


def load_data(path: Path) -> pd.DataFrame:
    """Load the dataset and check that the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns in data: {sorted(missing)}")
    return data


def save_boxplot(data: pd.DataFrame, x: str, y: str, filename: str) -> None:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x=x, y=y)
    plt.title(f"{VARIABLE_NAMES.get(y, y)} by {VARIABLE_NAMES.get(x, x).replace('_', ' ')}")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / filename, dpi=100)
    plt.close()


def print_result(title: str, h0: str, h1: str, p_value: float, if_significant: str, if_not: str) -> None:
    """Print the hypotheses, the p-value and the conclusion in plain words."""
    significant = p_value < ALPHA
    print(f"\n{title}")
    print(f"  H0: {h0}")
    print(f"  H1: {h1}")
    print(f"  p-value: {p_value:.3g} ({'<' if significant else '>='} {ALPHA})")
    if significant:
        print(f"  Decision: reject H0. {if_significant}")
    else:
        print(f"  Decision: cannot reject H0. {if_not}")


def compare_two_groups(heart: pd.DataFrame, col: str) -> None:
    """Two-sample t-test: mean of `col` for patients with vs without heart disease."""
    with_hd = heart.loc[heart.heart_disease == "presence", col]
    without_hd = heart.loc[heart.heart_disease == "absence", col]
    mean_diff = with_hd.mean() - without_hd.mean()
    median_diff = with_hd.median() - without_hd.median()
    p_value = ttest_ind(with_hd, without_hd).pvalue
    name = VARIABLE_NAMES[col]
    direction = "higher" if mean_diff > 0 else "lower"

    save_boxplot(heart, "heart_disease", col, f"{col}_by_heart_disease.png")
    print(f"\n{col}: mean with heart disease {with_hd.mean():.1f}, without {without_hd.mean():.1f} "
          f"(mean difference {mean_diff:+.1f}, median difference {median_diff:+.1f})")
    print_result(
        f"Two-sample t-test: {col} vs heart disease",
        f"average {name} is the same for patients with and without heart disease",
        f"average {name} is different for the two groups",
        p_value,
        f"Patients with heart disease have a significantly {direction} average {name} "
        f"(about {abs(mean_diff):.1f} {direction}).",
        f"The difference of {mean_diff:+.1f} could be due to random chance; "
        f"there is not enough evidence that average {name} differs between the groups.",
    )


def thalach_by_chest_pain(heart: pd.DataFrame) -> None:
    """ANOVA across the 4 chest pain types, then Tukey's range test for each pair."""
    save_boxplot(heart, "cp", "thalach", "thalach_by_chest_pain.png")
    groups = [heart.loc[heart.cp == cp, "thalach"] for cp in sorted(heart.cp.unique())]
    p_value = f_oneway(*groups).pvalue

    print("\nMean thalach by chest pain type:")
    print(heart.groupby("cp").thalach.mean().round(1).to_string())
    print_result(
        "ANOVA: thalach vs chest pain type (4 groups)",
        "all 4 chest pain types have the same average maximum heart rate",
        "at least one pair of chest pain types has a different average maximum heart rate",
        p_value,
        "At least one pair of chest pain types differs. Tukey's test shows which pairs.",
        "There is not enough evidence that any chest pain types differ.",
    )

    tukey = pairwise_tukeyhsd(heart.thalach, heart.cp, ALPHA)
    print(f"\nTukey's range test (family-wise error rate = {ALPHA} for all 6 pairs):")
    print(tukey)


def chi_square_with_heart_disease(heart: pd.DataFrame, col: str) -> None:
    """Chi-Square test: is categorical `col` associated with heart disease?"""
    xtab = pd.crosstab(heart[col], heart.heart_disease)
    p_value = chi2_contingency(xtab).pvalue
    name = VARIABLE_NAMES[col]
    rates = (xtab["presence"] / xtab.sum(axis=1) * 100).round(1)

    print(f"\nContingency table: {col} vs heart disease")
    print(xtab.to_string())
    print("Heart disease rate (%) per group:")
    print(rates.to_string())
    print_result(
        f"Chi-Square test: {col} vs heart disease",
        f"there is no association between {name} and heart disease",
        f"there is an association between {name} and heart disease",
        p_value,
        f"The heart disease rate is significantly different across {name} groups.",
        f"There is not enough evidence of an association between {name} and heart disease.",
    )


def main() -> None:
    heart = load_data(DATA_PATH)
    PLOTS_DIR.mkdir(exist_ok=True)
    print(f"Patients: {len(heart)} | significance threshold (alpha): {ALPHA}")
    print(heart.head())

    print("\n=== 1. Quantitative variables vs heart disease ===")
    for col in ["thalach", "age", "trestbps", "chol"]:
        compare_two_groups(heart, col)

    print("\n=== 2. Maximum heart rate vs chest pain type ===")
    thalach_by_chest_pain(heart)

    print("\n=== 3. Categorical variables vs heart disease ===")
    for col in ["cp", "sex", "exang"]:
        chi_square_with_heart_disease(heart, col)

    print(f"\nBox plots saved to: {PLOTS_DIR}")


if __name__ == "__main__":
    main()
