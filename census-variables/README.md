# Census Variables

Checking and fixing variable types in a small census dataset.

**What I did**
- Inspected column data types with `head()`, `info()` and `dtypes`.
- Cleaned `birth_year` (replaced the text value `missing`), converted it to `int` and found the mean.
- Turned `higher_tax` into an ordered category, then label encoded it with `cat.codes` and found the median.
- One-hot encoded `marital_status` with `pd.get_dummies`.

**Skills:** pandas, variable types, ordinal and nominal encoding.

Dataset: `census_data.csv` from Codecademy (not included here).
