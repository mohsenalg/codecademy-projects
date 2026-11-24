# Linear Regression at Codecademy

Simple linear regression on simulated Codecademy learner data, from the Codecademy **Master Statistics with Python** skill path.

## Goal

The question is which learner factors are linked with quiz performance:

1. Do learners who have **completed more content items** score higher on the quiz?
2. Do learners score differently depending on the **lesson (A or B)** they took right before the quiz?

## Data

`codecademy.csv` has 100 learners and 3 columns:

| Column | Meaning |
|---|---|
| `score` | Quiz score |
| `completed` | Number of other Codecademy content items completed before the quiz |
| `lesson` | Lesson taken right before the quiz (`Lesson A` or `Lesson B`) |

## Method

- Models are fitted with `statsmodels` ordinary least squares: `sm.OLS.from_formula('score ~ completed', data)` and `sm.OLS.from_formula('score ~ lesson', data)`.
- The model assumptions are checked with a histogram of the residuals (normality, with a Shapiro-Wilk test) and a plot of residuals against fitted values (equal spread, called homoscedasticity).
- The significance level is alpha = 0.05 for every test.

## Results

### Model 1: score ~ completed

| Term | Value |
|---|---|
| Intercept | 13.21 |
| Slope (`completed`) | 1.31 |
| R-squared | 0.46 |

- **Intercept:** a learner with 0 completed items is expected to score about 13.2.
- **Slope:** each extra completed item goes with about 1.31 more quiz points.
- **Prediction:** a learner with 20 completed items is expected to score **39.35**.

**Test of the slope**
- H0: the slope is 0, so completed items have no linear link with quiz score.
- H1: the slope is not 0, so completed items are linked with quiz score.
- p-value: **8.07e-15**
- Conclusion: p < 0.05, so we reject H0. There is strong evidence that learners who completed more items score higher. The link is positive, and `completed` explains about 46% of the variation in score. The rest comes from other factors.

### Checking the assumptions

**Normality of residuals (Shapiro-Wilk)**
- H0: the residuals are normally distributed.
- H1: the residuals are not normally distributed.
- p-value: **0.413**
- Conclusion: p >= 0.05, so we do not reject H0. There is no evidence against normality. The histogram also looks bell-shaped, so the normality assumption is met.

**Homoscedasticity (equal spread)**
- The residuals vs fitted values plot shows no pattern and no funnel shape. The spread of the residuals is about the same for low fitted values (SD 13.0) and high fitted values (SD 12.1), so the equal-spread assumption is met.

**Linearity**
- The scatter plot shows the points following a straight upward trend, so a straight line is a reasonable model.

### Model 2: score ~ lesson

| Term | Value | Meaning |
|---|---|---|
| Intercept | 59.22 | Mean score of Lesson A (the reference group) |
| `lesson[T.Lesson B]` | -11.64 | Lesson B mean minus Lesson A mean |

| Group | Mean score |
|---|---|
| Lesson A | 59.22 |
| Lesson B | 47.58 |
| Difference (B - A) | -11.64 |

With a categorical predictor, the intercept is the mean of the reference group (Lesson A), and the coefficient is the difference between the group means.

**Test of the lesson coefficient**
- H0: the mean quiz score is the same for Lesson A and Lesson B (difference = 0).
- H1: the mean quiz score is different for Lesson A and Lesson B.
- p-value: **0.00053**
- Conclusion: p < 0.05, so we reject H0. There is evidence that learners who took Lesson A score higher, by about 11.6 points on average. Lesson A seems to prepare learners better for this quiz.

## Summary

- Completing more content items is strongly linked with higher quiz scores: about +1.3 points per item.
- Lesson A learners score about 11.6 points higher on average than Lesson B learners.
- The assumptions of linear regression (linearity, normal residuals, equal spread) all look reasonable.
- The data is simulated and observational, so these results show links, not proof of cause.
- The last plot (`sns.lmplot` coloured by lesson) previews multiple regression, where `completed` and `lesson` would be used together in one model.

## Plots

Running the script saves these plots to the `plots/` folder:

1. Scatter plot of score vs completed
2. Scatter plot with the regression line
3. Histogram of residuals
4. Residuals vs fitted values
5. Boxplot of score by lesson
6. `lmplot` of score vs completed, coloured by lesson

## How to run

```bash
pip install -r requirements.txt
python codecademy_linear_regression.py
```

## Files

| File | Description |
|---|---|
| `codecademy_linear_regression.py` | Full analysis: models, assumption checks, tests and plots |
| `codecademy.csv` | Dataset (100 learners) |
| `requirements.txt` | Python packages needed |
