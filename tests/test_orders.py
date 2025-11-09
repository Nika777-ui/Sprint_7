import pytest
import allure
from helpers.api_client import ScooterApiClient


class TestCreateOrder:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @allure.title("Создание заказа с цветом: {color}")
    @allure.description("Проверяем создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"], 
            ["BLACK", "GREY"],
            []
        ]
    )
    def test_create_order_with_different_colors(self, api_client, color):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Ленина, 1",
            "metroStation": 5,
            "phone": "+79999999999",
            "rentTime": 3,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ",
            "color": color
        }
        
        response = api_client.create_order(order_data)
        
        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data


class TestGetOrdersList:
    @pytest.fixture
    def api_client(self):
        return ScooterApiClient()

    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что возвращается список заказов")
    def test_get_orders_list_returns_list(self, api_client):
        response = api_client.get_orders_list()
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)