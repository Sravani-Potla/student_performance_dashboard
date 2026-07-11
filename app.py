import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Performance Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Student Performance Dashboard")
st.markdown("Welcome to your student data analysis portal.")

# --- SAFE FILE LOADING ---
# This finds 'students.csv' in the same folder as this app.py file
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "students.csv"


@st.cache_data
def load_data(path):
    # Checks if the file actually exists before trying to read it
    if not path.exists():
        st.error(
            f"❌ **Data file not found!** Expected it at: `{path}`. Please ensure 'students.csv' is uploaded to GitHub in the correct folder."
        )
        st.stop()
    return pd.read_csv(path)


# Load the dataset
df = load_data(CSV_PATH)

# --- DASHBOARD METRICS ---
st.subheader("📈 Quick Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Students", value=len(df))

# Dynamically checking for common column names to show metrics safely
score_cols = [c for c in df.columns if "score" in c.lower() or "grade" in c.lower()]

if score_cols:
    main_score = score_cols[0]
    with col2:
        st.metric(
            label=f"Average {main_score}", value=f"{df[main_score].mean():.1f}"
        )
    with col3:
        st.metric(label=f"Max {main_score}", value=df[main_score].max())
else:
    with col2:
        st.metric(label="Data Columns", value=len(df.columns))
    with col3:
        st.metric(label="Data Rows", value=df.shape[0])

st.divider()

# --- DATA VIEW & CHART ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

with col_right:
    st.subheader("📊 Performance Distribution")

    if score_cols:
        # Create a matplotlib histogram
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(df[score_cols[0]], bins=15, color="skyblue", edgecolor="black")
        ax.set_title(f"Distribution of {score_cols[0]}")
        ax.set_xlabel("Scores")
        ax.set_ylabel("Number of Students")

        # Display the plot in Streamlit
        st.pyplot(fig)
    else:
        st.info(
            "Add a column containing the word 'Score' or 'Grade' to your CSV to automatically generate a performance chart!"
        )