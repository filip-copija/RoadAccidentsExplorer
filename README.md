# Road Accidents Database Explorer 🚦

This project is a web-based application designed to explore and analyze road accident data from Poland. The data is sourced from the **GUS (Główny Urząd Statystyczny)** using their public datasets.

---

## 📊 Dataset Information

- **Source**: [GUS Database](https://bdl.stat.gov.pl/bdl/start)
- **Dataset**: `Wypadki drogowe i ich ofiary` (Road Accidents and Their Victims)

---

## 🎯 Project Goals

1. Build a database to store and manage road accident data.
2. Provide an interactive web interface for exploring data using SQL queries.
3. Enable visualizations to identify trends and patterns in accidents over time and across regions.
4. Offer a clean and professional data pipeline, starting from raw CSV files to a fully populated PostgreSQL database.

---

## 🛠️ Technologies Used

- **Frontend**:
  - `Streamlit` for creating a responsive and interactive web dashboard.
- **Backend**:
  - `PostgreSQL` for storing and querying data.
  - `SQLAlchemy` for ORM and database management.
- **Data Processing**:
  - `Pandas` for cleaning and preparing the dataset.

---

## 🚀 How to Set Up the Project

### 1. Clone the Repository
```bash
git clone https://github.com/filip-copija/pl_road_accidents
cd pl_road_accidents
```
### 2. Set Up the Python Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### 3. Configure `.env` Variable
### 4. Set Up the Database (sql 📂)
### 5. Run Data Loading Script
```bash
python scripts/load_data.py
```
### 6. Run streamlit webb application
```bash
streamlit run main.py
```
