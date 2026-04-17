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

/* Background */
.stApp {
    background-color: #0f172a;
}

/* Main strong text */
h1, h2, h3 {
    color: #f9fafb !important;
    font-weight: 600;
}

/* Sub text (taglines, descriptions) */
p {
    color: #cbd5e1 !important;
}

/* Muted / small text */
small, span {
    color: #94a3b8 !important;
}

/* Force all text visible */
div, label {
    color: #e5e7eb !important;
}

/* Fix markdown transparency issue */
.stMarkdown {
    color: #e5e7eb !important;
    opacity: 1 !important;
}

/* Buttons */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
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
