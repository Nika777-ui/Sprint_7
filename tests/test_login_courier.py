import pytest
import allure
from data.test_data import TestData

class TestLoginCourier:
    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self, api_client, create_courier):
        login, password, first_name = create_courier()
        
        response = api_client.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password_fails(self, api_client, create_courier):
        login, password, first_name = create_courier()
        
        response = api_client.login_courier(login, "wrong_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине несуществующего курьера")
    def test_login_nonexistent_courier_fails(self, api_client):
        response = api_client.login_courier("nonexistent_login", "any_password")
        assert response.status_code == 404

    @allure.title("Ошибка при логине без обязательных полей")
    @pytest.mark.parametrize("invalid_data", TestData.INVALID_LOGIN_DATA[:2])  # только первые 2 случая
    def test_login_without_required_fields_fails(self, api_client, invalid_data, create_courier):
        # Создаем курьера, но используем invalid_data для запроса
        response = api_client.login_courier(
            invalid_data["login"],
            invalid_data["password"]
        )
        assert response.status_code == 400