
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

            if df[col].std() > 0:
                outliers = df[df[col] > df[col].mean() + 2 * df[col].std()]
                insights.append(f"Outliers: {len(outliers)}")

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

            if df[col].min() < mean * 0.2:
                insights.append(f"{col} has very low values")

        return insights

    # ---------------- LOAD DATA ----------------
    df_clean = None

    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet = st.selectbox("Select Sheet", excel_file.sheet_names)
            df = pd.read_excel(excel_file, sheet_name=sheet)

        df_clean = clean_data(df)

    # ---------------- DASHBOARD ----------------
    if df_clean is not None:

        # DATA
        st.subheader("Data")
        st.dataframe(df_clean)

        # KPI CARDS
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

                   st.warning("Could not generate trend")

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
