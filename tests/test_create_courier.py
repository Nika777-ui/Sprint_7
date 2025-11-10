import pytest
import allure
import random
import string
from data.test_data import TestData

class TestCreateCourier:
    def generate_random_string(self, length):
        """Генерирует случайную строку для тестовых данных"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, api_client, cleanup_courier):
        # Генерируем уникальные данные для курьера
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        # СОЗДАЕМ курьера и проверяем ответ
        response = api_client.create_courier(login, password, first_name)
        
        # Добавляем в cleanup для удаления после теста
        cleanup_courier.append([login, password])
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, api_client, cleanup_courier):
        # Сначала создаем курьера
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        first_response = api_client.create_courier(login, password, first_name)
        cleanup_courier.append([login, password])
        
        assert first_response.status_code == 201
        
        # Пытаемся создать такого же курьера второй раз
        second_response = api_client.create_courier(login, password, first_name)
        
        assert second_response.status_code == 409

    @allure.title("Создание курьера без обязательных полей")
    @pytest.mark.parametrize("invalid_data", TestData.INVALID_COURIER_DATA)
    def test_create_courier_without_required_fields_fails(self, api_client, invalid_data):
        response = api_client.create_courier(
            invalid_data["login"],
            invalid_data["password"], 
            invalid_data["first_name"]
        )
        assert response.status_code == 400

    @allure.title("Можно создать курьера без имени")
    def test_create_courier_without_first_name_success(self, api_client, cleanup_courier):
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)

        response = api_client.create_courier(login, password, "")

        # Добавляем в список для удаления
        cleanup_courier.append([login, password])

        assert response.status_code == 201
        assert response.json() == {"ok": True}