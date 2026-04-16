import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DataVista AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "projects" not in st.session_state:
    st.session_state.projects = []

# -----------------------------
# SIDEBAR (FIXED)
# -----------------------------
st.sidebar.title("📂 DataVista AI")

if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Dashboard", "🗂 Recent Projects"],
    index=["🏠 Home", "📊 Dashboard", "🗂 Recent Projects"].index(st.session_state.menu)
)

st.session_state.menu = menu

# -----------------------------
# HOME (you forgot this block)
# -----------------------------
if menu == "🏠 Home":

    st.title("🚀 DataVista AI")
    st.subheader("Smart Data Analytics Dashboard " \n " Designed & Developed by ATHIRA")

# -----------------------------
# DASHBOARD
# -----------------------------
elif menu == "📊 Dashboard":

    st.title("🚀 AI Data Pipeline PRO Dashboard")

    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    # -----------------------------
    # FUNCTIONS
    # -----------------------------
    def clean_data(df):
        df = df.drop_duplicates()
        df = df.fillna(0)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

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

            if df[col].std() > 0:
                outliers = df[df[col] > df[col].mean() + 2 * df[col].std()]
                insights.append(f"Outliers: {len(outliers)}")

        return "\n".join(insights)

    def business_insights(df):
        insights = []
        num_cols = df.select_dtypes(include='number').columns

        for col in num_cols:
            mean = df[col].mean()

            if mean > 1000:
                insights.append(f"{col} shows high values")

            if df[col].max() > mean * 3:
                insights.append(f"{col} has spikes")

            if df[col].min() < mean * 0.2:
                insights.append(f"{col} has very low values")

        return insights

    # -----------------------------
    # MAIN
    # -----------------------------
    df_clean = None

    # LOAD FROM RECENT PROJECT
    if "selected_project" in st.session_state:
        project = st.session_state.selected_project
        df_clean = project["data"]
        st.success(f"Loaded Project: {project['name']}")

    # LOAD NEW FILE
    elif uploaded_file:

        # MULTI-SHEET SUPPORT
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
            sheet = "CSV File"
        else:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            sheet = st.selectbox("📄 Select Sheet", sheet_names)
            df = pd.read_excel(excel_file, sheet_name=sheet)

        df_clean = clean_data(df)

        # SAVE PROJECT (FIXED POSITION)
        if uploaded_file.name not in [p["name"] for p in st.session_state.projects]:
            st.session_state.projects.append({
                "name": uploaded_file.name,
                "data": df_clean
            })

        st.success(f"Currently viewing: {sheet}")

    # RUN DASHBOARD ONLY IF DATA EXISTS
    if df_clean is not None:

        # DATA VIEW
        st.subheader("📄 Data")
        st.dataframe(df_clean)

        # KPI
        st.subheader("📊 Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])

        num_cols = df_clean.select_dtypes(include='number').columns
        if len(num_cols) > 0:
            col3.metric("Avg Value", round(df_clean[num_cols[0]].mean(), 2))

        # CHARTS
        st.subheader("📊 Smart Charts")

        col1, col2 = st.columns(2)
        column = st.selectbox("Select Column", df_clean.columns)

        with col1:
            if pd.api.types.is_numeric_dtype(df_clean[column]):
                fig1 = px.histogram(df_clean, x=column)
            else:
                data = df_clean[column].value_counts().head(10).reset_index()
                data.columns = [column, "count"]
                fig1 = px.bar(data, x=column, y="count")

            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            if pd.api.types.is_numeric_dtype(df_clean[column]):
                fig2 = px.box(df_clean, y=column)
            else:
                fig2 = px.pie(data, names=column, values="count")

            st.plotly_chart(fig2, use_container_width=True)

        # TREND
        st.subheader("📈 Trend Analysis")

        date_col = st.selectbox("Select Date Column", df_clean.columns)
        value_col = st.selectbox(
            "Select Value Column",
            df_clean.select_dtypes(include='number').columns
        )

        try:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
            trend_df = df_clean.groupby(date_col)[value_col].sum().reset_index()

            fig3 = px.line(trend_df, x=date_col, y=value_col)
            st.plotly_chart(fig3, use_container_width=True)

        except:
            st.warning("⚠️ Could not generate trend")

        # INSIGHTS
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
# RECENT PROJECTS
# -----------------------------
elif menu == "🗂 Recent Projects":

    st.title("🗂 Recent Projects")

    if st.session_state.projects:
        for i, project in enumerate(st.session_state.projects):
            if st.button(f"📁 {project['name']}", key=i):
                st.session_state.selected_project = project
                st.session_state.menu = "📊 Dashboard"
    else:
        st.info("No projects yet")
