import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import plotly.express as px

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
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

st.title("Road Accidents Database Explorer 🚧")

st.subheader("Dashboard Summary for Poland 🔎 (2014-2023)")

categories = [
    "wypadki ogółem",
    "ofiary wypadków ogółem",
    "ofiary śmiertelne",
    "ranni",
    "wina kierujących pojazdami - ogółem",
    "wina pieszych - ogółem",
    "współwina",
    "ogółem_nietrzeźwi",
]

summary_query = f"""
    SELECT accident_category, SUM(total_value) AS total_accidents
    FROM summary_overall
    WHERE region_name = 'POLSKA'
    AND accident_category IN ({','.join([f"'{cat}'" for cat in categories])})
    GROUP BY accident_category;
"""
summary_data = run_query(summary_query)

if isinstance(summary_data, pd.DataFrame) and not summary_data.empty:
    col1, col2, col3, col4 = st.columns(4)
    for i, category in enumerate(categories):
        value = summary_data.loc[summary_data['accident_category'] == category, 'total_accidents'].values
        metric_value = int(value[0]) if len(value) > 0 else 0

        if i < 4:
            locals()[f"col{i+1}"].metric(category.capitalize(), metric_value)
        else:
            locals()[f"col{i-3}"].metric(category.capitalize(), metric_value)
else:
    st.error("Failed to load summary data.")

st.subheader("Compare Two Provinces")

provinces_query = "SELECT DISTINCT region_name FROM summary_by_region_and_category WHERE region_type = 'województwo' ORDER BY region_name;"
provinces = run_query(provinces_query)

if isinstance(provinces, pd.DataFrame) and not provinces.empty:
    provinces_list = provinces['region_name'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        province1 = st.selectbox("Select the first province", options=provinces_list, key="province1")
        categories1 = st.multiselect(
            "Select categories for the first province",
            options=[
                "piesi", "kierujący pojazdami ogółem", "wina kierujących pojazdami - nieprzestrzeganie pierwszeństwa przejazdu",
                "kierujący rowerami", "wina pieszych - pozostałe", "wina pieszych - ogółem", "motocykle",
                "kierujący innymi pojazdami", "ofiary śmiertelne", "hulajnogi elektryczne", "wina kierujących pojazdami - ogółem",
                "kierujący motorowerami", "kierujący samochodami osobowymi", "kierujący samochodami ciężarowymi",
                "wina kierujących pojazdami - nieprawidłowe wyprzedzanie",
                "wina kierujących pojazdami - niezachowanie bezpiecznej odległości między pojazdami", "rowery", "ranni",
                "wina kierujących pojazdami - pozostałe", "ofiary wypadków ogółem", "inne pojazdy - ogółem",
                "wina pieszych - nieostrożne wejście na jezdnię", "ogółem_przyczyny", "wypadki ogółem", "motorowery",
                "ogółem_nietrzeźwi", "samochody osobowe", "ogółem_pojazdy", "inne pojazdy - nieustalony", "kierujący motocyklami",
                "wina kierujących pojazdami - nieprawidłowe zachowanie wobec pieszych", "wina pasażerów",
                "urządzenie transportu osobistego", "współwina", "pozostałe przyczyny", "wina kierujących pojazdami - niedostosowanie prędkości do warunków ruchu",
                "motocykle o pojemności silnika do 125 cm3", "samochody ciężarowe"
            ],
            key="categories1"
        )
    with col2:
        province2 = st.selectbox("Select the second province", options=provinces_list, key="province2")
        categories2 = st.multiselect(
            "Select categories for the second province",
            options=[
                "piesi", "kierujący pojazdami ogółem", "wina kierujących pojazdami - nieprzestrzeganie pierwszeństwa przejazdu",
                "kierujący rowerami", "wina pieszych - pozostałe", "wina pieszych - ogółem", "motocykle",
                "kierujący innymi pojazdami", "ofiary śmiertelne", "hulajnogi elektryczne", "wina kierujących pojazdami - ogółem",
                "kierujący motorowerami", "kierujący samochodami osobowymi", "kierujący samochodami ciężarowymi",
                "wina kierujących pojazdami - nieprawidłowe wyprzedzanie",
                "wina kierujących pojazdami - niezachowanie bezpiecznej odległości między pojazdami", "rowery", "ranni",
                "wina kierujących pojazdami - pozostałe", "ofiary wypadków ogółem", "inne pojazdy - ogółem",
                "wina pieszych - nieostrożne wejście na jezdnię", "ogółem_przyczyny", "wypadki ogółem", "motorowery",
                "ogółem_nietrzeźwi", "samochody osobowe", "ogółem_pojazdy", "inne pojazdy - nieustalony", "kierujący motocyklami",
                "wina kierujących pojazdami - nieprawidłowe zachowanie wobec pieszych", "wina pasażerów",
                "urządzenie transportu osobistego", "współwina", "pozostałe przyczyny", "wina kierujących pojazdami - niedostosowanie prędkości do warunków ruchu",
                "motocykle o pojemności silnika do 125 cm3", "samochody ciężarowe"
            ],
            key="categories2"
        )

    if st.button("Compare"):
        if province1 and province2 and categories1 and categories2:
            query1 = f"""
                SELECT accident_category, SUM(total_value) AS total
                FROM summary_by_region_and_category
                WHERE region_name = '{province1}'
                AND region_type = 'województwo'
                AND accident_category IN ({','.join([f"'{cat}'" for cat in categories1])})
                GROUP BY accident_category
                ORDER BY accident_category;
            """
            data1 = run_query(query1)

            query2 = f"""
                SELECT accident_category, SUM(total_value) AS total
                FROM summary_by_region_and_category
                WHERE region_name = '{province2}'
                AND region_type = 'województwo'
                AND accident_category IN ({','.join([f"'{cat}'" for cat in categories2])})
                GROUP BY accident_category
                ORDER BY accident_category;
            """
            data2 = run_query(query2)

            if isinstance(data1, pd.DataFrame) and not data1.empty and isinstance(data2, pd.DataFrame) and not data2.empty:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader(f"Comparison for {province1}")
                    fig1 = px.bar(
                        data1,
                        x="total",
                        y="accident_category",
                        orientation="h",
                        title=f"Accident Categories in {province1}",
                        labels={"total": "Total Accidents", "accident_category": "Category"},
                        color_discrete_sequence=["#656D4A"],
                    )
                    fig1.update_layout(height=500, xaxis=dict(title="Total"), yaxis=dict(title=""))
                    st.plotly_chart(fig1, use_container_width=True, key="province1_chart")

                with col2:
                    st.subheader(f"Comparison for {province2}")
                    fig2 = px.bar(
                        data2,
                        x="total",
                        y="accident_category",
                        orientation="h",
                        title=f"Accident Categories in {province2}",
                        labels={"total": "Total Accidents", "accident_category": "Category"},
                        color_discrete_sequence=["#656D4A"],
                    )
                    fig2.update_layout(height=500, xaxis=dict(title="Total"), yaxis=dict(title=""))
                    st.plotly_chart(fig2, use_container_width=True, key="province2_chart")

            else:
                st.error("Failed to fetch data for one or both provinces. Please check your selections.")
        else:
            st.warning("Please select both provinces and at least one category for each.")
else:
    st.error("Failed to fetch provinces.")

st.subheader("Accidents by Vehicle Type (2014-2023)")

region_data = run_query("SELECT DISTINCT name FROM regions WHERE type = 'województwo' ORDER BY name;")

region_filter = None 

if isinstance(region_data, pd.DataFrame) and not region_data.empty:
    region_filter = st.selectbox(
        "Select Region",
        ["POLSKA"] + region_data["name"].tolist()
    )
else:
    st.error("Failed to load regions. Please check your database connection or query.")

if region_filter:
    vehicle_query = f"""
        SELECT accident_category, SUM(total_accidents) AS total
        FROM accidents_by_vehicle
        WHERE region_name = '{region_filter}'
        GROUP BY accident_category
        ORDER BY total DESC;
    """
    vehicle_data = run_query(vehicle_query)

    if isinstance(vehicle_data, pd.DataFrame) and not vehicle_data.empty:
        fig = px.pie(
            vehicle_data,
            values="total",
            names="accident_category",
            title=f"Accidents by Vehicle Type in {region_filter} (2014-2023)",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected region.")

st.subheader("Total Accidents Over Time")

regions_data = run_query("""
    SELECT DISTINCT name, type 
    FROM regions 
    WHERE type IN ('kraj', 'województwo') 
    ORDER BY type, name;
""")

if isinstance(regions_data, pd.DataFrame) and not regions_data.empty:
    selected_regions = st.multiselect(
        "Select Regions",
        options=regions_data["name"].tolist(),
        default=["POLSKA"] 
    )

    if selected_regions:
        selected_regions_str = ",".join([f"'{region}'" for region in selected_regions])
        line_chart_query = f"""
            SELECT region_name, year, total_accidents
            FROM accidents_over_time
            WHERE region_name IN ({selected_regions_str})
            ORDER BY region_name, year;
        """
        line_chart_data = run_query(line_chart_query)

        if isinstance(line_chart_data, pd.DataFrame) and not line_chart_data.empty:
            min_year = int(line_chart_data["year"].min())
            max_year = int(line_chart_data["year"].max())
            year_range = st.slider(
                "Select Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                step=1
            )

            filtered_data = line_chart_data[
                (line_chart_data["year"] >= year_range[0]) &
                (line_chart_data["year"] <= year_range[1])
            ]

            if not filtered_data.empty:
                fig = px.line(
                    filtered_data,
                    x="year",
                    y="total_accidents",
                    color="region_name",
                    title="Total Accidents Over Time",
                    labels={"total_accidents": "Total Accidents", "year": "Year"},
                    markers=True
                )
                fig.update_traces(line=dict(width=2))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for the selected year range.")
        else:
            st.warning("No data available for the selected regions.")
else:
    st.error("Failed to load region data. Please check your database connection.")

st.subheader("SQL Query Executor 🛠️")

with st.expander("Write and Execute Custom SQL Queries", expanded=True):
    query_input = st.text_area(
        "Write your SQL query here:",
        placeholder="SELECT * FROM accidents_over_time WHERE year = 2023;",
        height=200
    )
    execute_button = st.button("Execute Query", key="execute_query")

    if execute_button and query_input.strip():
        try:
            query_result = run_query(query_input)
            if isinstance(query_result, pd.DataFrame) and not query_result.empty:
                st.success("Query executed successfully! 🎉")
                st.dataframe(query_result, use_container_width=True)
                csv_data = query_result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="💾 Download Results as CSV",
                    data=csv_data,
                    file_name="query_results.csv",
                    mime="text/csv",
                )
            elif isinstance(query_result, pd.DataFrame) and query_result.empty:
                st.warning("Query executed successfully, but returned no results.")
            else:
                st.error(f"Query execution error: {query_result}")
        except Exception as e:
            st.error(f"An error occurred while executing the query: {e}")

with st.expander("Example Queries", expanded=False):
    st.write("Here are some example queries you can try:")
    st.code("SELECT * FROM regions WHERE type = 'województwo';", language="sql")
    st.code("SELECT year, SUM(total_accidents) FROM accidents_over_time GROUP BY year;", language="sql")
    st.code("SELECT accident_category, SUM(total_accidents) FROM accidents_by_vehicle GROUP BY accident_category;", language="sql")

