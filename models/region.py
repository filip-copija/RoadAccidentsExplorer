from sqlalchemy import Column, Integer, String
from models.base import Base

# Model for the regions table
class Region(Base):
    __tablename__ = "regions"

    region_id = Column(Integer, primary_key=True) 
    name = Column(String(255), nullable=False)   
    type = Column(String(50), nullable=False)      
