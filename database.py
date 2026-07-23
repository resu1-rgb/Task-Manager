from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

url_database = 'postgresql://resul@localhost/mydb'

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