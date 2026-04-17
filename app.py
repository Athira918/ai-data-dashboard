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

# Reviews Button
with col4:
    if st.button("Reviews", use_container_width=True):
        st.session_state.menu = "Reviews"
        st.rerun()
# -----------------------------
# PAGE CONTROL
# -----------------------------

if menu == "Home":

    # ---------------- FEATURE CARDS ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3>Data Analysis</h3>
            <p>Explore datasets, detect patterns, and uncover insights instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3>Smart Visualization</h3>
            <p>Interactive charts that reveal trends and business opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3> AI Insights</h3>
            <p>Automated insights to help you make data-driven decisions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Why Use DataVista AI?")
    st.markdown("""
    ✔ Analyze data faster without coding complexity  
    ✔ Automatically clean and structure datasets  
    ✔ Generate meaningful insights in seconds  
    ✔ Identify trends and business opportunities  
    ✔ Export reports for decision-making  
    """)

    st.divider()

    st.subheader("How It Works")
    st.markdown("""
  1 Upload your dataset (CSV / Excel)  
    2 Clean and prepare data automatically  
    3 Explore interactive dashboards  
    4 Generate insights & reports  
    """)

    st.divider()

    st.markdown("""
    <div style="text-align:center; margin-top:30px;">
        <h2> Start Your Data Journey</h2>
        <p style="color:#94a3b8;">Upload your dataset and unlock insights instantly</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="text-align:center; margin-top:40px;">
        <p style="color:#64748b;">Designed & Developed by</p>
        <h3 style="margin-top:-10px;">ATHIRA</h3>
    </div>
    """, unsafe_allow_html=True)


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


elif menu == "Recent Projects":

    st.title("Recent Projects")
    st.write("No projects yet")


elif menu == "Reviews":

    st.title(" User Reviews")

    if "reviews" not in st.session_state:
        st.session_state.reviews = []

    st.subheader("Write a Review")

    name = st.text_input("Your Name")
    rating = st.slider("Rating", 1, 5, 5)
    review = st.text_area("Your Feedback")

    if st.button("Submit Review"):
        if name and review:
            st.session_state.reviews.append({
                "name": name,
                "rating": rating,
                "review": review
            })
            st.success("Review submitted!")
        else:
            st.warning(" Please fill all fields")

    st.divider()

    st.subheader("What Users Say")

    if st.session_state.reviews:
        for r in st.session_state.reviews[::-1]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg,#111827,#1f2937);
                padding:20px;
                border-radius:12px;
                margin-bottom:10px;">
                <h4>{r['name']} {r['rating']}/5</h4>
                <p>{r['review']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No reviews yet. Be the first to write one!")


    # ---------------- HERO ----------------
    st.markdown("""
    <div style="text-align:center; padding-top:70px;">
        <h1 style="font-size:52px; font-weight:700;">DataVista AI</h1>
        <p style="font-size:20px; color:#94a3b8;">
            Transform raw data into powerful insights and smart decisions
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---------------- FEATURE CARDS ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3>Data Analysis</h3>
            <p>Explore datasets, detect patterns, and uncover insights instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3>Smart Visualization</h3>
            <p>Interactive charts that reveal trends and business opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:linear-gradient(145deg,#111827,#1f2937);
                    padding:25px; border-radius:15px; text-align:center;">
            <h3> AI Insights</h3>
            <p>Automated insights to help you make data-driven decisions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


    # ---------------- VALUE SECTION ----------------
    st.subheader("Why Use DataVista AI?")

    st.markdown("""
    ✔ Analyze data faster without coding complexity  
    ✔ Automatically clean and structure datasets  
    ✔ Generate meaningful insights in seconds  
    ✔ Identify trends and business opportunities  
    ✔ Export reports for decision-making  
    """)

    st.divider()

    # ---------------- WORKFLOW ----------------
    st.subheader("How It Works")

    st.markdown("""
  1 Upload your dataset (CSV / Excel)  
    2 Clean and prepare data automatically  
    3 Explore interactive dashboards  
    4 Generate insights & reports  
    """)

    st.divider()

    # ---------------- CALL TO ACTION ----------------
    st.markdown("""
    <div style="text-align:center; margin-top:30px;">
        <h2> Start Your Data Journey</h2>
        <p style="color:#94a3b8;">Upload your dataset and unlock insights instantly</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---------------- FOOTER ----------------
    st.markdown("""
    <div style="text-align:center; margin-top:40px;">
        <p style="color:#64748b;">Designed & Developed by</p>
        <h3 style="margin-top:-10px;">ATHIRA</h3>
    </div>
    """, unsafe_allow_html=True)
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
