from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.constants import DATABASE_URL
from src.utils import ensure_directory_exists

# Ensure the directory exists
ensure_directory_exists("data/db")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class PresentationSlide(Base):
    __tablename__ = 'presentation_slides'
    ID = Column(Integer, primary_key=True)
    Folientitel = Column(String)
    Firmenname = Column(String)
    Unternehmensbranche = Column(String)
    Kontaktdaten = Column(String)
    Vortragszeit = Column(String)
    Vorname = Column(String)
    Nachname = Column(String)
    Naechster_vortrag = Column(String)


Base.metadata.create_all(engine)
