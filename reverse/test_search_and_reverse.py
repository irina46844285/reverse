import requests
from requests.exceptions import HTTPError
import pytest
import allure
from API_documentation import check_success_request
from API_documentation import search_geokoding
from API_documentation import reverse_geokoding
from API_documentation import load_test_data

# Прописываем путь к файлу с тестовыми данными path_search_test_data и path_reverse_test_data
path_search_test_data = "/home/litvinova-i/PycharmProjects/test1/tests/test_data_searche.txt"
path_reverse_test_data = "/home/litvinova-i/PycharmProjects/test1/tests/test_data_reverse.txt"
# В файле test_data_searche.txt лежат тестовые данные test_search : каждая строка "запрос,ожидаемый_результат" > (query, expected)
# В файле test_data_reverse.txt лежат тестовые данные test_reverse : координаты_через_пробел,ожидаемый_результат" > (lon, lat, expected)


# Загружаем тестовые данные из файлов для  test_search, test_reverse (указываем путь к .txt файлу c запросом и ожидаемыми результатами, и флаг False/True. Флаг он показыват, нужно ли делить часть слева от запятой еще на две части по " ", чтобы получить lon и lat (для reverse)
search_test_data = load_test_data( path_search_test_data, False)
reverse_test_data = load_test_data(path_reverse_test_data, True)

class TestSearchGeokoding:

    @allure.feature("search_geokoding")
    @pytest.mark.parametrize("test_data", search_test_data)
    def test_search(self, test_data):
        query, expected = test_data
        with allure.step("Отправка в параметрах запроса query, извлечение lon и lat из response_json"):
            result = search_geokoding(query)
        with allure.step("Сравнение полученных lon и lat с ожидаемым результатом"):
            allure.attach(f"Result: {result} VS Expected: {expected}", name="Assert_details", attachment_type=allure.attachment_type.TEXT)
            assert result == expected


class TestReverseGeokoding:


    @allure.feature("reverse_geokoding")
    @pytest.mark.parametrize("test_data", reverse_test_data)
    def test_reverse(self, test_data):
        lon, lat, expected = test_data
        with allure.step("Отправка в параметрах запроса lon и  lat, извлечение name из response_json "):
            result = reverse_geokoding(lon, lat)
        with allure.step("Сравнение полученного name  с ожидаемым результатом"):
            allure.attach(f"Result: {result} VS Expected: {expected}", name="Assert_details", attachment_type=allure.attachment_type.TEXT)
            assert result == expected

