import requests


class ScooterApiClient:
    """Клиент для работы с API Яндекс.Самокат"""
    
    def __init__(self):
        self.base_url = "https://qa-scooter.praktikum-services.ru/api/v1"
    
    def create_courier(self, login, password, first_name):
        """Создание курьера"""
        payload = {
            "login": login,
            "password": password, 
            "firstName": first_name
        }
        response = requests.post(f"{self.base_url}/courier", data=payload)
        return response
    
    def login_courier(self, login, password):
        """Логин курьера"""
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f"{self.base_url}/courier/login", data=payload)
        return response
    
    def create_order(self, order_data):
        """Создание заказа"""
        response = requests.post(f"{self.base_url}/orders", json=order_data)
        return response
    
    def get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(f"{self.base_url}/orders")
        return response
    
    def delete_courier(self, courier_id):
        """Удаление курьера по ID"""
        response = requests.delete(f"{self.base_url}/courier/{courier_id}")
        return response