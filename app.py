import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# -----------------------------
# PAGE CONFIG (ONLY ONCE)
# -----------------------------
st.set_page_config(
    page_title="DataVista AI",
    page_icon="📊",   # or "icon.ico" if file exists
    layout="wide"
)

# -----------------------------
# SESSION STATE (PROJECTS)
# -----------------------------
if "projects" not in st.session_state:
    st.session_state.projects = []

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("📂 DataVista AI")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Dashboard", "🗂 Recent Projects"]
)

# -----------------------------
# HOME PAGE
# -----------------------------
if menu == "🏠 Home":

    st.title("🚀 DataVista AI")
    st.subheader("Smart Data Analytics Dashboard")

    st.markdown("""
    ### 👋 Welcome!
    DataVista AI helps you analyze your data easily.

    ### 🔍 Features:
    - Upload Excel/CSV  
    - Clean Data  
    - Create Charts  
    - Get AI Insights  

    ### 📌 How to use:
    1. Go to Dashboard  
    2. Upload file  
    3. Explore insights  
    """)

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
elif menu == "📊 Dashboard":

    st.title("📊 AI Data Pipeline Dashboard")

    # Upload file
    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    def clean_data(df):
        df = df.drop_duplicates()
        df = df.fillna(0)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    def generate_insights(df):
        insights = []
        insights.append(f"Total Rows: {df.shape[0]}")
        insights.append(f"Total Columns: {df.shape[1]}")

        num_cols = df.select_dtypes(include='number').columns

        for col in num_cols:
            insights.append(f"\n🔹 {col}")
            insights.append(f"Avg: {df[col].mean():.2f}")
            insights.append(f"Max: {df[col].max()}")
            insights.append(f"Min: {df[col].min()}")

        return "\n".join(insights)

    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------
    def business_insights(df):
        insights = []
        num_cols = df.select_dtypes(include='number').columns

        for col in num_cols:
            mean = df[col].mean()

            if mean > 1000:
                insights.append(f"{col} shows high values")

            if df[col].max() > mean * 3:
                insights.append(f"{col} has spikes")

        return insights

    # -----------------------------
    # MAIN LOGIC
    # -----------------------------
    if uploaded_file:

        # Save project name
        if uploaded_file.name not in st.session_state.projects:
            st.session_state.projects.append(uploaded_file.name)

        # Read file
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df_clean = clean_data(df)

        # Show data
        st.subheader("📄 Cleaned Data")
        st.dataframe(df_clean)

        # KPI
        st.subheader("📊 Overview")
        col1, col2 = st.columns(2)
        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])

        # Chart
        st.subheader("📊 Chart")
        column = st.selectbox("Select Column", df_clean.columns)

        if pd.api.types.is_numeric_dtype(df_clean[column]):
            fig = px.histogram(df_clean, x=column)
        else:
            data = df_clean[column].value_counts().reset_index()
            data.columns = [column, "count"]
            fig = px.bar(data, x=column, y="count")

        st.plotly_chart(fig, use_container_width=True)

        # Insights
        st.subheader("📊 Insights")
        st.text(generate_insights(df_clean))

        st.subheader("💡 Business Insights")
        biz = business_insights(df_clean)

        if biz:
            for i in biz:
                st.write("👉", i)
        else:
            st.write("No strong patterns found")

# -----------------------------
# RECENT PROJECTS PAGE
# -----------------------------
elif menu == "🗂 Recent Projects":

    st.title("🗂 Recent Projects")

    if st.session_state.projects:
        for project in st.session_state.projects:
            st.write("📁", project)
    else:
        st.info("No projects yet")
