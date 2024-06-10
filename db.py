from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)
