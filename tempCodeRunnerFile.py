import streamlit as st
import pandas as pd

st.title("AI Data Pipeline System")

uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(0)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

if uploaded_file:
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    cleaned_df = clean_data(df)

    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df)

    st.success("Data cleaned successfully!")