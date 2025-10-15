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
# === 3.0. EXPLORATORY DATA ANALYSIS (EDA) ===
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
third_place_round = "Third-place match"
third_place_matches = df[df["round"] == "third_place_round"]
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
plt.title("All countries, which were host of WC and average attendance")
plt.tight_layout()
plt.grid(True, axis = "y", linestyle = "--")
plt.show()

# ==================================================================================
# === 3.1. CHECKING THE HYPOTHESIS ===
# ==================================================================================
# --- Hypothesis 1: The average number of goals per game at the World Cup is decreasing over time? ---

# Creating new column of all goals on WC and grouping
df["total_goals"] = df["home_score"] + df["away_score"]
avg_goals_per_year = df.groupby("year")["total_goals"].mean()
avg_goals_df = avg_goals_per_year.reset_index()

# Visualization of all goals on all WC
plt.figure(figsize=(10, 5))
ax = sns.lineplot(data=avg_goals_df, x= "year", y = "total_goals")
# Creating "Eras"
ax.axvspan(1930, 1978, color='green', alpha=0.1, label='13-16 teams')
ax.axvspan(1982, 1994, color='blue', alpha=0.1, label='24 teams')
ax.axvspan(1998, 2022, color='red', alpha=0.1, label='32 teams')

for index, row in avg_goals_df.iterrows():
    label = f"{row['total_goals']:.2f}"
    ax.text(
        row['year'],
        row['total_goals'],
        label,
        ha='center',
        va='bottom',
        fontsize=9,
        zorder=10
    )

min_year = df["year"].min()
max_year = df["year"].max()
plt.xticks(np.arange(min_year,max_year + 4,4), rotation=30, ha = "right")

plt.xlabel("Year")
plt.ylabel("Average goals")
plt.title("Average goals per year")
plt.grid(True, axis = "y", linestyle = "dashed")
plt.legend()
plt.tight_layout()
plt.show()

# --- Hypothesis 2.1: The finalists (1-3 places) averagely score more goals per game than "other" teams ? ---
# --- Hypothesis 2.2: The finalists (1-3 places) averagely conceded less goals per game than "other" teams ? ---

# Creating all medalists list by year
yearly_medalist_team = pd.melt(world_cup_full, id_vars = ["year"], value_vars = ["gold", "silver", "bronze"], var_name = "medal_type", value_name = "team")
yearly_medalist_team.dropna(inplace=True)

# Sorting and creating new tables with "home team" statistic and "away team" statistic
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

# Combing home and away tables
all_games_df = pd.concat([df_home, df_away])

# Merging yearly_medalist table with all_games table
merged_df = pd.merge(
    all_games_df,
    yearly_medalist_team,
    on = ["year", "team"],
    how = "left")

# Creating a new section (boolean type), which shows if a team is a medalist on WC
merged_df["is_medalist"] = merged_df["medal_type"].notna()

# alternative
# merged_df['is_medalist'] = np.where(
#     merged_df['medal_type'].isnull(),
#     False,
#     True

# Grouping the results of merged_df
grouped_all_games = merged_df.groupby(["year","is_medalist"]).mean(["goals_scored", "goals_conceded"])

# Visualization of results
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

plt.suptitle("Champions Profile: Goals Scored vs Goals Conceded (Medalists vs Others)", fontsize = 16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
