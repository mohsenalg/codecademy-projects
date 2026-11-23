"""
FetchMaker
Codecademy - Master Statistics with Python (Hypothesis Testing project)

FetchMaker matches people with adoptable dogs. Three questions about its dogs:
1. Are whippets more or less likely than 8% to be rescues?     -> binomial test
2. Do whippets, terriers and pitbulls weigh the same?           -> ANOVA, then Tukey
3. Do poodles and shihtzus come in the same mix of colors?      -> Chi-Square test

Run: python fetchmaker_analysis.py
"""

from pathlib import Path

import pandas as pd
from scipy.stats import binomtest, chi2_contingency, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

DATA_PATH = Path(__file__).parent / "dog_data.csv"
ALPHA = 0.05
EXPECTED_RESCUE_RATE = 0.08  # FetchMaker's historical rate for all dogs
MID_SIZED_BREEDS = ["whippet", "terrier", "pitbull"]
COLOR_BREEDS = ["poodle", "shihtzu"]


def load_data(path: Path) -> pd.DataFrame:
    """Load the dog data and check that the needed columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    dogs = pd.read_csv(path)
    missing = {"breed", "is_rescue", "weight", "color"} - set(dogs.columns)
    if missing:
        raise ValueError(f"Missing columns in data: {sorted(missing)}")
    return dogs


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


def whippet_rescues(dogs: pd.DataFrame) -> None:
    """Tasks 2-5: binomial test of the whippet rescue rate against 8%."""
    whippet_rescue = dogs.loc[dogs.breed == "whippet", "is_rescue"]
    num_whippet_rescues = int((whippet_rescue == 1).sum())
    num_whippets = len(whippet_rescue)
    p_value = binomtest(num_whippet_rescues, num_whippets, EXPECTED_RESCUE_RATE).pvalue

    print(f"Whippet rescues: {num_whippet_rescues} of {num_whippets} "
          f"({num_whippet_rescues / num_whippets:.0%}, expected {EXPECTED_RESCUE_RATE:.0%})")
    print_result(
        "Binomial test: whippet rescue rate vs 8%",
        "8% of whippets are rescues",
        "the whippet rescue rate is more or less than 8%",
        p_value,
        "Whippets are rescued at a significantly different rate than other dogs.",
        f"The difference ({num_whippet_rescues / num_whippets:.0%} vs {EXPECTED_RESCUE_RATE:.0%}) "
        "could be due to random chance. There is no evidence that whippets are more or less "
        "likely to be rescues than other dogs.",
    )


def mid_sized_weights(dogs: pd.DataFrame) -> None:
    """Tasks 6-8: ANOVA across 3 breeds, then Tukey's test for each pair."""
    weights = {breed: dogs.loc[dogs.breed == breed, "weight"] for breed in MID_SIZED_BREEDS}
    p_value = f_oneway(*weights.values()).pvalue

    print("\nMean weight (pounds): " + ", ".join(f"{b} {w.mean():.1f}" for b, w in weights.items()))
    print_result(
        "ANOVA: weight of whippets, terriers and pitbulls",
        "all 3 breeds have the same average weight",
        "at least one pair of breeds has a different average weight",
        p_value,
        "At least one pair differs. Tukey's test shows which pairs.",
        "There is not enough evidence that the 3 breeds differ in weight.",
    )

    dogs_wtp = dogs[dogs.breed.isin(MID_SIZED_BREEDS)]
    tukey = pairwise_tukeyhsd(dogs_wtp.weight, dogs_wtp.breed, ALPHA)
    print(f"\nTukey's range test (family-wise error rate = {ALPHA} for all 3 pairs):")
    print(tukey)


def poodle_shihtzu_colors(dogs: pd.DataFrame) -> None:
    """Tasks 9-10: Chi-Square test of breed vs color."""
    dogs_ps = dogs[dogs.breed.isin(COLOR_BREEDS)]
    xtab = pd.crosstab(dogs_ps.color, dogs_ps.breed)
    shares = (xtab / xtab.sum() * 100).round(1)
    p_value = chi2_contingency(xtab).pvalue

    print("\nColor by breed (counts):")
    print(xtab.to_string())
    print("\nColor by breed (% of each breed):")
    print(shares.to_string())
    print_result(
        "Chi-Square test: breed (poodle vs shihtzu) vs color",
        "there is no association between breed and color",
        "there is an association between breed and color",
        p_value,
        "Poodles and shihtzus come in significantly different color mixes.",
        "There is not enough evidence that the color mix differs between the breeds.",
    )


def main() -> None:
    dogs = load_data(DATA_PATH)
    print(f"Dogs: {len(dogs)} | significance threshold (alpha): {ALPHA}\n")
    whippet_rescues(dogs)
    mid_sized_weights(dogs)
    poodle_shihtzu_colors(dogs)


if __name__ == "__main__":
    main()
