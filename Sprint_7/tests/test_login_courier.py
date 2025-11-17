import pytest
import allure
from generators import generate_fake_courier
from methods.courier_methods import CourierMethods
from data import Message, TestData


@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, courier):
        with allure.step('Получить логин и пароль созданного курьера'):
            login = courier["login"]
            password = courier["password"]

        with allure.step('Отправить POST-запрос на авторизацию курьера'):
            response = CourierMethods.login_courier(login, password)

        with allure.step('Проверить, что статус-код 200 и в ответе есть id'):
            assert response.status_code == 200
            assert 'id' in response.json()
            assert isinstance(response.json()['id'], int)

    @allure.title('Нельзя авторизоваться без логина')
    def test_login_courier_without_login_error(self, courier):
        with allure.step('Получить пароль созданного курьера'):
            password = courier["password"]

        with allure.step('Отправить POST-запрос без логина'):
            response = CourierMethods.login_courier("", password)

        with allure.step('Проверить код 400 и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json().get("message") == Message.LOGIN_COURIER_MISSING_FIELDS

    @allure.title('Нельзя авторизоваться без пароля')
    def test_login_courier_without_password_error(self, courier):
        with allure.step('Получить логин созданного курьера'):
            login = courier["login"]

        with allure.step('Отправить POST-запрос без пароля'):
            response = CourierMethods.login_courier(login, "")

        with allure.step('Проверить код 400 и сообщение об ошибке'):
            assert response.status_code == 400
            assert response.json().get("message") == Message.LOGIN_COURIER_MISSING_FIELDS

    @allure.title('Нельзя авторизоваться с несуществующим логином')
    def test_login_courier_invalid_login_error(self, courier):
        with allure.step('Получить пароль созданного курьера'):
            password = courier["password"]

        with allure.step('Отправить POST-запрос с неверным логином'):
            response = CourierMethods.login_courier(TestData.NONEXISTENT_LOGIN, password)

        with allure.step('Проверить код 404 и сообщение «Курьер не найден»'):
            assert response.status_code == 404
            assert response.json().get("message") == Message.LOGIN_COURIER_NOT_FOUND

    @allure.title('Нельзя авторизоваться с несуществующим паролем')
    def test_login_courier_invalid_password_error(self, courier):
        with allure.step('Получить логин созданного курьера'):
            login = courier["login"]

        with allure.step('Отправить POST-запрос с неверным паролем'):
            response = CourierMethods.login_courier(login, TestData.NONEXISTENT_PASSWORD)

        with allure.step('Проверить код 404 и сообщение «Курьер не найден»'):
            assert response.status_code == 404
            assert response.json().get("message") == Message.LOGIN_COURIER_NOT_FOUND