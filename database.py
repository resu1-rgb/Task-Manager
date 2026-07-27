import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

url_database = os.getenv('DATABASE_URL', 'postgresql://resul:password@localhost/mydb')

engine = create_engine(url_database, echo=True)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()