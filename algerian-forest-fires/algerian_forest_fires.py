"""Algerian Forest Fires: multiple linear regression.

Weather and fire-risk data from two regions of Algeria (Bejaia and Sidi Bel-abbes):
  1. Predict relative humidity from temperature and region.
  2. Predict FFMC (fuel moisture code) from temperature and fire status, with an interaction.
  3. Predict FFMC from humidity with a squared (polynomial) term.
  4. Explore FFMC from all its weather inputs, and FWI from ISI and BUI.

Run:  python algerian_forest_fires.py
Plots are saved to the plots/ folder.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save plots to files, no window needed

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

DATA_FILE = Path(__file__).parent / "forests.csv"
PLOT_DIR = Path(__file__).parent / "plots"
REQUIRED_COLUMNS = {"temp", "humid", "wind", "rain", "FFMC", "ISI", "BUI", "FWI", "region", "fire"}
HIGH_CORRELATION = 0.8


def load_data(path):
    """Read the CSV and check that the expected columns exist."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path.name}: {sorted(missing)}")
    return df


def save_plot(name):
    """Save the current figure, then close it so plots do not overlap."""
    PLOT_DIR.mkdir(exist_ok=True)
    plt.savefig(PLOT_DIR / name, dpi=120, bbox_inches="tight")
    plt.close("all")


def print_model(title, model):
    """Print coefficients, p-values and R-squared of a fitted model."""
    print(f"\n{title}")
    table = pd.DataFrame({
        "coef": model.params.round(4),
        "p-value": model.pvalues.map(lambda p: f"{p:.3g}"),
    })
    print(table.to_string())
    print(f"  R-squared: {model.rsquared:.3f}")


def line_legend(labels):
    """Legend for the regression lines only (not the scatter points)."""
    plt.legend(plt.gca().get_lines(), labels)


def humidity_section(forests):
    # Task 1: correlations and heat map (multicollinearity check)
    corr_grid = forests.drop(columns=["region", "fire"]).corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr_grid, vmin=-1, center=0, vmax=1, cmap="PuOr", annot=True, fmt=".2f")
    plt.title("Correlations between quantitative variables")
    save_plot("1_correlation_heatmap.png")

    print("Pairs with |correlation| >= 0.8 (do not use together as predictors):")
    columns = corr_grid.columns
    for i, first in enumerate(columns):
        for second in columns[i + 1:]:
            value = corr_grid.loc[first, second]
            if abs(value) >= HIGH_CORRELATION:
                print(f"  {first} and {second}: {value:.2f}")

    # Task 2: humid vs temp, coloured by region
    sns.lmplot(x="temp", y="humid", hue="region", fit_reg=False, data=forests)
    save_plot("2_humid_vs_temp_by_region.png")

    # Task 3: humid ~ temp + region
    modelH = sm.OLS.from_formula("humid ~ temp + region", data=forests).fit()
    print_model("Model: humid ~ temp + region", modelH)

    # Tasks 4 and 5: one equation per region (same slope, different intercepts)
    intercept_bejaia = modelH.params["Intercept"]
    intercept_sidi = intercept_bejaia + modelH.params["region[T.Sidi Bel-abbes]"]
    slope = modelH.params["temp"]
    print(f"  Bejaia:         humid = {intercept_bejaia:.2f} + ({slope:.2f})*temp")
    print(f"  Sidi Bel-abbes: humid = {intercept_sidi:.2f} + ({slope:.2f})*temp")

    # Task 6: scatter plot with both regression lines
    sns.lmplot(x="temp", y="humid", hue="region", fit_reg=False, data=forests)
    temps = np.linspace(forests.temp.min(), forests.temp.max(), 100)
    plt.plot(temps, intercept_bejaia + slope * temps, color="tab:blue", linewidth=3)
    plt.plot(temps, intercept_sidi + slope * temps, color="tab:orange", linewidth=3)
    line_legend(["Bejaia line", "Sidi Bel-abbes line"])
    save_plot("3_humid_vs_temp_with_lines.png")


def interaction_section(forests):
    # Task 7: FFMC vs temp, coloured by fire
    sns.lmplot(x="temp", y="FFMC", hue="fire", fit_reg=False, data=forests)
    save_plot("4_ffmc_vs_temp_by_fire.png")

    # Task 8: FFMC ~ temp + fire + temp:fire
    resultsF = sm.OLS.from_formula("FFMC ~ temp + fire + temp:fire", data=forests).fit()
    print_model("Model: FFMC ~ temp + fire + temp:fire", resultsF)

    # Tasks 9 and 10: one equation per fire group (different intercepts AND slopes)
    intercept_no = resultsF.params["Intercept"]
    slope_no = resultsF.params["temp"]
    intercept_yes = intercept_no + resultsF.params["fire[T.True]"]
    slope_yes = slope_no + resultsF.params["temp:fire[T.True]"]
    print(f"  No fire: FFMC = {intercept_no:.2f} + {slope_no:.2f}*temp")
    print(f"  Fire:    FFMC = {intercept_yes:.2f} + {slope_yes:.2f}*temp")

    # Task 11: scatter plot with both regression lines
    sns.lmplot(x="temp", y="FFMC", hue="fire", fit_reg=False, data=forests)
    temps = np.linspace(forests.temp.min(), forests.temp.max(), 100)
    plt.plot(temps, intercept_no + slope_no * temps, color="tab:blue", linewidth=3)
    plt.plot(temps, intercept_yes + slope_yes * temps, color="tab:orange", linewidth=3)
    line_legend(["No fire line", "Fire line"])
    save_plot("5_ffmc_vs_temp_with_lines.png")


def polynomial_section(forests):
    # Task 12: FFMC vs humid
    sns.lmplot(x="humid", y="FFMC", fit_reg=False, data=forests)
    save_plot("6_ffmc_vs_humid.png")

    # Task 13: FFMC ~ humid + humid^2
    resultsP = sm.OLS.from_formula("FFMC ~ humid + np.power(humid, 2)", data=forests).fit()
    print_model("Model: FFMC ~ humid + humid^2", resultsP)
    simple = sm.OLS.from_formula("FFMC ~ humid", data=forests).fit()
    print(f"  R-squared of the straight-line model (FFMC ~ humid): {simple.rsquared:.3f}")

    # Task 14: predictions at 25%, 35%, 60% and 70% humidity
    b0, b1, b2 = resultsP.params
    print("  Predicted FFMC:")
    for humid in (25, 35, 60, 70):
        print(f"    humid = {humid}%: {b0 + b1 * humid + b2 * humid ** 2:.2f}")
    print(f"  Peak of the curve at humid = {-b1 / (2 * b2):.1f}%")

    # Task 15: straight line vs curved line
    humids = np.linspace(forests.humid.min(), forests.humid.max(), 100)
    sns.lmplot(x="humid", y="FFMC", ci=None, data=forests)
    plt.plot(humids, b0 + b1 * humids + b2 * humids ** 2, linestyle="dashed", linewidth=3, color="black")
    line_legend(["Straight line", "Polynomial curve"])
    save_plot("7_ffmc_vs_humid_polynomial.png")


def exploration_section(forests):
    # Task 16: FFMC from its weather inputs, and FWI from ISI and BUI
    modelFFMC = sm.OLS.from_formula("FFMC ~ humid + temp + wind + rain", data=forests).fit()
    print_model("Model: FFMC ~ humid + temp + wind + rain", modelFFMC)

    modelFWI = sm.OLS.from_formula("FWI ~ ISI + BUI", data=forests).fit()
    print_model("Model: FWI ~ ISI + BUI", modelFWI)
    print(f"  Correlation between ISI and BUI: {forests.ISI.corr(forests.BUI):.2f}")


def main():
    forests = load_data(DATA_FILE)
    print(f"Rows: {len(forests)}")
    print(forests.head(), "\n")

    humidity_section(forests)
    interaction_section(forests)
    polynomial_section(forests)
    exploration_section(forests)
    print(f"\nPlots saved to {PLOT_DIR}")


if __name__ == "__main__":
    main()
