# Sprint_7
Finalnyy proekt 7 sprinta - testirovaniye API Yandeks.Samokat

## Opisaniye proekta
Avtomatizirovannyye testy dlya API servisa "Yandeks.Samokat" s ispol'zovaniyem Python, pytest i Allure.

## Tekhnologii
- Python 3.13
- pytest 7.4.0
- Requests 2.32.5
- Allure-pytest 2.15.0

## Struktura proekta
Sprint_7/
├── tests/
│ ├── test_courier.py # Testy dlya kur'yerov (sozdaniye, login)
│ └── test_orders.py # Testy dlya zakazov (sozdaniye, spisok)
├── helpers/
│ ├── api_client.py # Klient dlya raboty s API
│ └── courier_generator.py # Generator testovykh dannykh
├── requirements.txt # Zavisimosti proekta
└── README.md # Dokumentatsiya

## Testovoye pokrytiye
- Sozdaniye kur'yera
- Login kur'yera
- Sozdaniye zakaza (s parametrizatsiyey tsvetov)
- Polucheniye spiska zakazov

## Zapusk testov
```bash
# Ustanovka zavisimostey
pip install -r requirements.txt

# Zapusk vsekh testov
pytest tests/ -v

# Zapusk s generatsiyey Allure-otchyota
pytest tests/ --alluredir=allure_results -v
allure serve allure_results

Protestirovannyye API endpointy
POST /api/v1/courier - Sozdaniye kur'yera
POST /api/v1/courier/login - Login kur'yera
POST /api/v1/orders - Sozdaniye zakaza
GET /api/v1/orders - Polucheniye spiska zakazov