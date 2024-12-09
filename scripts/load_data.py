import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.region import Region
from models.accident import Accident
from models.accident_type import AccidentType
from models.unit import Unit
import pandas as pd

env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def clean_value(value):
    """Convert value to an integer or return None if invalid."""
    try:
        return int(value)
    except ValueError:
        return 0  # It should be empty here

def add_context_to_overall(data, column_name, context):
    data[column_name] = data[column_name].apply(
        lambda x: f"ogółem_{context}" if x == "ogółem" else x
    )
    return data

def load_data():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    processed_dir = root_dir / "data" / "processed_data"
    accident_files = [
        "correct_raw_road_accidents_and_their_victims_1999_2023.csv",
        "correct_raw_road_accidents_by_major_causes_2014_2023.csv",
        "correct_raw_road_accidents_intoxicated_road_users_2014_2023.csv",
        "correct_raw_road_accidents_wehicle_type_2014_2023.csv"
    ]

    for file_name in accident_files:
        print(f"Processing file: {file_name}")
        file_path = processed_dir / file_name
        data = pd.read_csv(file_path, delimiter=";")

        if "Wypadki drogowe" in data.columns:
            data = add_context_to_overall(data, "Wypadki drogowe", "wypadki")
        if "Ważniejsze przyczyny wypadków" in data.columns:
            data = add_context_to_overall(data, "Ważniejsze przyczyny wypadków", "przyczyny")
        if "Nietrzeźwi sprawcy" in data.columns:
            data = add_context_to_overall(data, "Nietrzeźwi sprawcy", "nietrzeźwi")
        if "Wypadki drogowe według pojazdu sprawcy" in data.columns:
            data = add_context_to_overall(data, "Wypadki drogowe według pojazdu sprawcy", "pojazdy")

        if "Wartosc" in data.columns:
            data["Wartosc"] = data["Wartosc"].apply(clean_value)

        for _, row in data.iterrows():
            region = Region(
                name=row["Nazwa"],
                type=row["Region_Type"]
            )
            region_obj = session.query(Region).filter_by(name=region.name, type=region.type).first()
            if not region_obj:
                region_obj = session.merge(region)

            if "Wypadki drogowe" in data.columns:
                accident_type = AccidentType(
                    category=row["Wypadki drogowe"]
                )
            elif "Ważniejsze przyczyny wypadków" in data.columns:
                accident_type = AccidentType(
                    category=row["Ważniejsze przyczyny wypadków"]
                )
            elif "Nietrzeźwi sprawcy" in data.columns:
                accident_type = AccidentType(
                    category=row["Nietrzeźwi sprawcy"]
                )
            elif "Wypadki drogowe według pojazdu sprawcy" in data.columns:
                accident_type = AccidentType(
                    category=row["Wypadki drogowe według pojazdu sprawcy"]
                )
            else:
                continue

            accident_type_obj = session.query(AccidentType).filter_by(category=accident_type.category).first()
            if not accident_type_obj:
                accident_type_obj = session.merge(accident_type)

            unit_name = row["Jednostka miary"] if pd.notna(row["Jednostka miary"]) else None
            unit_obj = None
            if unit_name:
                unit = Unit(unit_name=unit_name)
                unit_obj = session.query(Unit).filter_by(unit_name=unit.unit_name).first()
                if not unit_obj:
                    unit_obj = session.merge(unit)

            accident = Accident(
                region_id=region_obj.region_id,
                year=row["Rok"],
                accident_type_id=accident_type_obj.accident_type_id,
                value=row["Wartosc"],
                unit_id=unit_obj.unit_id if unit_obj else None
            )
            session.add(accident)

    session.commit()
    print("Data successfully loaded into the database.")

if __name__ == "__main__":
    load_data()