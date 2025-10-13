import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

## 1.5 Renaming West-Geremany to Germany
df.replace("West Germany", "Germany", inplace=True)

## Basic statistics: ##
print(f"\n1st World Cup was in {df.year.min()}.\n The last World Cup was in {df.year.max()}.")
print(f"\nMatches played on all WC: {dfwc.matches.sum()}")

## creating top20 teams, which played most of games on WC
home_team_played = df["home_team"].value_counts()
away_team_played = df["away_team"].value_counts()
team_played = (home_team_played + away_team_played).sort_values(ascending=False).dropna()
top20_teams = team_played.head(20)

## creating visualization
# plt.figure(figsize=(12, 7))
# ax = sns.barplot(x=top20_teams.index, y=top20_teams.values, hue = top20_teams.index, palette = "Set2", legend = False)
#
# for container in ax.containers:
#     ax.bar_label(container, fontsize=10)

# plt.xticks(rotation=45, ha = "right")
# plt.xlabel("Teams")
# plt.ylabel("Games played on all WC")
# plt.title("Top 20 teams with most played games on WC")
# plt.tight_layout()
# plt.grid(True, axis = "y", linestyle = "--")
# plt.show()

## renaming values for better analysis
dfwc.rename(columns ={"champion": "gold", "runner-up": "silver"}, inplace = True)

## creating the list of "bronze"
third_place_matches = df[df["round"] == "Third-place match"]
third_place = np.where(
    third_place_matches["home_score"] > third_place_matches["away_score"],
    third_place_matches["home_team"],
    third_place_matches["away_team"]
)
third_place_year = third_place_matches["year"]
third_place_df = pd.DataFrame({
    "year": third_place_year,
    "bronze": third_place
})

world_cup_full = pd.merge(
    dfwc,
    third_place_df,
    how = "left",
    on = "year")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

gold_winners = world_cup_full["gold"].value_counts().rename("gold")
silver_winners = world_cup_full["silver"].value_counts().rename("silver")
bronze_winners = world_cup_full["bronze"].value_counts().rename("bronze")

medalists_df = pd.concat([gold_winners, silver_winners, bronze_winners], axis=1)
medalists_df.fillna(0, inplace=True)
print(f"\n{medalists_df}")

## visualization of all medalists

# plt.figure(figsize=(12, 7))
# sns.countplot(data = world_cup_full, x = "gold")
# sns.countplot(data = world_cup_full, x = "silver")
# sns.countplot(data = world_cup_full, x = "bronze")
# plt.xticks(rotation=45, ha = "right")
# plt.show()







