import codecademylib3_seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("country_data.csv")

# Task 1: look at the first 5 rows (comment out after you see it)
# print(data.head())

# Task 2: life expectancy column
life_expectancy = data["Life Expectancy"]

# Task 3: quartiles of life expectancy
life_expectancy_quartiles = np.quantile(life_expectancy, [0.25, 0.5, 0.75])
print(life_expectancy_quartiles)

# Task 4: histogram of all countries (removed in task 11)
# plt.hist(life_expectancy)
# plt.show()

# Task 6: GDP column
gdp = data["GDP"]

# Task 7: median GDP
median_gdp = np.quantile(gdp, 0.5)
print(median_gdp)

# Task 8: split rows into low and high GDP countries
low_gdp = data[data["GDP"] <= median_gdp]
high_gdp = data[data["GDP"] > median_gdp]

# Task 9: quartiles of life expectancy for low GDP countries
low_gdp_quartiles = np.quantile(low_gdp["Life Expectancy"], [0.25, 0.5, 0.75])
print(low_gdp_quartiles)

# Task 10: quartiles of life expectancy for high GDP countries
high_gdp_quartiles = np.quantile(high_gdp["Life Expectancy"], [0.25, 0.5, 0.75])
print(high_gdp_quartiles)

# Task 11: compare both groups in one histogram
plt.hist(high_gdp["Life Expectancy"], alpha = 0.5, label = "High GDP")
plt.hist(low_gdp["Life Expectancy"], alpha = 0.5, label = "Low GDP")
plt.legend()
plt.show()
