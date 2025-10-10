import requests
from requests.exceptions import HTTPError
import pytest
import allure
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_success_request(params):
    """
    :param headers: User-Agent одинаковый для запросов из search и reverse, можно посмотреть в Devtools, без него response_json не вернется
    :param params: у search принимаем параметр query; у reverse принмаем lon и lat
    :return: при неуспешном запросе(HTTPError,Exception)  возвращаем None, при успешном response.json()
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36'}

    try:
        with allure.step(f"Отправка запроса к {url}, с параметрами {params}"):
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            logging.info(f"Запрос к {url} успешен: статус {response.status_code}")
            allure.attach(str(params), name="url_params", attachment_type=allure.attachment_type.TEXT)
    except HTTPError as http_err:
        with allure.step(f"В ответ на запрос получили HTTP error: {http_err}"):
            allure.attach(str(http_err), name="HTTP Error", attachment_type=allure.attachment_type.TEXT)
            logging.error(f'HTTP error: {http_err}')
            return None
    except Exception as err:
        with allure.step(f"В ответ на запрос получили {err}"):
            logging.error(f'Other error: {err}')
            allure.attach(str(err), name="Other Error", attachment_type=allure.attachment_type.TEXT)
            return "None"
    else:
        if response.status_code == 200:
            with allure.step("Попытка получения response.json, status_response = 200"):
                response_json = response.json()
                allure.attach(json.dumps(response_json, indent=2), name="Response_json", attachment_type=allure.attachment_type.JSON)
                return response_json
        else:
            allure.attach(response.text, name="Not_200_response", attachment_type=allure.attachment_type.TEXT)
            return None

def search_geokoding(query):
    """
    :param query: запрос считываем из файлика test_data_searche.txt
    :return: в случае успешного получения response_json возвращаем долготу и широту в формате "lon lat" , иначе "None"
    """
    params = {"q": query, "format": "json"}  # параметры запроса
    response_json = check_success_request(params)
    if response_json:
            lon = response_json[0].get("lon")  # lon - Longitude ( долгота)
            lat = response_json[0].get("lat")  # lat - Latitude (широта)
            result = f"{lon} {lat}"
            allure.attach(result, name= f"Lon_lat {query}", attachment_type=allure.attachment_type.TEXT)
            return result
    else:
        allure.attach("None", name = f"Failed_lon_lat {query}", attachment_type=allure.attachment_type.TEXT)
        return "None"


def reverse_geokoding(lon, lat):
    """
    :param lon: считываем из файла с помощью функции load_test_data
    :param lat: считываем из файла с помощью функции load_test_data
    :return: name , если запрос response_json был успешен, в противном случае "None"
    """

    params = {"lon": lon, "lat": lat, "format": "json"}  # параметры запроса
    response_json = check_success_request(params)
    if response_json:
        with allure.step("Извлечение name из json"):
            print('Success!')
            name = response_json.get("name")
            allure.attach(str(name), name=f"Name {lon},{lat}", attachment_type=allure.attachment_type.TEXT)
            result = name
            return result
    else:
        allure.attach("None", name=f"Failed_name {lon},{lat}", attachment_type=allure.attachment_type.TEXT)
        return "None"

def load_test_data(file_path, Flag):
    """
    :param file_path: путь к файлу, из которого считываем входные данные и ожидаемый результат
    :param Flag: если True, то делим query на две строки по " " (в случае reverse, чтобы получить lon и lan), если False то не делим query достаточно(в случае searche)
    :return:test_data - список с тестовыми данными
    """
    # функция для считывания данных из файла и создания списка с парами значений запрос/ожидаемы результат
    test_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            parts = line.split(',')  # Делим строку запятой, создаем список parts из двух частей
            query = parts[0].strip()
            expected = parts[1].strip()
            if Flag == True:
                coordinat = query.split(" ") # создаем список из "lon lat" деля по пробелу
                lon = coordinat[0].strip() # 0 элемент списка coordinat это  lon
                lat = coordinat[1].strip() # 1 элемент списка coordinat это  lat
                test_data.append([lon, lat, expected])  # создаем список из взодных значений lon, lat и ожидаемого результата expected  для reverse
            else:
                test_data.append([query, expected])  # создаем список из пар-значений для search
    return test_data


