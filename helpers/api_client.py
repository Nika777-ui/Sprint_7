import requests
import allure
from data.urls import Urls

class ScooterApiClient:
    """Клиент для работы с API Яндекс.Самокат"""

    def __init__(self):
        self.base_url = Urls.BASE_URL

    @allure.step("Создать курьера")
    def create_courier(self, login, password, first_name):
        """Создание курьера"""
        payload = {
            "login": login,
            "password": password, 
            "firstName": first_name
        }
        response = requests.post(f"{self.base_url}{Urls.COURIER}", data=payload)
        return response

    @allure.step("Залогинить курьера")
    def login_courier(self, login, password):
        """Логин курьера"""
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{self.base_url}{Urls.COURIER_LOGIN}", data=payload)
        return response

    @allure.step("Создать заказ")
    def create_order(self, order_data):
        """Создание заказа"""
        response = requests.post(f"{self.base_url}{Urls.ORDERS}", json=order_data)
        return response

    @allure.step("Получить список заказов")
    def get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(f"{self.base_url}{Urls.ORDERS}")
        return response

    @allure.step("Удалить курьера по ID: {courier_id}")
    def delete_courier(self, courier_id):
        """Удаление курьера по ID"""
        response = requests.delete(f"{self.base_url}{Urls.COURIER}/{courier_id}")
        return response