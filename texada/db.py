from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import contextmanager

Base = declarative_base()

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
engine = create_engine(MYSQL_URL).connect() 
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
