import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# NBA API URL (or scrape source)
NBA_API_URL = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"

# Function to pull NBA player stats (for this example, we will scrape the data)
@st.cache
def get_nba_data():
    # Read the stats table from the website
    dfs = pd.read_html(NBA_API_URL)  # Scrapes all tables from the page
    
    # Inspect the first table
    player_data = dfs[0]
    
    # Filter relevant columns based on actual data
    player_data = player_data[['Rk', 'Player', 'Team', 'G', 'MP', 'PTS']]  # Filter relevant columns

    # Clean up the data
    player_data.columns = ['Rank', 'Player', 'Team', 'Games Played', 'Minutes Per Game', 'Points Per Game']

    # Remove rows with missing data
    player_data = player_data.dropna()

    # Remove players with fewer than 50 games played
    player_data = player_data[player_data['Games Played'] >= 50]

    # Convert columns to numeric
    player_data['Minutes Per Game'] = pd.to_numeric(player_data['Minutes Per Game'])
    player_data['Points Per Game'] = pd.to_numeric(player_data['Points Per Game'])
    player_data['Games Played'] = pd.to_numeric(player_data['Games Played'])

    return player_data

# Pull the data
nba_data = get_nba_data()

# Streamlit UI
st.title("NBA Player Performance Analysis (2024 Season)")

# Sidebar filters
st.sidebar.title("Filters")
min_games = st.sidebar.slider('Minimum Games Played', min_value=50, max_value=100, value=50, step=10)
filtered_data = nba_data[nba_data['Games Played'] >= min_games]

# Show a table with filtered data
st.subheader(f"Showing players with more than {min_games} games played")
st.dataframe(filtered_data)

# Scatter Plot of Minutes Played vs Points Per Game
st.subheader("Scatter Plot: Minutes Played vs Points Per Game")
scatter_fig, scatter_ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='Minutes Per Game', y='Points Per Game', hue='Team', palette='tab20', alpha=0.7, ax=scatter_ax)
scatter_ax.set_title('NBA Player Performance: Minutes Played vs Points Per Game (2024 Season)')
scatter_ax.set_xlabel('Minutes Played per Game')
scatter_ax.set_ylabel('Points Per Game')
scatter_ax.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(scatter_fig)

# Histogram of Minutes Played
st.subheader("Histogram: Distribution of Minutes Played per Game")
hist_fig, hist_ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['Minutes Per Game'], kde=True, color='blue', bins=30, ax=hist_ax)
hist_ax.set_title('Distribution of Minutes Played per Game (2024 Season)')
hist_ax.set_xlabel('Minutes Played per Game')
hist_ax.set_ylabel('Frequency')
st.pyplot(hist_fig)

# Histogram of Points Per Game
st.subheader("Histogram: Distribution of Points Per Game")
ppg_hist_fig, ppg_hist_ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['Points Per Game'], kde=True, color='green', bins=30, ax=ppg_hist_ax)
ppg_hist_ax.set_title('Distribution of Points Per Game (2024 Season)')
ppg_hist_ax.set_xlabel('Points Per Game')
ppg_hist_ax.set_ylabel('Frequency')
st.pyplot(ppg_hist_fig)

# Box Plot of Points Per Game by Team
st.subheader("Box Plot: Points Per Game by Team")
box_fig, box_ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=filtered_data, x='Team', y='Points Per Game', ax=box_ax)
box_ax.set_xticklabels(box_ax.get_xticklabels(), rotation=90)
box_ax.set_title('Distribution of Points Per Game by Team (2024 Season)')
box_ax.set_xlabel('Team')
box_ax.set_ylabel('Points Per Game')
st.pyplot(box_fig)

# Correlation Heatmap (Minutes vs PPG)
st.subheader("Correlation Heatmap: Minutes Played vs Points Per Game")
corr_fig, corr_ax = plt.subplots(figsize=(8, 6))
corr = filtered_data[['Minutes Per Game', 'Points Per Game']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=corr_ax)
corr_ax.set_title('Correlation between Minutes Played and Points Per Game')
st.pyplot(corr_fig)

# Optionally add more visualizations or interactivity (e.g., dropdowns, sliders)
