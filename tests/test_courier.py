import pytest
import allure
from helpers.api_client import ScooterApiClient
from helpers.courier_generator import register_new_courier_and_return_login_password


class TestCreateCourier:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @allure.title("Успешное создание курьера")
    @allure.description("Проверяем, что курьера можно создать с валидными данными")
    def test_create_courier_success(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        assert len(courier_data) == 3
        
        login, password, first_name = courier_data
        login_response = api_client.login_courier(login, password)
        
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.create_courier(login, password, first_name)
        
        assert response.status_code == 409

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.create_courier("", password, first_name)
        assert response.status_code == 400

    @allure.title("Успешный запрос возвращает ok true")
    def test_create_courier_returns_ok_true(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        new_login = f"new_{login}"
        response = api_client.create_courier(new_login, password, first_name)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.create_courier(login, "", first_name)
        assert response.status_code == 400

    @allure.title("Можно создать курьера без имени")
    def test_create_courier_without_first_name_success(self, api_client):
        import random
        import string
        
        def generate_random_string(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = api_client.create_courier(login, password, "")
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}


class TestLoginCourier:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.login_courier(login, password)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.login_courier(login, "wrong_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине несуществующего курьера")
    def test_login_nonexistent_courier_fails(self, api_client):
        response = api_client.login_courier("nonexistent_login", "any_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине без логина")
    def test_login_without_login_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.login_courier("", password)
        assert response.status_code == 400

    @allure.title("Ошибка при логине без пароля")
    def test_login_without_password_fails(self, api_client):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        response = api_client.login_courier(login, "")
        assert response.status_code == 400  