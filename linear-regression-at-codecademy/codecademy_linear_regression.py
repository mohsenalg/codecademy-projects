"""Linear Regression at Codecademy.

Simple linear regression on simulated learner data:
  1. Does the number of completed content items predict quiz score?
  2. Does the lesson taken right before the quiz (A or B) predict quiz score?

Run:  python codecademy_linear_regression.py
Plots are saved to the plots/ folder.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save plots to files, no window needed

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy import stats

DATA_FILE = Path(__file__).parent / "codecademy.csv"
PLOT_DIR = Path(__file__).parent / "plots"
REQUIRED_COLUMNS = {"score", "completed", "lesson"}
ALPHA = 0.05


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
    """Save the current figure, then clear it for the next plot."""
    PLOT_DIR.mkdir(exist_ok=True)
    plt.savefig(PLOT_DIR / name, dpi=120, bbox_inches="tight")
    plt.clf()


def print_result(title, h0, h1, p_value, if_significant, if_not):
    """Print one hypothesis test with its assumption and plain-English decision."""
    print(f"\n{title}")
    print(f"  H0: {h0}")
    print(f"  H1: {h1}")
    print(f"  p-value: {p_value:.4g}")
    if p_value < ALPHA:
        print(f"  Decision: p < {ALPHA}, reject H0. {if_significant}")
    else:
        print(f"  Decision: p >= {ALPHA}, do not reject H0. {if_not}")


def main():
    codecademy = load_data(DATA_FILE)

    # Task 1: inspect the data
    print("First five rows:")
    print(codecademy.head())
    print(f"\nRows: {len(codecademy)}")

    # Task 2: scatter plot of score vs completed
    plt.scatter(codecademy.completed, codecademy.score)
    plt.xlabel("Completed content items")
    plt.ylabel("Quiz score")
    plt.title("Quiz score vs completed items")
    save_plot("1_scatter_score_vs_completed.png")

    # Task 3: fit score ~ completed
    model = sm.OLS.from_formula("score ~ completed", data=codecademy).fit()
    intercept = model.params["Intercept"]
    slope = model.params["completed"]
    print("\nModel 1: score ~ completed")
    print(model.params)
    print(f"R-squared: {model.rsquared:.3f}")

    # Task 4: interpretation
    print(f"Intercept: a learner with 0 completed items is expected to score "
          f"{intercept:.2f}.")
    print(f"Slope: each extra completed item goes with a {slope:.2f} point "
          f"higher expected score.")

    print_result(
        "Test of the slope (completed)",
        "slope = 0 (completed items have no linear link with quiz score)",
        "slope != 0 (completed items are linked with quiz score)",
        model.pvalues["completed"],
        "There is evidence that learners who completed more items score higher.",
        "There is no evidence of a link between completed items and score.",
    )

    # Task 5: scatter plot with the regression line
    plt.scatter(codecademy.completed, codecademy.score)
    plt.plot(codecademy.completed, intercept + slope * codecademy.completed,
             color="red")
    plt.xlabel("Completed content items")
    plt.ylabel("Quiz score")
    plt.title("Regression line: score ~ completed")
    save_plot("2_regression_line.png")

    # Task 6: prediction for 20 completed items
    predicted_20 = model.predict({"completed": [20]})[0]
    print(f"\nPredicted score for 20 completed items: {predicted_20:.2f}")

    # Tasks 7 and 8: fitted values and residuals
    fitted_values = model.predict(codecademy)
    residuals = codecademy.score - fitted_values

    # Task 9: normality assumption
    plt.hist(residuals, bins=15)
    plt.xlabel("Residual")
    plt.title("Histogram of residuals")
    save_plot("3_residuals_histogram.png")

    shapiro_p = stats.shapiro(residuals).pvalue
    print_result(
        "Normality of residuals (Shapiro-Wilk)",
        "the residuals are normally distributed",
        "the residuals are not normally distributed",
        shapiro_p,
        "The normality assumption looks broken.",
        "There is no evidence against normality, so the assumption is met.",
    )

    # Task 10: homoscedasticity assumption
    plt.scatter(fitted_values, residuals)
    plt.axhline(0, color="red")
    plt.xlabel("Fitted value")
    plt.ylabel("Residual")
    plt.title("Residuals vs fitted values")
    save_plot("4_residuals_vs_fitted.png")

    # Task 11: boxplot of score by lesson
    sns.boxplot(x="lesson", y="score", data=codecademy)
    plt.title("Quiz score by lesson")
    save_plot("5_boxplot_score_by_lesson.png")

    # Task 12: fit score ~ lesson
    model_lesson = sm.OLS.from_formula("score ~ lesson", data=codecademy).fit()
    diff_coef = model_lesson.params["lesson[T.Lesson B]"]
    print("\nModel 2: score ~ lesson")
    print(model_lesson.params)

    # Task 13: group means and difference
    mean_a = codecademy.score[codecademy.lesson == "Lesson A"].mean()
    mean_b = codecademy.score[codecademy.lesson == "Lesson B"].mean()
    print(f"Mean score, Lesson A: {mean_a:.2f}  (equals the intercept)")
    print(f"Mean score, Lesson B: {mean_b:.2f}")
    print(f"Difference B - A:     {mean_b - mean_a:.2f}  (equals the slope)")

    better = "Lesson A" if diff_coef < 0 else "Lesson B"
    print_result(
        "Test of the lesson coefficient",
        "mean score is the same for Lesson A and Lesson B (difference = 0)",
        "mean score is different for Lesson A and Lesson B",
        model_lesson.pvalues["lesson[T.Lesson B]"],
        f"There is evidence that {better} learners score higher.",
        "There is no evidence that the lesson changes the quiz score.",
    )

    # Task 14: preview of multiple regression
    sns.lmplot(x="completed", y="score", hue="lesson", data=codecademy)
    plt.title("Score vs completed, by lesson")
    PLOT_DIR.mkdir(exist_ok=True)
    plt.savefig(PLOT_DIR / "6_lmplot_by_lesson.png", dpi=120,
                bbox_inches="tight")
    plt.close("all")

    print(f"\nPlots saved to {PLOT_DIR}")


if __name__ == "__main__":
    main()
