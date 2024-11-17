import sys
from pathlib import Path

# Add the root directory of the project to sys.path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Import models and other modules
from models.base import Base
from models.region import Region
from models.accident import Accident
from scripts.process_data import process_csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://postgres:admin@localhost:5432/road_accidents"

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