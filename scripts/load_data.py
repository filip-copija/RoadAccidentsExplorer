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
from scripts.process_data import process_csv

env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def load_data():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    csv_path = Path(__file__).parent.parent / "data" / "correct_accidents_2019_2024.csv"
    regions_data, accidents_data = process_csv(csv_path)

    for _, row in regions_data.iterrows():
        region = Region(name=row["Region"], type=row["Type"])
        session.add(region)

    session.commit()

    regions_mapping = {region.name: region.region_id for region in session.query(Region).all()}

    for _, row in accidents_data.iterrows():
        accident = Accident(
            region_id=regions_mapping[row["Region"]],
            year=int(row["Year"]),
            accident_type=row["Accident_Type"],
            value=int(row["Value"]),
            unit=row["Unit"]
        )
        session.add(accident)

    session.commit()
    print("Data successfully loaded into the database.")

if __name__ == "__main__":
    load_data()
