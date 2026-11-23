"""
Familiar: A Study in Data Analysis
Codecademy - Master Statistics with Python (Hypothesis Testing project)

Familiar is a fictional blood transfusion startup with two products:
the Vein Pack (basic) and the Artery Pack (premium).

Questions:
1. Do Vein Pack subscribers live longer than the 73-year average?  -> one-sample t-test
2. Do Vein and Artery Pack subscribers live equally long?           -> two-sample t-test
3. Is the pack linked to the subscriber's iron level?               -> Chi-Square test

Run: python familiar_analysis.py
"""

from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency, ttest_1samp, ttest_ind

BASE_DIR = Path(__file__).parent
LIFESPAN_PATH = BASE_DIR / "familiar_lifespan.csv"
IRON_PATH = BASE_DIR / "familiar_iron.csv"
ALPHA = 0.05
AVERAGE_LIFE_EXPECTANCY = 73  # years


def load_csv(path: Path, required: set) -> pd.DataFrame:
    """Load a CSV file and check that the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    data = pd.read_csv(path)
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")
    return data


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


def vein_vs_average(vein: pd.Series) -> None:
    """Tasks 1-5: one-sample t-test of Vein Pack lifespans against 73 years."""
    p_value = ttest_1samp(vein, AVERAGE_LIFE_EXPECTANCY).pvalue
    difference = vein.mean() - AVERAGE_LIFE_EXPECTANCY
    direction = "longer" if difference > 0 else "shorter"
    print(f"Vein Pack: {len(vein)} subscribers, mean lifespan {vein.mean():.2f} years")
    print_result(
        "One-sample t-test: Vein Pack vs 73 years",
        f"average Vein Pack lifespan = {AVERAGE_LIFE_EXPECTANCY} years",
        f"average Vein Pack lifespan is not {AVERAGE_LIFE_EXPECTANCY} years",
        p_value,
        f"Vein Pack subscribers live significantly {direction} than {AVERAGE_LIFE_EXPECTANCY} years "
        f"(about {abs(difference):.1f} years {direction}).",
        f"There is not enough evidence that Vein Pack lifespan differs from {AVERAGE_LIFE_EXPECTANCY} years.",
    )


def vein_vs_artery(vein: pd.Series, artery: pd.Series) -> None:
    """Tasks 6-9: two-sample t-test of Vein vs Artery Pack lifespans."""
    p_value = ttest_ind(vein, artery).pvalue
    print(f"\nArtery Pack: {len(artery)} subscribers, mean lifespan {artery.mean():.2f} years")
    print(f"Difference (Vein - Artery): {vein.mean() - artery.mean():+.2f} years")
    print_result(
        "Two-sample t-test: Vein Pack vs Artery Pack",
        "average lifespan is the same for both packs",
        "average lifespan is different for the two packs",
        p_value,
        "The two packs have significantly different average lifespans.",
        "The difference could be due to random chance. There is not enough evidence "
        "that the premium Artery Pack changes lifespan compared with the Vein Pack.",
    )


def pack_vs_iron(iron: pd.DataFrame) -> None:
    """Tasks 10-13: Chi-Square test of pack vs iron level."""
    xtab = pd.crosstab(iron.pack, iron.iron)[["low", "normal", "high"]]
    shares = (xtab.div(xtab.sum(axis=1), axis=0) * 100).round(1)
    p_value = chi2_contingency(xtab).pvalue
    most_common = ", ".join(
        f"{pack.capitalize()} Pack mostly {shares.loc[pack].idxmax()} ({shares.loc[pack].max():.0f}%)"
        for pack in shares.index
    )

    print("\nIron level by pack (counts):")
    print(xtab.to_string())
    print("\nIron level by pack (% of each pack):")
    print(shares.to_string())
    print_result(
        "Chi-Square test: pack vs iron level",
        "there is no association between pack and iron level",
        "there is an association between pack and iron level",
        p_value,
        f"Iron level depends on the pack: {most_common}.",
        "There is not enough evidence that iron level depends on the pack.",
    )


def main() -> None:
    lifespans = load_csv(LIFESPAN_PATH, {"pack", "lifespan"})
    iron = load_csv(IRON_PATH, {"pack", "iron"})
    vein = lifespans.loc[lifespans.pack == "vein", "lifespan"]
    artery = lifespans.loc[lifespans.pack == "artery", "lifespan"]

    print(f"Significance threshold (alpha): {ALPHA}\n")
    vein_vs_average(vein)
    vein_vs_artery(vein, artery)
    pack_vs_iron(iron)


if __name__ == "__main__":
    main()
