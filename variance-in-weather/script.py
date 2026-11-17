import codecademylib3_seaborn
import pandas as pd
import numpy as np
from weather_data import london_data

print(london_data.iloc[100:200])
print(len(london_data))
temp = london_data['TemperatureC']
print(temp.head(50))
average_temp = sum(temp) / len(temp)
print(average_temp)
temperature_var = np.var(temp)
print(temperature_var)
print(temperature_var ** 0.5)
print(london_data.head())

june = london_data.loc[london_data['month'] == 6]['TemperatureC']
print(june)
july = london_data.loc[london_data['month'] == 7]['TemperatureC']
print(july)
print(f'mean tempreture in June: {np.mean(june)}')
print(f'mean tempreture in july: {np.mean(july)}')
print(f'std for jun: {np.std(june)}')
print(f'std for july: {np.std(july)}')
for i in range(1, 13):
  month = london_data.loc[london_data["month"] == i]["TemperatureC"]
  print("The mean temperature in month "+str(i) +" is "+ str(np.mean(month)))
  print("The standard deviation of temperature in month "+str(i) +" is "+ str(np.std(month)) +"\n")

import numpy as np
from matplotlib import pyplot as plt

# Each group = 3 months
groups = {
    "Jan-Mar": [1, 2, 3],
    "Apr-Jun": [4, 5, 6],
    "Jul-Sep": [7, 8, 9],
    "Oct-Dec": [10, 11, 12],
}

labels = []
group_means = []

for name, months in groups.items():
    # Keep only rows where the month is in this group
    temps = london_data.loc[london_data["month"].isin(months)]["TemperatureC"]
    labels.append(name)
    group_means.append(np.mean(temps))

positions = range(len(labels))
plt.bar(positions, group_means)
plt.xticks(positions, labels)
plt.xlabel("Months")
plt.ylabel("Average Temperature (°C)")
plt.title("London Average Temperature Every 3 Months (2015)")
plt.show()
