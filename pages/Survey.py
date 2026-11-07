# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = APP_DIR / "data.csv"

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What is your favorite NFL team?")
    value_input = st.text_input(
        "How satisfied are you with their 2024 season? (1–10)"
    )

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        team_name = category_input.strip()

        if team_name == "":
            st.error("Please enter your favorite NFL team.")
        else:
            try:
                rating = int(value_input)

                if 1 <= rating <= 10:
                    new_row = pd.DataFrame({
                        "Category": [team_name],
                        "Value": [rating]
                    })

                    new_row.to_csv(
                        CSV_PATH,
                        mode="a",
                        header=(
                            not CSV_PATH.exists()
                            or CSV_PATH.stat().st_size == 0
                        ),
                        index=False
                    )

                    st.success("Your data has been submitted!")
                    st.write(
                        f"Team: **{team_name}**, "
                        f"Satisfaction: **{rating}/10**"
                    )
                else:
                    st.error("Please enter a rating from 1 to 10.")

            except ValueError:
                st.error("Please enter a whole number for your rating.")

# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
    current_data_df = pd.read_csv(CSV_PATH)
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")