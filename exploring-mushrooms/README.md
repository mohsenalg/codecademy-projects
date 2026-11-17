# Exploring Mushrooms

Bar charts for every variable in the UCI mushroom dataset (23 categorical columns, 8,124 mushrooms).

**What I did**
- Looped over every column and drew a `seaborn.countplot` for each one.
- Ordered bars from most to least common with `df[col].value_counts().index`.
- Rotated x labels so long category names do not overlap, and added a title per chart.

**Skills:** pandas, seaborn, matplotlib, bar charts for categorical data.

Data: `mushroom_data.csv` (Codecademy version of the [UCI Mushroom dataset](https://archive.ics.uci.edu/dataset/73/mushroom)).
