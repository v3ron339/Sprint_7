import pytest
from generators import generate_fake_courier
from methods.courier_methods import CourierMethods


@pytest.fixture
def courier():
    # Генерация данных курьера
    courier_data = generate_fake_courier()

    # Создание курьера
    CourierMethods.create_courier(courier_data)

    yield courier_data

    # После теста удалиение курьера
    login = courier_data["login"]
    password = courier_data["password"]

    login_response = CourierMethods.login_courier(login, password)

    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            CourierMethods.delete_courier(courier_id)