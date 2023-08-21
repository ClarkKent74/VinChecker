from fastapi import FastAPI

from backend.schemas import DefaultResponse
from DataBase import add, view, remove, view_all

app = FastAPI(
    title='Vin checker'
)


@app.post("/vin/add", response_model=DefaultResponse)
def add_vin(vin: str) -> DefaultResponse:
    """
    Добавляем vin в базу данных
    :param vin: вводим vin
    :return: DefaultResponse
    """
    response = add(vin)
    return response


@app.delete("/vin/delete", response_model=DefaultResponse)
def delete_vin(id: int) -> DefaultResponse:
    """
    Удаляем vin из базы данных
    :param id: вводим id
    :return: DefaultResponse
    """
    response = remove(id)
    return response


@app.get("/vin/view", response_model=DefaultResponse)
def view_info(id: int):
    """
    Просматриваем всю доступную информацию об автомобиле
    :param id: вводим id
    :return: DefaultResponse
    """
    response = view(id)
    return response


@app.get("/vin/view_all_vin", response_model=DefaultResponse)
def view_all_vin():
    """
    Просматриваем все vin номера из базы данных
    :return: DefaultResponse
    """
    response = view_all()
    return response
