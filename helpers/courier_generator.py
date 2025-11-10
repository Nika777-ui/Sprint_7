import requests
import random
import string

def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def register_new_courier_and_return_login_password():
    """Регистрация нового курьера и возврат логина, пароля и имени"""
    login_pass = []
    
    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    # отправляем запрос на регистрацию курьера
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    
    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    
    # возвращаем список
    return login_pass