import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ---------------- Title ----------------
st.title("🎓 Student Performance Dashboard")
st.write("Analyze student marks and performance.")

# ---------------- Load Data ----------------
data = pd.read_csv("students.csv")

# ---------------- Display Dataset ----------------
st.subheader("📋 Student Records")
st.dataframe(data, use_container_width=True)

# ---------------- Student Selection ----------------
student = st.selectbox(
    "Select a Student",
    data["Name"]
)

student_data = data[data["Name"] == student]

st.subheader("📖 Student Details")
st.write(student_data)

# ---------------- Average Calculation ----------------
marks = student_data.iloc[:, 1:]

average = marks.mean(axis=1).values[0]

# ---------------- Grade ----------------
if average >= 90:
    grade = "A+"
elif average >= 80:
    grade = "A"
elif average >= 70:
    grade = "B"
elif average >= 60:
    grade = "C"
else:
    grade = "Fail"

# ---------------- Metrics ----------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Average Marks", f"{average:.2f}")

with col2:
    st.metric("Grade", grade)

# ---------------- Bar Chart ----------------
st.subheader("📊 Subject-wise Marks")

fig, ax = plt.subplots()

subjects = marks.columns
scores = marks.values.flatten()

ax.bar(subjects, scores)

ax.set_xlabel("Subjects")
ax.set_ylabel("Marks")
ax.set_title(f"{student}'s Performance")

st.pyplot(fig)

# ---------------- Class Statistics ----------------
st.subheader("📈 Class Average")

class_avg = data.iloc[:, 1:].mean()

st.bar_chart(class_avg)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")