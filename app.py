import streamlit as st
import sqlalchemy as sa
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Sakila Analytics Dashboard", layout="wide")

st.title("🎬 Sakila Film Analytics Dashboard")
st.markdown("Interactive insights into films, ratings, and rental trends")

# ---------------------------
# Database Connection
# ---------------------------
engine = sa.create_engine(
    "postgresql+psycopg://postgres:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
)


@st.cache_data
def load_data():
    query = "SELECT * FROM sakila.film"
    return pd.read_sql(query, engine)

df = load_data()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔎 Filters")

selected_years = st.sidebar.multiselect(
    "Select Release Year(s):",
    sorted(df["release_year"].dropna().unique()),
    default=sorted(df["release_year"].dropna().unique())
)

selected_ratings = st.sidebar.multiselect(
    "Select Rating(s):",
    df["rating"].dropna().unique(),
    default=df["rating"].dropna().unique()
)

filtered_df = df[
    (df["release_year"].isin(selected_years)) &
    (df["rating"].isin(selected_ratings))
]

# ---------------------------
# KPI Metrics
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Films", len(filtered_df))
col2.metric("Avg Rental Rate", f"${filtered_df['rental_rate'].mean():.2f}")
col3.metric("Avg Film Length", f"{filtered_df['length'].mean():.0f} min")
col4.metric("Unique Ratings", filtered_df["rating"].nunique())

st.markdown("---")

# ---------------------------
# Row 1 - Distribution Charts
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    fig_rating = px.pie(
        filtered_df,
        names="rating",
        title="Film Distribution by Rating",
        hole=0.4
    )
    st.plotly_chart(fig_rating, use_container_width=True)

with col2:
    fig_hist = px.histogram(
        filtered_df,
        x="rental_rate",
        nbins=20,
        title="Rental Rate Distribution",
        color="rating"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------
# Row 2 - Trends & Comparison
# ---------------------------
col3, col4 = st.columns(2)

with col3:
    films_per_year = (
        filtered_df.groupby("release_year")
        .size()
        .reset_index(name="count")
    )

    fig_year = px.bar(
        films_per_year,
        x="release_year",
        y="count",
        title="Number of Films per Year",
        color="count",
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_year, use_container_width=True)

with col4:
    fig_box = px.box(
        filtered_df,
        x="rating",
        y="length",
        title="Film Length Distribution by Rating",
        color="rating"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ---------------------------
# Row 3 - Advanced Scatter
# ---------------------------
st.markdown("### 🎯 Rental Rate vs Film Length")

fig_scatter = px.scatter(
    filtered_df,
    x="length",
    y="rental_rate",
    color="rating",
    size="rental_duration",
    hover_data=["title"],
    title="Rental Rate vs Film Length"
)

st.plotly_chart(fig_scatter, use_container_width=True)
