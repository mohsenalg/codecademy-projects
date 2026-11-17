import numpy as np
import pandas as pd
from scipy.stats import pearsonr, chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

import codecademylib3
np.set_printoptions(suppress=True, precision = 2)
nba = pd.read_csv('./nba_games.csv')

# Subset data to 2010 and 2014 seasons
nba_2010 = nba[nba.year_id == 2010]
nba_2014 = nba[nba.year_id == 2014]

print(nba_2010.head())
print(nba_2014.head())

# Points for Knicks and Nets in 2010
knicks_pts_10 = nba_2010.pts[nba_2010.fran_id == 'Knicks']
nets_pts_10 = nba_2010.pts[nba_2010.fran_id == 'Nets']

# Difference in mean points
diff_means_2010 = knicks_pts_10.mean() - nets_pts_10.mean()
print(diff_means_2010)
#Histogram
sns.histplot(knicks_pts_10, color='blue', label='knick', stat='density', alpha=0.5)
sns.histplot(nets_pts_10, color='green', label='nets', stat='density', alpha=0.5)
plt.legend()
plt.show()

knicks_pts_2014 = nba_2014.pts[nba_2014.fran_id == 'Knicks']
nets_pts_2014 = nba_2014.pts[nba_2014.fran_id == 'Nets']
diff_means_2014 = knicks_pts_2014.mean() - nets_pts_2014.mean()
print(diff_means_2014)

plt.clf()
sns.histplot(knicks_pts_2014, color='blue', label='Knicks', stat='density', alpha=0.5)
sns.histplot(nets_pts_2014, color='red', label='Nets', stat='density', alpha=0.5)
plt.legend()
plt.title('2014 Season')
plt.show()


location_result_freq = pd.crosstab(nba_2010.game_location, nba_2010.game_result)
print(location_result_freq)

location_result_proportions =(location_result_freq/len(nba_2010))
print(location_result_proportions)

chi2, p, dof, expected = chi2_contingency(location_result_freq)
print(chi2, p)
print(expected)

point_diff_forecast_cov = np.cov(nba_2010.forecast, nba_2010.point_diff)
print(point_diff_forecast_cov)

point_diff_forecast_corr, p = pearsonr(nba_2010.forecast, nba_2010.point_diff)
print(point_diff_forecast_corr)

plt.clf()
plt.scatter(nba_2010.forecast, nba_2010.point_diff)
plt.xlabel('forcast')
plt.ylabel('point_diff')
plt.show()
