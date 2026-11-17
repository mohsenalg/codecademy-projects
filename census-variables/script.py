import codecademylib3
import pandas as pd

# ============================================================
# Load data
# ============================================================
census = pd.read_csv('census_data.csv', index_col=0)


# ============================================================
# Tasks 1-3: Assess variable types
# ============================================================
# First five rows
print(census.head())

# Column summary: non-null counts and dtypes
census.info()

# Dtype of each column
print(census.dtypes)


# ============================================================
# Tasks 4-7: Clean birth_year and find the average
# ============================================================
# Unique values show one text value: 'missing'
print(census['birth_year'].unique())

# Replace 'missing' with the researched birth year
census['birth_year'] = census['birth_year'].replace('missing', 1967)

# Check that 'missing' is gone
print(census['birth_year'].unique())

# Convert birth_year from str to int
census['birth_year'] = census['birth_year'].astype('int')
print(census.dtypes)

# Average birth year
print(f"Mean birth_year: {census['birth_year'].mean()}")


# ============================================================
# Task 8: Make higher_tax an ordered category
# ============================================================
print(f"higher_tax values before: {census['higher_tax'].unique()}")

tax_order = ['strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree']
census['higher_tax'] = pd.Categorical(census['higher_tax'], tax_order, ordered=True)

# Shows the categories with their order (<)
print(census['higher_tax'].unique())


# ============================================================
# Task 9: Label encode higher_tax and find the median
# ============================================================
# cat.codes turns each category into its position: 0 to 4
census['higher_tax'] = census['higher_tax'].cat.codes

print(f"Median higher_tax: {census['higher_tax'].median()}")


# ============================================================
# Task 10: One-hot encode marital_status
# ============================================================
# One new 0/1 column per marital status
census = pd.get_dummies(census, columns=['marital_status'], dtype=int)

print(census.head())
