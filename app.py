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

/* HEADINGS (VERY IMPORTANT) */
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

/* FIX STREAMLIT TITLE (THIS IS THE MAIN ISSUE) */
[data-testid="stMarkdownContainer"] h1 {
    color: #ffffff !important;
}

[data-testid="stMarkdownContainer"] p {
    color: #cbd5e1 !important;
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

/* REMOVE FADED LOOK */
.stMarkdown, .stText {
    opacity: 1 !important;
    color: #e5e7eb !important;
}

/* FIX LABELS */
label {
    color: #e5e7eb !important;
}

/* FILE UPLOADER */
.stFileUploader label {
    color: #e5e7eb !important;
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
