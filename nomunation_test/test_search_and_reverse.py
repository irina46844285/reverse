import requests
from requests.exceptions import HTTPError
import pytest
import allure
from API_documentation import check_success_request
from API_documentation import search_geokoding
from API_documentation import reverse_geokoding
from API_documentation import load_test_data


class TestSearchGeokoding:
    file_path = r"C:/Users/litvi/PycharmProjects/PythonProject/nomunation_test/test_data_searche.txt" #Прописываем путь к файлу test_data_searche.txt с тестовыми данными
    test_data = load_test_data( file_path, False) #  В файле test_data_searche.txt лежат тестовые данные test_search : каждая строка "запрос,ожидаемый_результат" > (query, expected)
    url = "https://nominatim.openstreetmap.org/search" # url для отправки запроса


    @allure.feature("search_geokoding")
    @pytest.mark.parametrize("test_data", test_data)
    def test_search(self, test_data):
        query, expected = test_data
        with allure.step("Отправка в параметрах запроса query, извлечение lon и lat из response_json"):
            result = search_geokoding(query)
        with allure.step("Сравнение полученных lon и lat с ожидаемым результатом"):
            allure.attach(f"Result: {result} VS Expected: {expected}", name="Assert_details", attachment_type=allure.attachment_type.TEXT)
            assert result == expected


class TestReverseGeokoding:
    file_path = " "  #Прописываем путь к файлу test_data_reverse.txt  с тестовыми данными
    test_data = load_test_data(file_path, True) # В файле test_data_reverse.txt лежат тестовые данные test_reverse : координаты_через_пробел,ожидаемый_результат" > (lon, lat, expected)
    url = "https://nominatim.openstreetmap.org/reverse" # url для отправки запроса



    @allure.feature("reverse_geokoding")
    @pytest.mark.parametrize("test_data", test_data)
    def test_reverse(self, test_data):
        lon, lat, expected = test_data
        with allure.step("Отправка в параметрах запроса lon и  lat, извлечение name из response_json "):
            result = reverse_geokoding(lon, lat)
        with allure.step("Сравнение полученного name  с ожидаемым результатом"):
            allure.attach(f"Result: {result} VS Expected: {expected}", name="Assert_details", attachment_type=allure.attachment_type.TEXT)
            assert result == expected

