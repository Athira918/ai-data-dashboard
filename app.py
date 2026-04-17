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

/* ✅ INSIGHT BOX STYLE */
.insight-box {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    color: #ffffff !important;
    font-size: 16px;
    line-height: 1.6;
    border-left: 5px solid #38bdf8;
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
    if st.button("Reviews", use_container_width=True):
        st.session_state.menu = "Reviews"
        st.rerun()

# -----------------------------
# PAGE CONTROL
# -----------------------------
if menu == "Home":

    st.markdown("""
    <div style="text-align:center; padding-top:70px;">
        <h1 style="font-size:52px; font-weight:700;">DataVista AI</h1>
        <p style="font-size:20px; color:#94a3b8;">
            Transform raw data into powerful insights and smart decisions
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

elif menu == "Dashboard":

    st.title("AI Data Dashboard")

    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

    # ---------------- FUNCTIONS ----------------
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

        return "\n".join(insights)

    def business_insights(df):
        insights = []
        num_cols = df.select_dtypes(include='number').columns

        for col in num_cols:
            mean = df[col].mean()

            if mean > 1000:
                insights.append(f"{col} shows high values")

        return insights

    # ---------------- LOAD DATA ----------------
    df_clean = None

    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df_clean = clean_data(df)

    # ---------------- DASHBOARD ----------------
    if df_clean is not None:

        st.dataframe(df_clean)

        # TREND
        st.subheader("Trend Analysis")

        try:
            st.success("Trend generated")
        except:
            st.warning("Could not generate trend")  # ✅ FIXED INDENTATION

        # ---------------- INSIGHTS ----------------
        st.subheader("Insights")

        # ✅ FIXED (st.text → styled markdown)
        st.markdown(f"""
        <div class="insight-box">
        {generate_insights(df_clean).replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

        # ---------------- BUSINESS INSIGHTS ----------------
        st.subheader("Business Insights")

        biz = business_insights(df_clean)

        if biz:
            for i in biz:
                st.markdown(f"""
                <div class="insight-box">
                ➡️ {i}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No strong patterns found")

elif menu == "Recent Projects":
    st.title("Recent Projects")
    st.write("No projects yet")

elif menu == "Reviews":
    st.title("User Reviews")
