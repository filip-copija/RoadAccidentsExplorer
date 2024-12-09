from sqlalchemy import Column, Integer, String
from models.base import Base

# Model for the accidents_types table
class AccidentType(Base):
    __tablename__ = "accident_types"

    accident_type_id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
