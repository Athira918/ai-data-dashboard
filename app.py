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
# CSS
# -----------------------------
st.markdown("""
<style>
.stApp { background-color: #0f172a; }

h1, h2, h3 { color: #f9fafb !important; }

p { color: #cbd5e1 !important; }

.stButton > button {
    background: linear-gradient(135deg, #1f2937, #111827);
    border-radius: 10px;
    height: 50px;
}

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

if "menu" not in st.session_state:
    st.session_state.menu = "Home"

menu = st.session_state.menu

# ---------------- NAVBAR ----------------
st.markdown("### Navigate")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Home", use_container_width=True):
        st.session_state.menu = "Home"
        st.rerun()

with col2:
    if st.button("Dashboard", use_container_width=True):
        st.session_state.menu = "Dashboard"
        st.rerun()

with col3:
    if st.button("Projects", use_container_width=True):
        st.session_state.menu = "Recent Projects"
        st.rerun()

with col4:
    if st.button("Insights", use_container_width=True):
        st.session_state.menu = "Dashboard"
        st.rerun()

# -----------------------------
# HOME
# -----------------------------
if menu == "Home":

    st.markdown("""
    <div style="text-align:center; padding-top:70px;">
        <h1>DataVista AI</h1>
        <p>Transform raw data into powerful insights</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.write("Data Analysis")
    col2.write("Smart Visualization")
    col3.write("AI Insights")

    st.divider()

    st.subheader("Why Use DataVista AI?")
    st.write("Analyze data faster and generate insights instantly.")

    st.divider()

# -----------------------------
# DASHBOARD
# -----------------------------
elif menu == "Dashboard":

    st.title("Data Dashboard")

    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    def clean_data(df):
        df = df.drop_duplicates()
        df = df.fillna(0)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

    def generate_insights(df):
        return f"Rows: {df.shape[0]}, Columns: {df.shape[1]}"

    df_clean = None

    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df_clean = clean_data(df)

    if df_clean is not None:
        st.dataframe(df_clean)

# -----------------------------
# PROJECTS
# -----------------------------
elif menu == "Recent Projects":
    st.title("Recent Projects")
    st.write("No projects yet")
