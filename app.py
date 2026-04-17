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

/* Global text fix */
body, p, span, label, div {
    color: #e2e8f0 !important;
}

/* Fix all headings */
h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Radio & Select labels */
.stRadio label, .stSelectbox label {
    color: #cbd5f5 !important;
    font-weight: 500;
}

/* File uploader text */
.stFileUploader label {
    color: #cbd5f5 !important;
}

/* Input text */
input, textarea {
    color: white !important;
}

/* Placeholder text */
::placeholder {
    color: #64748b !important;
}

/* Fix dataframe text */
[data-testid="stDataFrame"] {
    color: white !important;
}

/* Fix expander / subheader */
.stExpanderHeader {
    color: #e2e8f0 !important;
}

/* Success / warning messages */
.stAlert {
    color: white !important;
}

/* Make subheaders more visible */
h2 {
    border-bottom: 1px solid #1f2937;
    padding-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# SESSION STATE
# -----------------------------
if "projects" not in st.session_state:
    st.session_state.projects = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.markdown("""
        <div style="padding: 10px 0;">
            <h2>DataVista AI</h2>
            <p style="font-size:12px;">Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "Navigation",
        ["Home", "Dashboard", "Recent Projects"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <p style="font-size:12px;">
    Version 1.0<br>
    Developed by ATHIRA
    </p>
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
