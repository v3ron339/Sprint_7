import pytest
import allure
from generators import generate_fake_courier
from methods.courier_methods import CourierMethods
from data import Message


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        with allure.step('Создать валидные данные для курьера'):
            courier_data = generate_fake_courier()
            login = courier_data['login']
            password = courier_data['password']

        with allure.step('Отправить POST-запрос на создание курьера'):
            response = CourierMethods.create_courier(courier_data)

        with allure.step('Проверить, что статус-код 201 и возвращается {"ok": true}'):
            assert response.status_code == 201
            assert response.json() == {'ok': True}

        # Удаляем созданного курьера
        with allure.step('Удалить созданного курьера после проверки'):
            login_response = CourierMethods.login_courier(login, password)
            courier_id = login_response.json().get("id")
            CourierMethods.delete_courier(courier_id)

    @allure.title('Нельзя создать курьера с занятым логином')
    def test_create_courier_with_existing_login_conflict(self, courier):
        with allure.step('Получить данные уже созданного курьера'):
            login = courier["login"]
            password = courier["password"]

        with allure.step('Повторно отправить запрос на создание курьера с тем же логином'):
            response = CourierMethods.create_courier({
                'login': login,
                'password': password
            })

        with allure.step('Проверить, что статус-код 409 и корректное сообщение об ошибке'):
            assert response.status_code == 409
            assert Message.CREATE_COURIER_ALREADY_EXISTS in response.json().get('message')

    @pytest.mark.parametrize('field', ['login', 'password'])
    @allure.title('Нельзя создать курьера без обязательного поля login или password')
    def test_create_courier_without_required_field_error(self, field):
        with allure.step(f'Создать данные для курьера и удалить обязательное поле {field}'):
            courier_data = generate_fake_courier()
            del courier_data[field]

        with allure.step('Отправить POST-запрос на создание курьера'):
            response = CourierMethods.create_courier(courier_data)

        with allure.step('Проверить, что статус-код 400 и правильное сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json().get('message') == Message.CREATE_COURIER_MISSING_FIELDS