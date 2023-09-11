from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON

from sqlalchemy.orm import sessionmaker, declarative_base


from datetime import datetime
import pathlib
import json


db_file = pathlib.Path(__file__).parent.parent / 'app.sqlite3'

sqlite_addr = f"sqlite:///{db_file}"



Base = declarative_base()

engine = create_engine(sqlite_addr)
# delete table first, and then create table
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

data = Report()

session.add(data)
session.commit()