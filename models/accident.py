from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

# Model for the accidents table
class Accident(Base):
    __tablename__ = "accidents"

    accident_id = Column(Integer, primary_key=True)  
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False) 
    year = Column(Integer, nullable=False)        
    accident_type_id = Column(Integer, ForeignKey("accident_types.accident_type_id"), nullable=False)
    value = Column(Integer, nullable=True)      
    unit_id = Column(Integer, ForeignKey("units.unit_id"), nullable=True)
