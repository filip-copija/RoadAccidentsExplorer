from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# Model for the accidents table
class Accident(Base):
    __tablename__ = "accidents"

    accident_id = Column(Integer, primary_key=True)  # Unique accident ID
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)  # Foreign key to regions
    year = Column(Integer, nullable=False)          # Year of accident
    accident_type = Column(String(100), nullable=False)  # Type of accident
    value = Column(Integer, nullable=False)         # Value (e.g., number of accidents)
    unit = Column(String(20), nullable=False)       # Unit of measurement
