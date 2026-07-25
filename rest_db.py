from database import Base, engine

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)
print("База данных сброшена!!")
