import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(layout="wide")

st.title("🚀 AI Data Pipeline PRO Dashboard")

# -----------------------------
# SEND TO N8N FUNCTION
# -----------------------------
def send_to_n8n(insights, biz):
    url = "http://0.0.0.0:5678/webhook-test/44fa76df-a6fc-4a85-aef4-144b351859f5"

    data = {
        "insights": insights,
        "business": biz
    }

    try:
        response = requests.post(url, json=data)
        print("Status:", response.status_code)
        print("Response:", response.text)
        return response.status_code
    except Exception as e:
        print("Error:", e)
        return None
# -----------------------------
# Upload file
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])


# -----------------------------
# Data Cleaning
# -----------------------------
def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(0)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df


# -----------------------------
# Insights
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

        if df[col].std() > 0:
            outliers = df[df[col] > df[col].mean() + 2 * df[col].std()]
            insights.append(f"Outliers: {len(outliers)}")

    return "\n".join(insights)


# -----------------------------
# Business Insights
# -----------------------------
def business_insights(df):
    insights = []
    num_cols = df.select_dtypes(include='number').columns

    for col in num_cols:
        mean = df[col].mean()

        if mean > 1000:
            insights.append(f"{col} shows high overall values")

        if df[col].max() > mean * 3:
            insights.append(f"{col} has extreme spikes")

        if df[col].min() < mean * 0.2:
            insights.append(f"{col} has very low values")

    return insights


# -----------------------------
# MAIN APP
# -----------------------------
if uploaded_file:

    # -----------------------------
    # FILE READING (MULTI-SHEET)
    # -----------------------------
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
        sheet = "CSV File"
    else:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        sheet = st.selectbox("📄 Select Excel Sheet", sheet_names)
        df = pd.read_excel(excel_file, sheet_name=sheet)

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    df_clean = clean_data(df)

    st.success(f"Currently viewing: {sheet}")

    st.subheader("📄 Raw Data")
    st.dataframe(df)

    st.subheader("✅ Cleaned Data")
    st.dataframe(df_clean)

    # Download cleaned data
    st.download_button(
        "⬇ Download Cleaned Data",
        df_clean.to_csv(index=False),
        "cleaned_data.csv"
    )

    # -----------------------------
    # KPI DASHBOARD
    # -----------------------------
    st.subheader("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", df_clean.shape[0])
    col2.metric("Total Columns", df_clean.shape[1])

    num_cols = df_clean.select_dtypes(include='number').columns
    if len(num_cols) > 0:
        col3.metric("Avg Value", round(df_clean[num_cols[0]].mean(), 2))

    # -----------------------------
    # SMART CHARTS
    # -----------------------------
    st.subheader("📊 Smart Dashboard")

    col1, col2 = st.columns(2)

    column = st.selectbox("Select Column", df_clean.columns)

    top_n = 10

    with col1:
        if pd.api.types.is_numeric_dtype(df_clean[column]):
            fig1 = px.histogram(df_clean, x=column, nbins=30, title="Distribution")
        else:
            data = df_clean[column].value_counts().head(top_n).reset_index()
            data.columns = [column, "count"]

            fig1 = px.bar(data, x=column, y="count", title=f"Top {top_n} Categories", text="count")

        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        if not pd.api.types.is_numeric_dtype(df_clean[column]):
            fig2 = px.pie(data, names=column, values="count", title="Top Category Share")
        else:
            fig2 = px.box(df_clean, y=column, title="Box Plot (Outliers View)")

        st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # TREND ANALYSIS
    # -----------------------------
    st.subheader("📈 Trend Analysis")

    date_col = st.selectbox("Select Date Column", df_clean.columns)
    value_col = st.selectbox("Select Value Column", df_clean.select_dtypes(include='number').columns)

    try:
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')

        trend_df = df_clean.groupby(date_col)[value_col].sum().reset_index()

        fig3 = px.line(trend_df, x=date_col, y=value_col, title="Trend Over Time")

        st.plotly_chart(fig3, use_container_width=True)

    except:
        st.warning("⚠️ Could not generate trend (check date column)")

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    insights_text = generate_insights(df_clean)

    st.subheader("📊 Key Insights")
    st.text(insights_text)

    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------
    st.subheader("💡 Business Insights")

    biz = business_insights(df_clean)

    if biz:
        for i in biz:
            st.write("👉", i)
    else:
        st.write("No strong patterns found")

    # -----------------------------
    # SEND TO N8N BUTTON ✅
    # -----------------------------
    st.subheader("📤 Send Report")

    if st.button("Send to n8n"):
        status = send_to_n8n(insights_text, biz)

        if status == 200:
            st.success("✅ Sent successfully to n8n!")
        else:
            st.error("❌ Failed to send. Check n8n or webhook URL.")