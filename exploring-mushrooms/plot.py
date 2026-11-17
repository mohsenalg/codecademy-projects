import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import codecademylib3

# load in the data
df = pd.read_csv("mushroom_data.csv")
print(df.head())

# list of all column headers
columns = df.columns.tolist()
print(df.info())

for col in columns:
  sns.countplot(x=col, order= df[col].value_counts().index, data=df)
  plt.xticks(rotation=30, fontsize=10)
  plt.title(col + " Value Counts")
  plt.show()
  plt.clf()
