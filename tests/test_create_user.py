import pytest
import allure
import requests

from data.text_response import TextResponse
from helpers.helpers import Person
from data.status_code import StatusCode
from data.urls import URL, Endpoints


class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Проверяем ответ;
                        3. Удаляем пользователя.
                        ''')
    def test_create_user(self, create_new_user):
        with allure.step("Получить ответ от фикстуры create_new_user"):
        response = create_new_user
    
        with allure.step("Проверить статус-код и наличие success в ответе"):
            assert response[1].json().get("success") == True
            assert response[1].status_code == StatusCode.OK

    @allure.title('Проверка создания дублирующего пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Получаем данные для регистрации;
                        3. Отправляем повторный запрос на создание пользователя;
                        4. Проверяем ответ;
                        5. Удаляем пользователя.
                        ''')
    def test_create_double_user(self, create_new_user):
        with allure.step("Получить данные созданного пользователя из фикстуры"):
        response = create_new_user
        payload = response[0]
    
        with allure.step("Отправить запрос на повторное создание того же пользователя"):
        response_double_register = requests.post(
            URL.main_url + Endpoints.CREATE_USER,
            data=payload
        )
    
        with allure.step("Проверить статус-код FORBIDDEN и сообщение об ошибке"):
            assert response_double_register.status_code == StatusCode.FORBIDDEN
            assert response_double_register.json().get("message") == TextResponse.CREATE_DOUBLE_USER

    @allure.title('Проверка создания некорректного пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя с некорректными данными;
                        2. Проверяем ответ.
                        ''')
    @pytest.mark.parametrize('payload', [
        Person.create_data_incorrect_user_without_email(),
        Person.create_data_incorrect_user_without_name(),
        Person.create_data_incorrect_user_without_password()
    ])
    def test_create_user_incorrect_data(self, payload):
        with allure.step("Подготовка некорректных данных для создания пользователя"):
        allure.attach(
            str(payload),
            "Некорректные данные",
            allure.attachment_type.TEXT
        )
    
        with allure.step("Отправить запрос на создание пользователя с некорректными данными"):
        response = requests.post(
            URL.main_url + Endpoints.CREATE_USER,
            data=payload
        )
    
        with allure.step("Проверить статус-код FORBIDDEN и success = False"):
            assert response.status_code == StatusCode.FORBIDDEN
            assert response.json().get("success") == False
