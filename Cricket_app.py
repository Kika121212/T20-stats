import streamlit as st
import pandas as pd

# Load the dataset
file_path = "T20 staats.csv.xlsx"  # Update with your file path
df = pd.read_excel(file_path, sheet_name="Sheet1")

# Batting Stats Calculation
batting_stats = df.groupby("Striker").agg(
    Runs_Scored=("Batter Runs", "sum"),
    Balls_Faced=("Batter Balls", "sum"),
    High_Score=("Batter Runs", "max"),
    Dismissals=("Dismissed player", "count")
).reset_index()

batting_stats["Average"] = batting_stats.apply(
    lambda row: row["Runs_Scored"] / row["Dismissals"] if row["Dismissals"] > 0 else row["Runs_Scored"], axis=1
)
batting_stats["Strike_Rate"] = (batting_stats["Runs_Scored"] / batting_stats["Balls_Faced"]) * 100
batting_stats = batting_stats.fillna(0).round(2)

# Bowling Stats Calculation
bowling_stats = df.groupby("Bowler").agg(
    Wickets=("Is strike out", "sum"),
    Runs_Conceded=("Batter Runs", "sum"),
    Balls_Bowled=("Balls", "count")
).reset_index()

bowling_stats["Economy_Rate"] = (bowling_stats["Runs_Conceded"] / (bowling_stats["Balls_Bowled"] / 6)).round(2)
bowling_stats = bowling_stats.fillna(0)

# HTML & CSS for Table
table_css = """
<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
    }
    tr:nth-child(even) { background-color: #F9F9F9; }
    tr:nth-child(odd) { background-color: #F2F2F2; }
    th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
</style>
"""

# Streamlit UI
st.title("T20 Cricket Stats")

# Tabs
tab1, tab2 = st.tabs(["Stats", "Player Dashboard"])

# *Tab 1: Stats*
with tab1:
    st.subheader("Select Stats Type")
    option = st.selectbox("Choose Stats", ["Batting Stats", "Bowling Stats"])

    if option == "Batting Stats":
        st.markdown(table_css, unsafe_allow_html=True)
        st.dataframe(batting_stats.sort_values(by="Runs_Scored", ascending=False))

    elif option == "Bowling Stats":
        st.markdown(table_css, unsafe_allow_html=True)
        st.dataframe(bowling_stats.sort_values(by="Wickets", ascending=False))

# *Tab 2: Player Dashboard*
with tab2:
    st.subheader("Search Player Stats")
    player_name = st.text_input("Enter Player Name")

    if player_name:
        batting_data = batting_stats[batting_stats["Striker"].str.contains(player_name, case=False, na=False)]
        bowling_data = bowling_stats[bowling_stats["Bowler"].str.contains(player_name, case=False, na=False)]

        if not batting_data.empty:
            st.subheader("Batting Stats")
            st.markdown(table_css, unsafe_allow_html=True)
            st.dataframe(batting_data)

        if not bowling_data.empty:
            st.subheader("Bowling Stats")
            st.markdown(table_css, unsafe_allow_html=True)
            st.dataframe(bowling_data)

        if batting_data.empty and bowling_data.empty:
            st.warning("No data found for this player.")