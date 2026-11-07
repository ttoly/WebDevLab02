# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path


# PAGE CONFIGURATION
st.set_page_config(
    page_title="NFL Visuals",
    page_icon="🏈",
)

# PAGE TITLE
st.title("2024 NFL Team Records 🏈")
st.write("Explore the final team records from the 2024 regular season.")


# PART 1: GRAPHS FROM data.json
APP_DIR = Path(__file__).resolve().parent.parent

with open(APP_DIR / "data.json", "r") as infile:
    data = json.load(infile)

teams = data["data_points"]

st.header("Team Wins")
st.write("This chart compares the regular-season wins of all 32 teams.")

wins_df = pd.DataFrame({
    "Team": [team["label"] for team in teams],
    "Wins": [team["wins"] for team in teams],
})

st.bar_chart(wins_df.set_index("Team"))

# PART 1: DYNAMIC PIE CHART
st.header("Selected Team: Wins and Losses")

team_names = [team["label"] for team in teams]

# Store the selected team in Session State
if "selected_team" not in st.session_state:
    st.session_state["selected_team"] = team_names[0]

st.selectbox(
    "Choose a team:",
    options=team_names,
    key="selected_team",
)

for team in teams:
    if team["label"] == st.session_state["selected_team"]:
        selected_team = team
        break

fig, ax = plt.subplots()

ax.pie(
    [selected_team["wins"], selected_team["losses"]],
    labels=["Wins", "Losses"],
    autopct="%1.1f%%",
    colors=["#2ca02c", "#d62728"],
    startangle=90,
)

ax.set_title(
    f'{selected_team["label"]}: '
    f'{selected_team["wins"]} Wins, '
    f'{selected_team["losses"]} Losses'
)
ax.axis("equal")

st.pyplot(fig)
plt.close(fig)

st.caption("Source: NFL official 2024 regular-season standings")
st.markdown(
    "[View original data]"
    "(https://www.nfl.com/standings/division/2024/REG)"
)



# PART 2: GRAPHS FROM data.csv
csv_path = APP_DIR / "data.csv"

st.divider()
st.header("NFL Fan Survey Results")

if not csv_path.exists():
    st.info("Please submit a response on the Survey page first.")
else:
    survey_df = pd.read_csv(csv_path)

    if survey_df.empty:
        st.info("Please submit a response on the Survey page first.")
    else:
        # STATIC CHART: Average satisfaction by team
        st.subheader("Average Satisfaction by Team")

        average_ratings = survey_df.groupby("Category")["Value"].mean()

        fig, ax = plt.subplots()

        ax.bar(
            average_ratings.index,
            average_ratings.values,
            color="steelblue"
        )

        ax.set_title("Average Satisfaction with the 2024 Season")
        ax.set_xlabel("NFL Team")
        ax.set_ylabel("Average Satisfaction (1–10)")
        ax.set_ylim(0, 10)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        # DYNAMIC CHART: Rating distribution for a selected team
        st.subheader("Satisfaction Distribution by Team")

        survey_teams = sorted(survey_df["Category"].unique().tolist())

        st.selectbox(
            "Select a team from the survey:",
            options=survey_teams,
            key="survey_team"
        )

        selected_ratings = survey_df.loc[
            survey_df["Category"] == st.session_state["survey_team"],
            "Value"
        ]

        fig, ax = plt.subplots()

        ax.hist(
            selected_ratings,
            bins=[x - 0.5 for x in range(1, 12)],
            color="orange",
            edgecolor="black"
        )

        ax.set_title(
            f'{st.session_state["survey_team"]}: Satisfaction Distribution'
        )
        ax.set_xlabel("Satisfaction Rating")
        ax.set_ylabel("Number of Responses")
        ax.set_xticks(range(1, 11))

        # Show whole numbers on the response-count axis
        max_count = int(selected_ratings.value_counts().max())
        ax.set_yticks(range(max_count + 1))

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)
