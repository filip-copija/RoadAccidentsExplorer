from sqlalchemy import Column, Integer, String
from models.base import Base

# Model for the regions table
class Region(Base):
    __tablename__ = "regions"

    region_id = Column(Integer, primary_key=True)  # Unique region ID
    name = Column(String(255), nullable=False)     # Region name
    type = Column(String(50), nullable=False)      # Region type (e.g., province, city)
