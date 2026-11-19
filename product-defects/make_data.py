"""Create year_defects.csv: one simulated year of daily defect counts from Poisson(7).

A fixed seed makes the file reproducible. Run: python make_data.py
"""
import csv

import scipy.stats as stats

LAM = 7
DAYS = 365
SEED = 42

year_defects = stats.poisson.rvs(LAM, size=DAYS, random_state=SEED)

with open("year_defects.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["day", "defects"])
    for day, defects in enumerate(year_defects, start=1):
        writer.writerow([day, int(defects)])
