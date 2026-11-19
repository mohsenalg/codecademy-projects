import scipy.stats as stats
import numpy as np

### Task Group 1 ###
## Task 1:
# rate parameter (expected defects per day)
lam = 7

## Task 2:
# probability of exactly lam defects
print(stats.poisson.pmf(lam, lam))

## Task 3:
# probability of 4 or fewer defects (a very good day)
print(stats.poisson.cdf(4, lam))

## Task 4:
# probability of more than 9 defects (a bad day)
print(1 - stats.poisson.cdf(9, lam))


### Task Group 2 ###
## Task 5:
# simulate one year of daily defects
year_defects = stats.poisson.rvs(lam, size=365)

## Task 6:
print(year_defects[:20])

## Task 7:
# expected total defects in a year
print(lam * 365)

## Task 8:
# actual total in the simulated year
print(sum(year_defects))

## Task 9:
# simulated average per day (should be close to lam)
print(np.mean(year_defects))

## Task 10:
max_defects = max(year_defects)
print(max_defects)

## Task 11:
# probability of max_defects or more
print(1 - stats.poisson.cdf(max_defects - 1, lam))


### Extra ###
## Task 12:
# defects count at the 90th percentile
percentile_90 = stats.poisson.ppf(0.9, lam)
print(percentile_90)

## Task 13:
# share of simulated days at or above the 90th percentile (expect about 10%)
print(sum(year_defects >= percentile_90) / len(year_defects))
