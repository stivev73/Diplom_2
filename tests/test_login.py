import allure
import requests

from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Проверка логин под существующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на логин в системе;
                        3. Проверяем ответ;
                        3. Удаляем пользователя.
                        ''')
    def test_login_user(self, create_new_user):
        with allure.step("Получить данные созданного пользователя из фикстуры"):
            response = create_new_user
            user_data = response[0]
    
        with allure.step("Отправить запрос на логин с учетными данными пользователя"):
            login = requests.post(
                URL.main_url + Endpoints.LOGIN,
                data=user_data
            )
    
        with allure.step("Проверить статус-код OK и success = True"):
            assert login.status_code == StatusCode.OK
            assert login.json().get("success") == True

    @allure.title('Проверка логин под несуществующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на логин в системе без регистрации;
                        2. Проверяем ответ.
                        ''')
    def test_login_under_none_user(self):
        with allure.step("Подготовить данные несуществующего пользователя"):
            incorrect_user_data = Person.create_data_incorrect_user_without_name()
            allure.attach(
                str(incorrect_user_data),
                "Данные несуществующего пользователя",
                allure.attachment_type.TEXT
            )
    
        with allure.step("Отправить запрос на логин с данными несуществующего пользователя"):
            login = requests.post(
                URL.main_url + Endpoints.LOGIN,
                data=incorrect_user_data
            )
    
        with allure.step("Проверить статус-код UNAUTHORIZED и success = False"):
            assert login.status_code == StatusCode.UNAUTHORIZED
            assert login.json().get("success") == False
