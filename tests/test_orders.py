import pytest
import allure
from data.test_data import TestData

class TestCreateOrder:
    @allure.title("Создание заказа с цветом: {color}")
    @allure.description("Проверяем создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("color", TestData.COLOR_VARIANTS)
    def test_create_order_with_different_colors(self, api_client, color):
        # Используем тестовые данные из data модуля
        order_data = TestData.BASE_ORDER_DATA.copy()
        order_data["color"] = color

        response = api_client.create_order(order_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data

class TestGetOrdersList:
    @allure.title("Получение списка заказов")
    @allure.description("Проверяем, что возвращается список заказов")
    def test_get_orders_list_returns_list(self, api_client):
        response = api_client.get_orders_list()

        assert response.status_code == 200
        response_data = response.json()

        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)