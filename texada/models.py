from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import Float
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
   
    location_record = relationship("LocationRecord")


class LocationRecord(Base):
    __tablename__ = "location_record"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    elevation = Column(Integer, nullable=False)
   
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    
