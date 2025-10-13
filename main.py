import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("matches_1930_2022.csv")

# df.info()

### Preparing columns for data analysis : ###
## 1.1 Making small letters: ##
df.columns = [col.lower() for col in df.columns]
# df.info()

### 1.2. Deleting unnecessary columns ###
cols = [3,4,6,7,8,9,10,11,13,14,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
df.drop(df.columns[cols], axis=1, inplace=True)

## 1.3. Making "date" as DATE ##



