import logging

from sqlalchemy import select

from backend.helpers import VinParser, ru_to_en
from backend.models import SessionLocal
from backend.models import (
    Vin,
    Characteristics
)
from backend.schemas import DefaultResponse


def add(vin: str) -> DefaultResponse:
    """
    Добавляем автомобиль по vin в базу данных
    :param vin: вводим vin автомобиля
    :return: DefaultResponse
    """
    try:
        with SessionLocal() as session:
            vin = ru_to_en(vin)
            vin_check = session.query(Vin.id).filter(Vin.vin_number == vin).first()
            if vin_check:
                response = DefaultResponse(error=True, message="введено некорректное значение"
                                                               " или Vin уже существует в базе", payload=None)
            else:
                vin_parser = VinParser(vin)
                vin_data = vin_parser.parse()
                vin_number = Vin(vin_number=vin)
                vin_info = Characteristics(model=vin_data['Model'],
                                           year=vin_data['Year'],
                                           category=vin_data['Category'],
                                           wheel_position=vin_data['Wheel position'],
                                           type_engine=vin_data['Type engine'],
                                           power_engine=vin_data['Power engine'],
                                           volume_engine=vin_data['Volume engine'])
                session.add(vin_number)
                session.add(vin_info)
                session.commit()
                response = DefaultResponse(error=False, message="Vin успешно добавлен", payload=None)

    except Exception as err:
        logging.error("Exception", exc_info=True)
        response = DefaultResponse(error=True, message="введено некорректное значение"
                                                       " или Vin уже существует в базе", payload=None)
    return response


def remove(id: int) -> DefaultResponse:
    """
    Удаляем автомобиль из базы данных по id
    :param id: вводим id автомобиля
    :return: DefaultResponse
    """
    try:
        with SessionLocal() as session:
            vin_check = session.query(Vin.id).filter(Vin.id == id).first()
            vin_exist = bool(vin_check[0])
            if not vin_exist:
                response = DefaultResponse(error=True, message="введено некорректное значение"
                                                               " или Vin не существует в базе", payload=None)
            else:
                vin_rm = session.query(Vin).filter(Vin.id == id).delete()
                characteristics_rm = session.query(Characteristics).filter(Characteristics.id == id).delete()
                session.commit()
                response = DefaultResponse(error=False, message="Vin успешно удален", payload=None)
    except Exception as err:
        logging.error("Exception", exc_info=True)
        response = DefaultResponse(error=True, message="введено некорректное значение"
                                                       " или Vin уже существует в базе", payload=None)
    return response


def view(id: int) -> DefaultResponse:
    """
    Просматриваем всю доступную информацию об автомобиле по id
    :param id: вводим id
    :return: DefaultResponse
    """
    try:
        with SessionLocal() as session:
            id_check = session.query(Vin.id).filter(Vin.id == id).first()
            if id_check:
                data = session.execute(select(Vin.vin_number, Characteristics.model, Characteristics.year,
                                              Characteristics.category, Characteristics.wheel_position,
                                              Characteristics.type_engine, Characteristics.power_engine,
                                              Characteristics.volume_engine)
                                       .join(Characteristics, Vin.id == Characteristics.id)
                                       .filter(Vin.id == id)).first()

                result = {
                    'Vin': data.vin_number,
                    'Model': data.model,
                    'Year': data.year,
                    'Category': data.category,
                    'Wheel position': data.wheel_position,
                    'Type engine': data.type_engine,
                    'Power engine': data.power_engine,
                    'Volume engine': data.volume_engine

                }
                response = DefaultResponse(error=False, message="OK", payload=result)
            else:
                response = DefaultResponse(error=True, message="введено некорректное значение"
                                                               " или Vin не существует в базе", payload=None)
    except Exception as err:
        logging.error("Exception", exc_info=True)
        response = DefaultResponse(error=True, message="введено некорректное значение"
                                                       " или Vin не существует в базе", payload=None)
    return response


def view_all() -> DefaultResponse:
    """
    Просматриваем все vin номера, находящиеся в базе данных.
    :return: DefaultResponse
    """
    try:
        with SessionLocal() as session:
            result = session.execute(select(Vin.vin_number)).all()
            print(result)
            vin_list = [vin_number[0] for vin_number in result]
            if vin_list:
                response = DefaultResponse(error=False, message="Ok", payload=vin_list)
            else:
                response = DefaultResponse(error=False, message="Ok", payload="Ни одного vin пока не добавлено.")
    except Exception as err:
        logging.error("Exception", exc_info=True)
        response = DefaultResponse(error=True, message="введено некорректное значение"
                                                       " или Vin не существует в базе", payload=None)
    return response
