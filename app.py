import streamlit as st
import sqlalchemy as sa
import pandas as pd
import plotly.express as px

# Database connection string
engine = sa.create_engine("mysql+pymysql://root:0828Fasih2006@localhost:3306/sakila")

@st.cache_data
def load_data():
    query = "SELECT * FROM film"
    return pd.read_sql(query, engine)

df = load_data()

# --- Add interactive filters ---
st.sidebar.header("Filters")

# Filter by release year
years = df["release_year"].unique()
selected_year = st.sidebar.selectbox("Choose a release year:", sorted(years))

# Filter by rating
ratings = df["rating"].unique()
selected_rating = st.sidebar.multiselect("Choose rating(s):", ratings, default=ratings)

# Apply filters
filtered_df = df[(df["release_year"] == selected_year) & (df["rating"].isin(selected_rating))]

st.write(f"Showing films from {selected_year} with ratings {selected_rating}")

# --- Visualizations ---
# Line chart of rental_rate distribution
st.line_chart(filtered_df["rental_rate"].value_counts().sort_index())

# Average rental_rate by release_year (only filtered data)
avg_rates = filtered_df.groupby("release_year")["rental_rate"].mean()
st.line_chart(avg_rates)

# Histogram of rental_rate
fig = px.histogram(filtered_df, x="rental_rate", title="Distribution of Rental Rates")
st.plotly_chart(fig)