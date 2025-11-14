import pytest
import allure
from helpers.api_client import ScooterApiClient
from helpers.courier_generator import register_new_courier_and_return_login_password

@pytest.fixture
def api_client():
    return ScooterApiClient()

@pytest.fixture
def cleanup_courier(api_client):
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

@pytest.fixture
def create_courier(api_client, cleanup_courier):
    """Фикстура для создания курьера перед тестом"""
    @allure.step("Создать тестового курьера")
    def _create_courier():
        courier_data = register_new_courier_and_return_login_password()
        assert len(courier_data) == 3
        
        login, password, first_name = courier_data
        # Добавляем в список для удаления
        cleanup_courier.append([login, password])
        
        return login, password, first_name
    
    return _create_courier