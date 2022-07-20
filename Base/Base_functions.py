from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import requests
import allure
from typing import List


# Функция ожидания элементов
@ allure.step('Действие: {description}')
def wait_of_elements_located(description, xpath, driver_init) -> List[WebElement]:
    elements = WebDriverWait(driver_init, 15).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, xpath)
        )
    )
    return elements


# Функция ожидания элемента
@ allure.step('Действие: {description}')
def wait_of_element_located(description, xpath, driver_init) -> WebElement:
    element = WebDriverWait(driver_init, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


# Ожидаемое условие для проверки того, что элемент либо невидим, либо отсутствует в DOM веб-страницы
@ allure.step('Действие: {description}')
def wait_of_invisibility_of_element_located(description, xpath, driver_init) -> WebElement:
    element = WebDriverWait(driver_init, 15).until(
        EC.invisibility_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


# Поиск текста в элементе
@ allure.step('Действие: {description}')
def find_text_in_element(description, xpath, driver_init, text) -> WebElement:
    element = WebDriverWait(driver_init, 300).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, xpath),
            text
        )
    )
    return element


# Функция авторизации в системе
def login_T4(driver, dict_init_data, dict_xpath_login):
    # T4MP -> "Email" (ввод)
    email_input = wait_of_element_located('ввод в поле "Email"',
                                          dict_xpath_login['0'], driver)
    email_input.send_keys(dict_init_data["email"])

    # T4MP -> "Password" (ввод)
    password_input = wait_of_element_located('ввод в поле "Password"',
                                             dict_xpath_login['1'], driver)
    password_input.send_keys(dict_init_data["password"])

    # T4MP -> "Sing in" (клик)
    login_button = wait_of_element_located('нажатие кнопки "Sing in"',
                                           dict_xpath_login['2'], driver)
    login_button.click()


# Выбор пайплайна и МП
def choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed):
    # листинг пайплайнов -> заданный пайплайн
    login_button = wait_of_element_located('выбор указанного пайплайна',
                                           dict_xpath_product_feed['0'], driver)
    login_button.click()

    # общая стр пайплайна -> Wildberries (клик)
    product_feed = wait_of_element_located('выбор МП "Wildberries"',
                                           dict_xpath_base['1'], driver)
    product_feed.click()


# Версия билда
def get_app_version():
    query = """query{
            appVersion{
                appVersion
            }
        }
        """
    headers = {"Content-Type": "application/json; charset=utf-8",
               "cookie": "csrftoken=DA9y74VS0SKQyDPhwvkPa54Q6365XZIw2QTI8wfl5a5W21HHSnWtxZHkEDkj5Dm4; sessionid=qkqlrryw6uive8faq3x18uf0mr0p4noi"}
    url = 'https://test.app.market4.place/graphql'
    response = requests.post(url, headers=headers, json={'query': query})
    response_body = response.json()
    return response_body['data']['appVersion']['appVersion']


# Получение стоков, прайсов и дисконта у WB
def get_WB_stock_price_discount(imtID):

    # Медиа 2.0
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjljMjk3YjlmLTcxNTctNGFlZC05NmI0LTVjNDU1MWRjMjk3MiJ9.W6Rkfr3RHx6e1cuJFbHp2hwYHxl6w448of_Mxnai73A'
    supplierID = "74c22891-16b9-47c7-8e22-6ba834aa5947"

    url = 'https://suppliers-api.wildberries.ru/'
    headers = {
        'accept': 'application/json',
        'Authorization': token,
        'Content-Type': 'application/json',
    }

    # Получение баркода
    uri = 'card/cardByImtID'
    body = {
        "jsonrpc": "2.0",
        "params": {
            "imtID": imtID,
            "supplierID": supplierID
        }
    }
    response = requests.post(url + uri, headers=headers, json=body)
    response_body = response.json()
    barcode = response_body['result']['card']['nomenclatures'][0]['variations'][0]['barcodes'][0]  # Баркод
    nomenclature = response_body['result']['card']['nomenclatures'][0]['nmId']  # Номенклатура
    name_prod = response_body['result']['card']['addin'][1]['params'][0]['value']
    print("id - " + str(imtID))
    print("Баркод - " + barcode)
    print("Номенклатура - " + str(nomenclature))
    print(name_prod)

    # Получение стоков по баркоду
    uri = 'api/v2/stocks'
    params = {
        'search': barcode,
        'skip': '0',
        'take': '1000'
    }
    response = requests.get(url + uri, headers=headers, params=params)
    response_body = response.json()
    stock = response_body['stocks'][0]['stock']  # Стоки
    warehouse_name = response_body['stocks'][0]['warehouseName']  # Склад
    print("Стоки - " + str(stock))
    print("Склад - " + warehouse_name)

    # Получение цен и скидок для все товаров
    uri = '/public/api/v1/info'
    params = {
        "quantity": "0",  # 2 - товар с нулевым остатком, 1 - товар с ненулевым остатком, 0 - товар с любым остатком
    }
    response = requests.get(url + uri, headers=headers, params=params)
    response_body = response.json()
    for product in response_body:
        if product['nmId'] == nomenclature:
            price = product['price']  # Прайс
            discount = product['discount']  # Скидка
            print("Прайс - " + str(price))
            print("Скидка - " + str(discount))

    return [price, stock]