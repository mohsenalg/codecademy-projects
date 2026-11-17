# NBA Trends

Looking for associations between variables in historical NBA game data (2010 and 2014 seasons).

**What I did**
- Quantitative vs categorical: compared Knicks and Nets points with mean differences and overlapping histograms.
- Categorical vs categorical: built a contingency table of game location vs result and ran a chi-square test.
- Quantitative vs quantitative: found covariance and Pearson correlation between forecast win probability and point difference, with a scatter plot.

**Skills:** pandas, seaborn, SciPy (`chi2_contingency`, `pearsonr`), matplotlib.

Data: `nba_games.csv` (from Codecademy, based on FiveThirtyEight NBA Elo data).
