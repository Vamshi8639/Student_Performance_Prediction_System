import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="TaPTaP College Analytics Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_excel("data/student_data.csv.xlsx")
model = joblib.load("models/placement_model.pkl")

df["Project_Value"] = df["Project_Completed"].map({"Yes": 1, "No": 0})

df["Performance_Score"] = (
    df["Attendance"] * 0.30 +
    df["Assignment_Score"] * 0.30 +
    df["MET_Score"] * 0.40
)

df["Employability_Band"] = pd.cut(
    df["Performance_Score"],
    bins=[0, 50, 60, 70, 80, 90, 100],
    labels=["F", "E", "D", "C", "B", "A"]
)

# =========================
# TITLE
# =========================

st.title("TaPTaP Student Employability Analytics Dashboard")

st.write(
    "This dashboard shows how TaPTaP helps colleges improve student learning, assignments, MET performance, projects, and placement readiness."
)

# =========================
# TOP KPI CARDS
# =========================

total_students = len(df)
placed_students = len(df[df["Placement_Status"] == "Placed"])
not_placed_students = len(df[df["Placement_Status"] == "Not Placed"])
placement_rate = round((placed_students / total_students) * 100, 2)

avg_attendance = round(df["Attendance"].mean(), 2)
avg_assignment = round(df["Assignment_Score"].mean(), 2)
avg_met = round(df["MET_Score"].mean(), 2)

projects_completed = len(df[df["Project_Completed"] == "Yes"])
placement_ready = len(df[df["Performance_Score"] >= 75])
students_at_risk = len(df[df["Performance_Score"] < 60])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", total_students)
c2.metric("Placed Students", placed_students)
c3.metric("Placement Rate", f"{placement_rate}%")
c4.metric("Placement Ready", placement_ready)

c5, c6, c7, c8 = st.columns(4)

c5.metric("Average Attendance", avg_attendance)
c6.metric("Average Assignment", avg_assignment)
c7.metric("Average MET Score", avg_met)
c8.metric("Students At Risk", students_at_risk)

st.markdown("---")

# =========================
# PORTAL OVERVIEW
# =========================

st.header("What TaPTaP Provides")

st.write("""
TaPTaP is a student learning and employability platform. It helps colleges provide learning content, assignments, MET tests, sample projects, project practice, placement preparation, and student performance tracking.
""")

p1, p2, p3 = st.columns(3)

with p1:
    st.subheader("For Students")
    st.write("""
    - Learn technical skills  
    - Practice assignments  
    - Take MET tests  
    - Build sample projects  
    - Prepare for placements  
    """)

with p2:
    st.subheader("For Faculty")
    st.write("""
    - Track student progress  
    - Monitor assignments  
    - Check MET performance  
    - Identify weak students  
    - Support placement training  
    """)

with p3:
    st.subheader("For Colleges")
    st.write("""
    - Improve student skills  
    - Increase placement readiness  
    - Department-wise tracking  
    - Performance reports  
    - Better college outcomes  
    """)

st.markdown("---")

# =========================
# STUDENT SELECTION
# =========================

st.header("Student Performance Check")

selected_student = st.selectbox(
    "Select Student ID",
    df["Student_ID"].tolist()
)

student = df[df["Student_ID"] == selected_student].iloc[0]

s1, s2, s3, s4 = st.columns(4)

s1.metric("Student ID", student["Student_ID"])
s2.metric("Department", student["Department"])
s3.metric("Attendance", student["Attendance"])
s4.metric("MET Score", student["MET_Score"])

s5, s6, s7, s8 = st.columns(4)

s5.metric("Assignment Score", student["Assignment_Score"])
s6.metric("Project Completed", student["Project_Completed"])
s7.metric("Performance Score", round(student["Performance_Score"], 2))
s8.metric("Employability Band", student["Employability_Band"])

# =========================
# AUTOMATIC PREDICTION
# =========================

input_data = pd.DataFrame(
    [[
        student["Attendance"],
        student["Assignment_Score"],
        student["MET_Score"],
        student["Project_Value"]
    ]],
    columns=[
        "Attendance",
        "Assignment_Score",
        "MET_Score",
        "Project_Completed"
    ]
)

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1] * 100

st.subheader("Placement Prediction")

if prediction == 1:
    st.success("Prediction: Placed")
else:
    st.error("Prediction: Not Placed")

st.info(f"Placement Chance: {probability:.2f}%")

# =========================
# REMARKS
# =========================

st.subheader("Remarks and Improvement Suggestions")

remarks = []

if student["Performance_Score"] >= 85:
    remarks.append("Excellent performance. Student is highly placement ready.")
elif student["Performance_Score"] >= 70:
    remarks.append("Average to good performance. Student can improve further.")
else:
    remarks.append("Needs improvement. Student requires more practice and support.")

if student["Attendance"] < 75:
    remarks.append(f"Improve attendance by {75 - student['Attendance']} points.")
else:
    remarks.append("Attendance is good.")

if student["Assignment_Score"] < 70:
    remarks.append(f"Improve assignment score by {70 - student['Assignment_Score']} points.")
else:
    remarks.append("Assignment score is good.")

if student["MET_Score"] < 70:
    remarks.append(f"Improve MET score by {70 - student['MET_Score']} points.")
else:
    remarks.append("MET score is good.")

if student["Project_Completed"] == "No":
    remarks.append("Complete at least one project to improve placement chance.")

for r in remarks:
    st.write("✅", r)

st.markdown("---")

# =========================
# GRAPH FUNCTIONS
# =========================

def bar_chart(title, data, xlabel, ylabel):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(kind="bar", ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def pie_chart(title, data):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(7, 5))
    data.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)

# =========================
# 15 DASHBOARD GRAPHS
# =========================

st.header("TaPTaP Analytics Dashboard")

bar_chart(
    "1. Department Wise Students",
    df["Department"].value_counts(),
    "Department",
    "Students"
)

pie_chart(
    "2. Placement Status Percentage",
    df["Placement_Status"].value_counts()
)

bar_chart(
    "3. Project Completion Status",
    df["Project_Completed"].value_counts(),
    "Project Completed",
    "Students"
)

bar_chart(
    "4. Average Attendance by Department",
    df.groupby("Department")["Attendance"].mean(),
    "Department",
    "Average Attendance"
)

bar_chart(
    "5. Average Assignment Score by Department",
    df.groupby("Department")["Assignment_Score"].mean(),
    "Department",
    "Average Assignment Score"
)

bar_chart(
    "6. Average MET Score by Department",
    df.groupby("Department")["MET_Score"].mean(),
    "Department",
    "Average MET Score"
)

bar_chart(
    "7. Department Wise Placed Students",
    df[df["Placement_Status"] == "Placed"]["Department"].value_counts(),
    "Department",
    "Placed Students"
)

bar_chart(
    "8. Department Wise Not Placed Students",
    df[df["Placement_Status"] == "Not Placed"]["Department"].value_counts(),
    "Department",
    "Not Placed Students"
)

bar_chart(
    "9. Employability Band Distribution",
    df["Employability_Band"].value_counts().sort_index(),
    "Employability Band",
    "Students"
)

bar_chart(
    "10. Top 10 Students by Performance",
    df.sort_values("Performance_Score", ascending=False)
      .head(10)
      .set_index("Student_ID")["Performance_Score"],
    "Student ID",
    "Performance Score"
)

bar_chart(
    "11. Least 10 Students by Performance",
    df.sort_values("Performance_Score")
      .head(10)
      .set_index("Student_ID")["Performance_Score"],
    "Student ID",
    "Performance Score"
)

bar_chart(
    "12. Top 10 MET Score Students",
    df.nlargest(10, "MET_Score")
      .set_index("Student_ID")["MET_Score"],
    "Student ID",
    "MET Score"
)

bar_chart(
    "13. Least 10 MET Score Students",
    df.nsmallest(10, "MET_Score")
      .set_index("Student_ID")["MET_Score"],
    "Student ID",
    "MET Score"
)

bar_chart(
    "14. Top Departments by Performance",
    df.groupby("Department")["Performance_Score"]
      .mean()
      .sort_values(ascending=False),
    "Department",
    "Average Performance Score"
)

bar_chart(
    "15. Students Needing Improvement by Department",
    df[df["Performance_Score"] < 60]["Department"].value_counts(),
    "Department",
    "Students Needing Improvement"
)

st.success("Dashboard Loaded Successfully")