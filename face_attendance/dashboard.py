import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Attendance Analytics",
    layout="wide"
)

st.title("📊 Face Recognition Attendance Analytics Dashboard")

# ==========================
# LOAD ATTENDANCE DATA
# ==========================

conn = sqlite3.connect("attendance.db")

df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

conn.close()

if len(df) == 0:
    st.warning("No attendance data found.")
    st.stop()

# ==========================
# LOAD STUDENT DATA
# ==========================

student_conn = sqlite3.connect("students.db")

students_df = pd.read_sql_query(
    "SELECT * FROM students",
    student_conn
)

student_conn.close()

# ==========================
# MERGE DATA
# ==========================

merged_df = pd.merge(
    df,
    students_df,
    on="name",
    how="inner"
)

# ==========================
# STUDENT FILTER
# ==========================

selected_student = st.selectbox(
    "Select Student",
    ["All"] + sorted(list(df["name"].unique()))
)

if selected_student != "All":
    filtered_df = df[df["name"] == selected_student]
else:
    filtered_df = df.copy()

# ==========================
# DOWNLOAD REPORT
# ==========================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Attendance Report",
    data=csv,
    file_name="attendance_report.csv",
    mime="text/csv"
)

# ==========================
# ATTENDANCE COUNT
# ==========================

attendance_count = filtered_df["name"].value_counts()

# ==========================
# KPIs
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Students",
        filtered_df["name"].nunique()
    )

with col2:
    st.metric(
        "Total Records",
        len(filtered_df)
    )

with col3:
    if len(attendance_count) > 0:
        st.metric(
            "Most Regular Student",
            attendance_count.idxmax()
        )

with col4:
    if len(attendance_count) > 0:
        st.metric(
            "Least Regular Student",
            attendance_count.idxmin()
        )

# ==========================
# ATTENDANCE %
# ==========================

total_days = filtered_df["date"].nunique()

report = pd.DataFrame({
    "Student": attendance_count.index,
    "Days Present": attendance_count.values
})

if total_days > 0:
    report["Attendance %"] = (
        report["Days Present"] /
        total_days
    ) * 100

st.subheader("📋 Attendance Percentage Report")

st.dataframe(report)

# ==========================
# RISK STUDENTS
# ==========================

risk_students = report[
    report["Attendance %"] < 75
]

st.subheader("⚠ Students Below 75% Attendance")

st.dataframe(risk_students)

# ==========================
# LEADERBOARD
# ==========================

st.subheader("🏆 Attendance Leaderboard")

leaderboard = report.sort_values(
    by="Attendance %",
    ascending=False
)

st.dataframe(leaderboard)

# ==========================
# DEPARTMENT ANALYTICS
# ==========================

st.subheader("🏢 Department Attendance")

if not merged_df.empty:

    dept_attendance = (
        merged_df.groupby("department")
                 .size()
                 .reset_index(name="Attendance Count")
    )

    st.dataframe(dept_attendance)

    dept_fig = px.bar(
        dept_attendance,
        x="department",
        y="Attendance Count",
        title="Attendance by Department"
    )

    st.plotly_chart(
        dept_fig,
        use_container_width=True
    )

# ==========================
# INSIGHTS
# ==========================

st.subheader("📌 Insights")

avg_attendance = report["Attendance %"].mean()

if len(attendance_count) > 0:

    st.write(
        f"✅ Most Regular Student: {attendance_count.idxmax()}"
    )

    st.write(
        f"⚠ Least Regular Student: {attendance_count.idxmin()}"
    )

st.write(
    f"📈 Average Attendance: {avg_attendance:.2f}%"
)

st.write(
    f"👥 Students Below 75%: {len(risk_students)}"
)

# ==========================
# BAR CHART
# ==========================

st.subheader("📊 Attendance Count")

fig = px.bar(
    report,
    x="Student",
    y="Days Present",
    title="Attendance Count by Student"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# PIE CHART
# ==========================

st.subheader("🥧 Attendance Distribution")

fig2 = px.pie(
    report,
    names="Student",
    values="Days Present"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================
# DAILY TREND
# ==========================

st.subheader("📈 Daily Attendance Trend")

daily_attendance = (
    filtered_df.groupby("date")
               .size()
               .reset_index(name="Count")
)

fig3 = px.line(
    daily_attendance,
    x="date",
    y="Count",
    markers=True,
    title="Daily Attendance Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================
# RAW DATA
# ==========================

st.subheader("🗄 Raw Attendance Data")

st.dataframe(filtered_df)