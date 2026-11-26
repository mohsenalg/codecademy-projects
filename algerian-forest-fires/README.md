# Algerian Forest Fires

Multiple linear regression project from the Codecademy **Master Statistics with Python** skill path (Linear Regression: Multiple Linear Regression).

## Goal

Use weather and fire-risk data from Algerian forests to practise **multiple linear regression**:

1. Predict **relative humidity** from temperature and region (a quantitative and a binary predictor).
2. Predict the **Fine Fuel Moisture Code (FFMC)** from temperature and fire status, with an **interaction term**.
3. Predict **FFMC** from humidity with a **polynomial (squared) term**.
4. Explore FFMC from all its weather inputs, and the **Fire Weather Index (FWI)** from ISI and BUI.

## Data

`forests.csv` has 243 days of observations (122 in Bejaia, 121 in Sidi Bel-abbes; a fire happened on 137 of them) and 12 columns:

| Column | Meaning |
|---|---|
| `temp` | Maximum temperature (°C) |
| `humid` | Relative humidity (%) |
| `wind` | Wind speed (km/h) |
| `rain` | Rain (mm) |
| `FFMC` | Fine Fuel Moisture Code: dryness of fine forest litter (higher = drier) |
| `DMC` | Duff Moisture Code |
| `DC` | Drought Code |
| `ISI` | Initial Spread Index: how fast a fire could spread |
| `BUI` | Buildup Index: how much fuel is available to burn |
| `FWI` | Fire Weather Index: overall fire intensity potential (uses ISI and BUI) |
| `region` | `Bejaia` (northeast Algeria) or `Sidi Bel-abbes` (northwest Algeria) |
| `fire` | `True` if a fire occurred, `False` if not |

**Source:** [UCI Machine Learning Repository: Algerian Forest Fires](https://archive.ics.uci.edu/dataset/547/algerian+forest+fires+dataset), a subset cleaned by Codecademy.
Citation: Faroudja ABID et al., *Predicting Forest Fire in Algeria using Data Mining Techniques: Case Study of the Decision Tree Algorithm*, AI2SD 2019, Marrakech, Morocco.

## Results

### 1. Multicollinearity check

Multiple regression assumes the predictors are **not highly correlated with each other**. The heat map shows these pairs with correlation ≥ 0.8, so they should **not** be used together as predictors:

| Pair | Correlation |
|---|---|
| DMC and BUI | 0.98 |
| DC and BUI | 0.94 |
| ISI and FWI | 0.92 |
| DMC and DC | 0.88 |
| DMC and FWI | 0.88 |
| BUI and FWI | 0.86 |

`temp` and `humid` are also fairly correlated (-0.65).

### 2. Humidity from temperature and region

`humid ~ temp + region` (R² = 0.48)

| Term | Coefficient | p-value |
|---|---|---|
| Intercept | 142.58 | < 0.001 |
| `region[T.Sidi Bel-abbes]` | -7.25 | < 0.001 |
| `temp` | -2.39 | < 0.001 |

| Region | Equation |
|---|---|
| Bejaia | humid = 142.58 - 2.39 × temp |
| Sidi Bel-abbes | humid = 135.33 - 2.39 × temp |

- **temp:** with region held constant, each extra 1 °C is linked to **2.39 percentage points lower** humidity on average.
- **region:** both lines have the **same slope**, so they are parallel. At the same temperature, Sidi Bel-abbes is on average **7.25 points drier** than Bejaia.
- **Intercepts:** 142.58% and 135.33% are the predicted humidity at 0 °C. They are **not practical**: humidity cannot go above 100%, and the data only covers 22 to 42 °C.
- **Fit:** the lines follow the downward trend, but the points are widely spread around them, so the fit is only moderate.

### 3. FFMC from temperature and fire status (interaction)

`FFMC ~ temp + fire + temp:fire` (R² = 0.74)

| Term | Coefficient | p-value |
|---|---|---|
| Intercept | -8.11 | 0.212 |
| `fire[T.True]` | 76.79 | < 0.001 |
| `temp` | 2.45 | < 0.001 |
| `temp:fire[T.True]` | -1.89 | < 0.001 |

| Group | Equation |
|---|---|
| No fire | FFMC = -8.11 + 2.45 × temp |
| Fire | FFMC = 68.68 + 0.56 × temp |

- The interaction term lets each group have its **own slope**. The lines have different intercepts **and** different slopes.
- **No fire:** each extra 1 °C is linked to **2.45 more** FFMC points on average.
- **Fire:** each extra 1 °C is linked to only **0.56 more** FFMC points on average.
- Where a fire happened, the fuel was already very dry (FFMC is high at every temperature), so temperature changes it much less. Where no fire happened, fuel dryness depends much more on temperature.
- The interaction is significant (p < 0.001), and two lines with different slopes fit the data much better than two parallel lines.

### 4. FFMC from humidity (polynomial)

`FFMC ~ humid + humid²` (R² = 0.46, compared with 0.42 for a straight line)

FFMC = 77.63 + 0.752 × humid - 0.0114 × humid²

| Humidity | Predicted FFMC |
|---|---|
| 25% | 89.30 |
| 35% | 89.97 |
| 60% | 81.65 |
| 70% | 74.33 |

- The coefficient on `humid` **cannot be read on its own**: humidity is in two terms, so we cannot change `humid` while keeping `humid²` the same.
- From 25% to 35% humidity, FFMC barely changes (+0.67). From 60% to 70%, it drops by **7.32**. The same 10-point rise in humidity matters much more when the air is already humid.
- **Meaning:** fuel stays very dry while humidity is low, peaks at about **33% humidity**, and then gets wetter faster and faster as humidity rises.
- A straight line would say every 1% of humidity lowers FFMC by the same amount. It misses the flat part at low humidity and the steep drop at high humidity.

### 5. Exploring other variables

`FFMC ~ humid + temp + wind + rain` (R² = 0.65)

FFMC = 50.46 - 0.35 × humid + 1.38 × temp + 0.42 × wind - 2.61 × rain

- Higher temperature goes with **drier** fuel (higher FFMC); more humidity and more rain go with **wetter** fuel (lower FFMC). All four predictors are significant (wind is the weakest, p = 0.042).
- To decide on **interaction terms**, plot FFMC against each predictor, coloured by another predictor, and look for lines with different slopes. Then add the interaction and check whether its coefficient is significant and R² improves.

`FWI ~ ISI + BUI` (R² = 0.97)

FWI = -2.27 + 1.13 × ISI + 0.24 × BUI

- Both coefficients are **positive**, as expected: higher spread potential and more available fuel mean higher fire intensity.
- The two predictors explain 97% of the variation in FWI, which makes sense because FWI is calculated from ISI and BUI.
- ISI and BUI are correlated (0.64), so their separate effects are not fully independent.

## Summary

- Higher temperature goes with lower humidity in both regions; Sidi Bel-abbes is consistently drier.
- Temperature affects fuel dryness (FFMC) much more on days **without** a fire; on fire days the fuel is already dry.
- Humidity has a **curved** link with FFMC: little effect at low humidity, a strong effect at high humidity.
- The data is observational, so these results show **associations, not causes**.

## Plots

Running the script saves these plots to the `plots/` folder:

1. Correlation heat map
2. Humidity vs temperature, coloured by region
3. Humidity vs temperature with one regression line per region
4. FFMC vs temperature, coloured by fire status
5. FFMC vs temperature with one regression line per fire group
6. FFMC vs humidity
7. FFMC vs humidity with the straight line and the polynomial curve

## How to run

```bash
pip install -r requirements.txt
python algerian_forest_fires.py
```

## Files

| File | Description |
|---|---|
| `algerian_forest_fires.py` | Full analysis: correlations, models, equations, predictions and plots |
| `forests.csv` | Dataset (243 observations) |
| `requirements.txt` | Python packages needed |
