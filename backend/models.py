import sqlalchemy as sa
import os

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
Base = declarative_base()

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Vin(Base):
    """
    Класс для таблицы с vin номерами автомобиля
    """
    __tablename__ = "vin"
    id = Column(Integer, primary_key=True, index=True)
    vin_number = Column(String)


class Characteristics(Base):
    """
    Класс для таблицы с характеристиками автомобиля
    """
    __tablename__ = "characteristics"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    year = Column(String)
    category = Column(String)
    wheel_position = Column(String)
    type_engine = Column(String)
    power_engine = Column(String)
    volume_engine = Column(String)


def init_models():
    """
    Функция для подключения к базе данных.
    """
    Base.metadata.create_all(bind=engine)


init_models()
