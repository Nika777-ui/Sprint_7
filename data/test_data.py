class TestData:
    """Тестовые данные для создания заказов"""
    
    # Базовые данные для заказа
    BASE_ORDER_DATA = {
        "firstName": "Иван",
        "lastName": "Иванов", 
        "address": "Москва, ул. Ленина, 1",
        "metroStation": 5,
        "phone": "+79999999999",
        "rentTime": 3,
        "deliveryDate": "2024-12-31",
        "comment": "Тестовый заказ"
    }
    
    # Варианты цветов для параметризации
    COLOR_VARIANTS = [
        ["BLACK"],
        ["GREY"], 
        ["BLACK", "GREY"],
        []
    ]
    
    # Данные для негативных тестов создания курьера
    INVALID_COURIER_DATA = [
        {"login": "", "password": "password123", "first_name": "Иван"},  # без логина
        {"login": "login123", "password": "", "first_name": "Иван"},     # без пароля
    ]
    
    # Данные для негативных тестов логина курьера  
    INVALID_LOGIN_DATA = [
        {"login": "", "password": "password123"},     # без логина
        {"login": "login123", "password": ""},        # без пароля
        {"login": "wrong_login", "password": "pass"}, # неверный логин
        {"login": "login123", "password": "wrong"}    # неверный пароль
    ]