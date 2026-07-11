import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Performance Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Student Performance Dashboard")
st.markdown("Welcome to your student data analysis portal.")

# --- 2. DYNAMIC FILE PATH FIX ---
# This looks for 'students.csv' in the exact same folder where 'app.py' lives.
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "students.csv"


@st.cache_data
def load_data(path):
    # Safely checks if the file exists before reading it
    if not path.exists():
        st.error(
            f"❌ **Data file not found!**\n\n"
            f"Expected it at: `{path}`\n\n"
            f"**How to fix:** Please ensure that your dataset is named **`students.csv`** "
            f"and is placed in the exact same GitHub folder as this `app.py` file."
        )
        st.stop()
    return pd.read_csv(path)


# Load the dataset
df = load_data(CSV_PATH)

# --- 3. DASHBOARD METRICS ---
st.subheader("📈 Quick Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Students", value=len(df))

# Automatically search for a column containing grades or scores to calculate averages
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
        st.metric(label="Total Columns", value=len(df.columns))
    with col3:
        st.metric(label="Total Rows", value=df.shape[0])

st.divider()

# --- 4. DATA VIEW & VISUALIZATION ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Dataset Preview")
    st.dataframe(df, use_container_width=True)

with col_right:
    st.subheader("📊 Performance Distribution")

    if score_cols:
        # Create a clean matplotlib histogram
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(df[score_cols[0]], bins=15, color="#1f77b4", edgecolor="black")
        ax.set_title(f"Distribution of {score_cols[0]}", fontsize=12)
        ax.set_xlabel("Scores", fontsize=10)
        ax.set_ylabel("Number of Students", fontsize=10)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Render the plot in Streamlit
        st.pyplot(fig)
    else:
        st.info(
            "💡 Want a chart? Add a column containing the word 'Score' or 'Grade' to your CSV to automatically generate a performance histogram!"
        )