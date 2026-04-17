import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# -----------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="DataVista AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# SESSION STATE (FIX ADDED)
# -----------------------------
if "projects" not in st.session_state:
    st.session_state.projects = []

# -----------------------------
# SIDEBAR (MENU FIX ADDED)
# -----------------------------
with st.sidebar:

    st.markdown("## DataVista AI")

    menu = st.radio(
        "Navigation",
        ["Home", "Dashboard", "Recent Projects"]
    )

# -----------------------------
# PROFESSIONAL CSS THEME
# -----------------------------
st.markdown("""
<style>

/* FORCE EVERYTHING VISIBLE */
* {
    color: #e5e7eb !important;
    opacity: 1 !important;
}

/* BACKGROUND */
.stApp {
    background-color: #0f172a !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* HEADINGS */
h1 {
    color: #ffffff !important;
    font-size: 42px !important;
    font-weight: 700 !important;
}

h2 {
    color: #f1f5f9 !important;
    font-size: 26px !important;
}

h3 {
    color: #cbd5e1 !important;
    font-size: 18px !important;
}

/* BUTTON */
.stButton>button {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 8px;
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background-color: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 10px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HOME
# -----------------------------
if menu == "Home":

    st.markdown("""
    <div style="padding-top: 40px; text-align: center;">
        <h1>DataVista AI</h1>
        <p>Intelligent data analysis and visualization platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.write("Data Processing")
    col2.write("Analytics Engine")
    col3.write("Visualization")
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
            sheet = st.selectbox("Select Sheet", sheet_names)
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
        st.subheader("Data")
        st.dataframe(df_clean)

        # KPI
        st.subheader("Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])

        num_cols = df_clean.select_dtypes(include='number').columns
        if len(num_cols) > 0:
            col3.metric("Avg Value", round(df_clean[num_cols[0]].mean(), 2))

        # CHARTS
        st.subheader("Smart Charts")

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
        st.subheader("Trend Analysis")

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
            st.warning("Could not generate trend")

        # INSIGHTS
        st.subheader("Insights")
        st.text(generate_insights(df_clean))

        st.subheader("Business Insights")
        biz = business_insights(df_clean)

        if biz:
            for i in biz:
                st.write("➡️", i)
        else:
            st.write("No strong patterns found")
# -----------------------------
# DASHBOARD
# -----------------------------
elif menu == "Dashboard":

    st.title("Data Dashboard")

    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    # FUNCTIONS
    def clean_data(df):
        df = df.drop_duplicates()
        df = df.fillna(0)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

    def generate_insights(df):
        insights = []
        insights.append(f"Total Rows: {df.shape[0]}")
        insights.append(f"Total Columns: {df.shape[1]}")

        for col in df.select_dtypes(include='number').columns:
            insights.append(f"\n{col}")
            insights.append(f"Avg: {df[col].mean():.2f}")
            insights.append(f"Max: {df[col].max()}")
            insights.append(f"Min: {df[col].min()}")

        return "\n".join(insights)

    def business_insights(df):
        insights = []
        for col in df.select_dtypes(include='number').columns:
            mean = df[col].mean()
            if mean > 1000:
                insights.append(f"{col} shows high values")
        return insights

    # LOAD DATA
    df_clean = None

    if "selected_project" in st.session_state:
        df_clean = st.session_state.selected_project["data"]

    elif uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df_clean = clean_data(df)

        # SAVE PROJECT (FIX ADDED)
        if uploaded_file.name not in [p["name"] for p in st.session_state.projects]:
            st.session_state.projects.append({
                "name": uploaded_file.name,
                "data": df_clean
            })

    # MAIN DASHBOARD
    if df_clean is not None:

        st.subheader("Dataset Overview")
        st.dataframe(df_clean)

        st.subheader("Overview")
        col1, col2 = st.columns(2)
        col1.metric("Rows", df_clean.shape[0])
        col2.metric("Columns", df_clean.shape[1])

        st.subheader("Visual Analysis")
        column = st.selectbox("Select Column", df_clean.columns)

        fig = px.histogram(df_clean, x=column)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Insights")
        st.code(generate_insights(df_clean))

        st.subheader("Business Insights")
        for i in business_insights(df_clean):
            st.markdown(f"- {i}")

        # COLUMN SUMMARY
        st.subheader("Column Summary")
        col_info = pd.DataFrame({
            "Column": df_clean.columns,
            "Type": df_clean.dtypes,
            "Missing Values": df_clean.isnull().sum()
        })
        st.dataframe(col_info)

        # PDF
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet

        def generate_pdf(text):
            doc = SimpleDocTemplate("report.pdf")
            styles = getSampleStyleSheet()
            content = [Paragraph(line, styles["Normal"]) for line in text.split("\n")]
            doc.build(content)

        if st.button("Generate Report"):
            generate_pdf(generate_insights(df_clean))
            with open("report.pdf", "rb") as f:
                st.download_button("Download Report", f, "DataVista_Report.pdf")

# -----------------------------
# RECENT PROJECTS
# -----------------------------
elif menu == "Recent Projects":

    st.title("Recent Projects")

    if st.session_state.projects:
        for i, project in enumerate(st.session_state.projects):
            if st.button(project['name'], key=i):
                st.session_state.selected_project = project
                st.session_state.menu = "Dashboard"
    else:
        st.info("No projects yet")
