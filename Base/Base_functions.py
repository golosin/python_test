from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import allure


# Функция ожидания элементов
@ allure.step('Действие: {description}')
def wait_of_element_located(description, xpath, driver_init):
    element = WebDriverWait(driver_init, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


# Ожидаемое условие для проверки того, что элемент либо невидим, либо отсутствует в DOM веб-страницы
def wait_of_invisibility_of_element_located(xpath, driver_init):
    element = WebDriverWait(driver_init, 15).until(
        EC.invisibility_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


# Поиск текста в элементе
def find_text_in_element(xpath, driver_init, text):
    element = WebDriverWait(driver_init, 15).until(
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