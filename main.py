# =============================================================================
# === 1. LIBRARY IMPORTS ===
# =============================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# === 2. DATA LOADING & PREPARATION ===
# =============================================================================
# Load the dataset
df = pd.read_csv("matches_1930_2022.csv")
dfwc = pd.read_csv("world_cup.csv")

# --- Data Cleaning & Transformation ---
# Standardizing column names to a consistent style (lowercase) ---
df.columns = [col.lower() for col in df.columns]
dfwc.columns = [col.lower() for col in dfwc.columns]

# Deleting unnecessary columns
cols = [3,4,6,7,8,9,10,11,13,14,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
df.drop(df.columns[cols], axis=1, inplace=True)

# Converting column "date" to datetime-format
df["date"] = pd.to_datetime(df["date"])

# Checking duplicates
print(f"Duplicates amount: {df.duplicated().sum()}")

# Replacing team names
df.replace("West Germany", "Germany", inplace=True)
dfwc.replace("West Germany", "Germany", inplace=True)

# ==================================================================================
# === 2. EXPLORATORY DATA ANALYSIS (EDA) ===
# ==================================================================================
# --- Providing basic statistics
# The date of the first and last WC
print(f"\n1st World Cup was in {df.year.min()}.\n The last World Cup was in {df.year.max()}.")

# The number of games played during all WC
print(f"\nMatches played on all WC: {dfwc.matches.sum()}")

# --- TOP20 team on WC
# Creating df of Top20 teams, which played most of games on WC
home_team_played = df["home_team"].value_counts()
away_team_played = df["away_team"].value_counts()
team_played = (home_team_played + away_team_played).sort_values(ascending=False).dropna()
top20_teams = team_played.head(20)

# Visualization of Top20 teams
plt.figure(figsize=(12, 7))
ax = sns.barplot(x=top20_teams.index, y=top20_teams.values, hue = top20_teams.index, palette = "Set2", legend = False)

for container in ax.containers:
    ax.bar_label(container, fontsize=10)

plt.xticks(rotation=45, ha = "right")
plt.xlabel("Teams")
plt.ylabel("Games played on all WC")
plt.title("Top 20 teams with most played games on WC")
plt.tight_layout()
plt.grid(True, axis = "y", linestyle = "--")
plt.show()

# --- Medalists on ALL WC
# Renaming values for better analysis
dfwc.rename(columns ={"champion": "gold", "runner-up": "silver"}, inplace = True)

# Creating the list of "bronze" teams
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

# Merging two tables
world_cup_full = pd.merge(
    dfwc,
    third_place_df,
    how = "left",
    on = "year")

# Sorting, counting and renaming values of Medalists
gold_winners = world_cup_full["gold"].value_counts().rename("Gold")
silver_winners = world_cup_full["silver"].value_counts().rename("Silver")
bronze_winners = world_cup_full["bronze"].value_counts().rename("Bronze")

# Creating df of all medalists on WC
medalists_df = (pd.concat([gold_winners, silver_winners, bronze_winners], axis=1)).reset_index()
medalists_df.fillna(0, inplace=True)

# Turning "wide" sheet to "long" sheet
medalists_df = pd.melt(medalists_df, id_vars = ["index"], value_vars = ["Gold", "Silver", "Bronze"], var_name= "Medal", value_name = "Amount", ignore_index=False)

# Visualization of all WC medalists

plt.figure(figsize=(12, 7))
medal_colors = {
    "Gold": "#FFD700",
    "Silver": "#C0C0C0",
    "Bronze": "#CD7F32"}
sns.barplot(data = medalists_df, x = "index", y = "Amount", hue = "Medal", palette = medal_colors )
plt.xticks(rotation=45, ha = "right")
plt.xlabel("Teams")
plt.ylabel("Medals count")
plt.title("All teams, which have medals")
plt.tight_layout()
plt.grid(True, axis = "y", linestyle = "dashdot")
plt.show()

# --- AVG attendance on all WC
# Sorting values by year

dfwc_sorted = dfwc.sort_values(by="year")

# Creating new column of WC host and year
dfwc_sorted["host_year"] = dfwc_sorted["host"] + " " + dfwc_sorted["year"].astype(str)

# Visulization of AVG attendance
plt.figure(figsize=(10, 5))
sns.lineplot(data = dfwc_sorted, x = dfwc_sorted["host_year"], y = dfwc_sorted["attendanceavg"], color = "red")
plt.xticks(rotation=30, ha = "right")
plt.yticks(np.arange(0, dfwc_sorted['attendanceavg'].max() + 5000, 5000))
plt.xlabel("Host and year")
plt.ylabel("Average attendance")
plt.title("All countries, which were host of WC")
plt.tight_layout()
plt.grid(True, axis = "y", linestyle = "--")
plt.show()

## Concept 1: Evolution of football in time
# I assume that the game style has changed, become more pragmatic and defensive.
# H1 : The average number of goals per game at the World Cup is decreasing over time (years).
#     * Group all matches by year (Year).
#     * For each year we calculate the average number of goals per game.
#     * Plot a line to see the trend.

df["total_goals"] = df["home_score"] + df["away_score"]

avg_goals_per_year = df.groupby("year")["total_goals"].mean()
avg_goals_df = avg_goals_per_year.reset_index()

# plt.figure(figsize=(10, 5))
# ax = sns.lineplot(data=avg_goals_df, x= "year", y = "total_goals")
# ## making eras
# ax.axvspan(1930, 1978, color='green', alpha=0.1, label='13-16 teams')
# ax.axvspan(1982, 1994, color='blue', alpha=0.1, label='24 teams')
# ax.axvspan(1998, 2022, color='red', alpha=0.1, label='32 teams')
#
# for index, row in avg_goals_df.iterrows():
#     label = f"{row['total_goals']:.2f}"
#     ax.text(
#         row['year'],
#         row['total_goals'],
#         label,
#         ha='center',
#         va='bottom',
#         fontsize=9,
#         zorder=10
#     )
#
min_year = df["year"].min()
max_year = df["year"].max()
# plt.xticks(np.arange(min_year,max_year + 4,4), rotation=30, ha = "right")

# plt.xlabel("Year")
# plt.ylabel("Average goals")
# plt.title("Average goals per year")
# plt.grid(True, axis = "y", linestyle = "dashed")
# plt.legend()
# plt.tight_layout()
# plt.show()

# I wouldn’t say that goals amount decreased. over time.
# Of course, in the general picture - you can see that the number of heads has decreased:
# From the beginning of the FIFA World Cup 1930 until 1958, the average number of goals was in the range of 3.6 - 5.38, and from 1962 to 2022 in the range of 2.21 - 2.97.
# But, we must also look at the periods when the number of teams was different:
# With 13-16 teams - the number of goals dropped noticeably (1930-1962). The teams became more defensive.
# With 24 teams - 1982 until 1990 the average number of goals fell to the lowest point. But then it became higher.
# With 32 teams - from 1998 to 2010 the average number of goals decreased by a little, but from 2014 to 2022 - is about the same level.
# Anomalous goals amount were the year 1954. Extremely low goals were 1990
# I would say that at the very beginning of an era, people definitely played more attack style (or were worse in defense ?: )) 
# But then, over time, it seems to me that the number of goals is about the same. I mean - my hypothesis was not confirmed.

## H2 A: The finalists (1-3 places) averagely score more goals per game than 'other' teams.
## H3 B: The finalists (1-3 places) averagely conceded less goals per game than "other" teams.

## creating medalists list
yearly_medalist_team = pd.melt(world_cup_full, id_vars = ["year"], value_vars = ["gold", "silver", "bronze"], var_name = "medal_type", value_name = "team")
yearly_medalist_team.dropna(inplace=True)

## sorting and creating new df with home team statistic and away team statistic
df_home = df[["year","home_team","home_score", "away_score"]]
df_home = df_home.rename(columns = {
    "home_team": "team",
    "home_score": "goals_scored",
    "away_score": "goals_conceded"
})

df_away = df[["year","away_team","away_score", "home_score"]]
df_away = df_away.rename(columns = {
    "away_team": "team",
    "away_score": "goals_scored",
    "home_score": "goals_conceded"
})
all_games_df = pd.concat([df_home, df_away])

merged_df = pd.merge(
    all_games_df,
    yearly_medalist_team,
    on = ["year", "team"],
    how = "left")

merged_df["is_medalist"] = merged_df["medal_type"].notna()
# alternative
# merged_df['is_medalist'] = np.where(
#     merged_df['medal_type'].isnull(),
#     False,
#     True


## grouping the results

grouped_all_games = merged_df.groupby(["year","is_medalist"]).mean(["goals_scored", "goals_conceded"])
print(grouped_all_games)

## visualization

final_comparison_df = grouped_all_games.reset_index()

fig, axes = plt.subplots(1,2,figsize=(18,7), sharey=True)

sns.lineplot(data=final_comparison_df, x = "year", y = "goals_scored", hue = "is_medalist", palette = "Set1", ax = axes[0], marker = "o")
axes[0].set_title("Average Goals Scored Per Game")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Average Goals")
axes[0].grid(True,linestyle = "dotted")

sns.lineplot(data=final_comparison_df, x = "year", y = "goals_conceded", hue = "is_medalist", palette = "Set2", ax = axes[1], marker = "o")
axes[1].set_title("Average Goals Conceded Per Game")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("")
axes[1].grid(True,linestyle = "dotted")

plt.suptitle("Champion\s Profile: Goals Scored vs Goals Conceded (Medalists vs Others)", fontsize = 16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()

This project is about evolution of footbal and analysis of success factors on WC from 1930 to 2022.

According data of all played matches I have checked two main hypotesis -

H1: the game style has changed, become more pragmatic and defensive.
The average number of goals per game at the World Cup was decreasing over time (years).
Findout that there is no corelation between years and goals amount.
At the very beginning of era, countries definitely played more attack style.
But, over time, team started play more tacktical, respnsible and from 1962 teams were scoring mostly same amount of goals till now.

H2.A: The finalists (1-3 places) averagely scored more goals per game than 'other' teams.
Additionally, I have checked H3 B: The finalists (1-3 places) averagely conceded less goals per game than "other" teams.
I can strongly confirm, that there is a huge differrence between medalists and other teams.
Teams who scored more goals and conceded less goals most probably will be on pedistal.

Overall, the analysis showed that the football become more pragmatic, strategic, but on the other hand - if you want to fight for a medals - score more, concede less - and you have huge chances to be on a top.












