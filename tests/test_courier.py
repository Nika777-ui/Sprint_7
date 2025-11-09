import pytest
import allure
from helpers.api_client import ScooterApiClient
from helpers.courier_generator import register_new_courier_and_return_login_password


class TestCreateCourier:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @pytest.fixture
    def cleanup_courier(self, api_client):
        """Фикстура для удаления курьеров после теста"""
        couriers_to_delete = []  # будем хранить [login, password]
        
        yield couriers_to_delete
        
        # После теста удаляем всех созданных курьеров
        for login, password in couriers_to_delete:
            # Получаем ID курьера через логин
            login_response = api_client.login_courier(login, password)
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                # Удаляем курьера
                delete_response = api_client.delete_courier(courier_id)
                # Проверяем что удаление успешно
                assert delete_response.status_code == 200

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        assert len(courier_data) == 3
        
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        login_response = api_client.login_courier(login, password)
        
        assert login_response.status_code == 200
        assert "id" in login_response.json()

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.create_courier(login, password, first_name)
        
        assert response.status_code == 409

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.create_courier("", password, first_name)
        assert response.status_code == 400

    @allure.title("Успешный запрос возвращает ok true")
    def test_create_courier_returns_ok_true(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        new_login = f"new_{login}"
        response = api_client.create_courier(new_login, password, first_name)
        
        # Добавляем нового курьера для удаления
        cleanup_courier.append([new_login, password])
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.create_courier(login, "", first_name)
        assert response.status_code == 400

    @allure.title("Можно создать курьера без имени")
    def test_create_courier_without_first_name_success(self, api_client, cleanup_courier):
        import random
        import string
        
        def generate_random_string(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        response = api_client.create_courier(login, password, "")
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}


class TestLoginCourier:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @pytest.fixture
    def cleanup_courier(self, api_client):
        """Фикстура для удаления курьеров после теста"""
        couriers_to_delete = []  # будем хранить [login, password]
        
        yield couriers_to_delete
        
        # После теста удаляем всех созданных курьеров
        for login, password in couriers_to_delete:
            # Получаем ID курьера через логин
            login_response = api_client.login_courier(login, password)
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                # Удаляем курьера
                delete_response = api_client.delete_courier(courier_id)
                # Проверяем что удаление успешно
                assert delete_response.status_code == 200

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.login_courier(login, password)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.login_courier(login, "wrong_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине несуществующего курьера")
    def test_login_nonexistent_courier_fails(self, api_client):
        response = api_client.login_courier("nonexistent_login", "any_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине без логина")
    def test_login_without_login_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.login_courier("", password)
        assert response.status_code == 400

    @allure.title("Ошибка при логине без пароля")
    def test_login_without_password_fails(self, api_client, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        response = api_client.login_courier(login, "")
        assert response.status_code == 400