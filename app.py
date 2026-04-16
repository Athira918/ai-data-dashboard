import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ✅ ONLY ONCE
st.set_page_config(
    page_title="DataVista AI",
    page_icon="icon.ico",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "home":

    # 🎨 Background
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #eef2f3, #dfe9f3);
    }
    </style>
    """, unsafe_allow_html=True)

    # 🌟 Title
    st.markdown("""
    <h1 style='text-align: center; font-size: 55px;'>🚀 DataVista AI</h1>
    <p style='text-align: center; color: gray;'>Smart Data Analytics Dashboard</p>
    <p style='text-align: center;'>✨ Designed & Developed by <b>ATHIRA</b></p>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 👋 Welcome!
    - Upload Excel/CSV  
    - Clean Data  
    - Visualize & Analyze  
    - Get AI Insights  
    """)

    if st.button("▶ Start"):
        st.session_state.page = "app"

# -----------------------------
# MAIN APP
# -----------------------------
elif st.session_state.page == "app":

    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "home"

    st.title("🚀 AI Data Pipeline PRO Dashboard")

    # -----------------------------
    # SEND TO N8N
    # -----------------------------
    def send_to_n8n(insights, biz):
        url = "http://0.0.0.0:5678/webhook-test/44fa76df-a6fc-4a85-aef4-144b351859f5"
        data = {"insights": insights, "business": biz}
        try:
            response = requests.post(url, json=data)
            return response.status_code
        except:
            return None

    # -----------------------------
    # Upload
    # -----------------------------
    uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

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

            if df[col].max() > mean * 3:
                insights.append(f"{col} has spikes")

        return insights

    # -----------------------------
    # RUN APP
    # -----------------------------
    if uploaded_file:

        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df_clean = clean_data(df)

        st.subheader("📄 Data")
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
            fig = px.bar(data, x="index", y=column)

        st.plotly_chart(fig, use_container_width=True)

        # Insights
        st.subheader("📊 Insights")
        st.text(generate_insights(df_clean))

        st.subheader("💡 Business Insights")
        for i in business_insights(df_clean):
            st.write("👉", i)
