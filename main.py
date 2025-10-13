import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("matches_1930_2022.csv")

# df.info()

df.columns = [col.lower() for col in df.columns]
# df.info()

cols = [3,6,8,9,10,11,18,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
df.drop(df.columns[cols], axis=1, inplace=True)

df.info()


