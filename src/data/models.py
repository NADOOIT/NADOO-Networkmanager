from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///input_data.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InputData(Base):
    __tablename__ = 'input_data'
    id = Column(String, primary_key=True)
    firmenname = Column(String)
    firmenbereich = Column(String)
    vorname = Column(String)
    nachname = Column(String)
    kontaktdaten = Column(String)
    kurzpraesentation = Column(String)
    naechster_vortrag = Column(String)
    vor_und_nachname = Column(String)


Base.metadata.create_all(engine)
