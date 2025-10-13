import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("matches_1930_2022.csv")
dfwc = pd.read_csv("world_cup.csv")
### Preparing columns for data analysis : ###

## 1.1 Making small letters of columns: ##
df.columns = [col.lower() for col in df.columns]
dfwc.columns = [col.lower() for col in dfwc.columns]


### 1.2. Deleting unnecessary columns ###
cols = [3,4,6,7,8,9,10,11,13,14,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
df.drop(df.columns[cols], axis=1, inplace=True)

## 1.3. Making column "date" in DATE-format ##
df["date"] = pd.to_datetime(df["date"])

## 1.4 Checking duplicate columns ##
print(f"Duplicates amount: {df.duplicated().sum()}")



## Basic statistics: ##
print(f"\n1st World Cup was in {df.year.min()}.\n The last World Cup was in {df.year.max()}.")
print(f"\nMatches played on all WC: {dfwc.matches.sum()}")


home_team_played = df["home_team"].value_counts()
away_team_played = df["away_team"].value_counts()
team_played = (home_team_played + away_team_played).sort_values(ascending=False).dropna()

plt.figure(figsize=(12, 6))
sns.barplot(x=team_played.index, y=team_played.values, hue = team_played.index, palette = "Set2", legend = False)
plt.xticks(rotation=45)
plt.xlim(0,20)
plt.xlabel("Teams")
plt.ylabel("Games played on all WC")
plt.title("Top 20 teams with most played games on WC")
plt.tight_layout()
plt.grid(True)
plt.show()



