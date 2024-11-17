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

st.title("Road Accidents Database Explorer")

st.subheader("SQL Query Writer")
with st.container():
    left, right = st.columns(2)
    with left:
        query = st.text_area("Write your SQL query here:")
        execute_button = st.button("Execute Query")
    with right:
        if execute_button:
            query_result = run_query(query)
            if isinstance(query_result, pd.DataFrame):
                st.write("Query Results")
                st.dataframe(query_result)
                csv = query_result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            else:
                st.error(query_result)

st.subheader("Accidents Over Time")
accidents_by_year_query = """
    SELECT year, SUM(value) AS total_accidents
    FROM accidents
    WHERE accident_type = 'wypadki ogółem'
    GROUP BY year
    ORDER BY year
"""
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
    st.line_chart(filtered_data.set_index("year"))
else:
    st.error("Failed to load accidents data.")