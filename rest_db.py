from database import engine, Base

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)
print('База данных сброшена!!')