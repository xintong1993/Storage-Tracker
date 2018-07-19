from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import Float
from os import environ
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    datetime = Column(String, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    elevation = Column(Integer, nullable=False)

from sqlalchemy import create_engine

MYSQL_USER = environ.get("MYSQL_USER", "root")
MYSQL_PW = environ["MYSQL_PW"]
MYSQL_HOST = environ.get("MYSQL_HOST", "localhost")
MYSQL_DB = environ.get("MYSQL_DB", "texada")

MYSQL_URL = "mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8&use_unicode=0" \
			.format(
				user=MYSQL_USER,
				pw=MYSQL_PW,
				host=MYSQL_HOST,
				db=MYSQL_DB,
			)
engine = create_engine(MYSQL_URL) 
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
