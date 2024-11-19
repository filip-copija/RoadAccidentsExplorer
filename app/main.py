import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URI)

# SQL WRITER FUNC
def run_query(query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            columns = result.keys()
            return pd.DataFrame(data, columns=columns)
    except Exception as e:
        return str(e)

st.set_page_config(page_title="Road Accidents Dashboard", layout="wide")

# Title
st.title("Road Accidents Database Explorer 🚧")

# Dashboard summary cards
st.subheader("Dashboard Summary 🔎")
summary_query = """SELECT * FROM accidents_summary;"""
summary_data = run_query(summary_query)

if isinstance(summary_data, pd.DataFrame) and not summary_data.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Regions", summary_data["total_regions"][0])
    col2.metric("Total Records", summary_data["total_accidents_records"][0])
    col3.metric("Total Accidents", summary_data["total_accidents"][0])
else:
    st.error("Failed to load summary data.")

# SQL Query Writer
st.subheader("SQL Query Writer ✒️")
with st.container():
    left, right = st.columns(2)
    with left:
        query = st.text_area("Write your SQL query here:")
        execute_button = st.button("Execute Query")
    with right:
        if execute_button:
            query_result = run_query(query)
            if isinstance(query_result, pd.DataFrame):
                st.write("Query Results 📈")
                st.dataframe(query_result)
                csv = query_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            else:
                st.error(query_result)

# Accidents Over Time
st.subheader("Accidents Over Time")
accidents_by_year_query = "SELECT * FROM accidents_over_time"
accidents_by_year = run_query(accidents_by_year_query)

if isinstance(accidents_by_year, pd.DataFrame):
    accidents_by_year['year'] = accidents_by_year['year'].astype(int)
    min_year, max_year = accidents_by_year['year'].min(), accidents_by_year['year'].max()
    year_range = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    filtered_data = accidents_by_year[
        (accidents_by_year['year'] >= year_range[0]) & 
        (accidents_by_year['year'] <= year_range[1])
    ]
    filtered_data['year'] = filtered_data['year'].astype(str)
    st.line_chart(filtered_data.set_index("year"), color="#666633")
else:
    st.error("Failed to load accidents data.")

# Aggregated Data Explorer
st.subheader("Explore Aggregated Data")
col1, col2 = st.columns(2)
with col1:
    view_option = st.selectbox(
        "Select a view to explore:",
        ["accidents_by_region", "accidents_by_year", "top_accidents_regions"]
    )

    view_query = f"SELECT * FROM {view_option}"
    view_data = run_query(view_query)

    if isinstance(view_data, pd.DataFrame):
        st.write(f"Data from `{view_option}`:")
        st.dataframe(view_data)
    else:
        st.error(f"Failed to load data from `{view_option}`.")
