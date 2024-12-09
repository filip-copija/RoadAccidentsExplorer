from sqlalchemy import Column, Integer, String
from models.base import Base

# Model for the units table
class Unit(Base):
    __tablename__ = "units"

    unit_id = Column(Integer, primary_key=True)
    unit_name = Column(String(50), nullable=False, unique=True)
