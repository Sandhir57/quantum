import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    file_path = "gp-search-20250302-213502-1.csv"  # Update if needed
    return pd.read_csv(file_path)

df = load_data()

# Streamlit App Layout
st.title("🔬 Quantum Computing Patents Dashboard")
st.markdown("Analyze trends, assignees, inventors, and more!")

# Sidebar filters
assignee_filter = st.sidebar.multiselect("Select Assignee(s):", df["assignee"].dropna().unique())
inventor_filter = st.sidebar.multiselect("Select Inventor(s):", df["inventor/author"].dropna().unique())

filtered_df = df
if assignee_filter:
    filtered_df = filtered_df[filtered_df["assignee"].isin(assignee_filter)]
if inventor_filter:
    filtered_df = filtered_df[filtered_df["inventor/author"].isin(inventor_filter)]

# Show data table
st.subheader("📊 Filtered Data Preview")
st.dataframe(filtered_df)

# Bar chart: Top Assignees
st.subheader("🏢 Top Patent Holders")
assignee_counts = df["assignee"].value_counts().reset_index()
assignee_counts.columns = ["Assignee", "Patent Count"]
fig1 = px.bar(assignee_counts.head(10), x="Assignee", y="Patent Count", title="Top 10 Patent Assignees", color="Patent Count")
st.plotly_chart(fig1)

# Timeline: Patents by Year
df["publication date"] = pd.to_datetime(df["publication date"], errors="coerce")
df["Year"] = df["publication date"].dt.year
st.subheader("📅 Patent Trends Over Time")
fig2 = px.line(df.groupby("Year").size().reset_index(name="Patent Count"), x="Year", y="Patent Count", title="Patents Published Per Year")
st.plotly_chart(fig2)

# Links to patent details
st.subheader("🔗 Explore Individual Patents")
df["Result Link"] = df["result link"].apply(lambda x: f"[View Patent]({x})" if pd.notna(x) else "")
st.write(df[["title", "Result Link"]].to_markdown(index=False))

st.sidebar.info("📌 This is an initial version. More AI/NLP insights coming soon!")
