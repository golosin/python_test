from Base.Base_functions import wait_of_element_located, get_app_version, login_T4, choice_pipeline_mp
from Base.Dictionary_xpath import init_dict_xpath_login, init_dict_xpath_product_feed, init_dict_xpath_base
import allure
import time

# Функция загрузки YML feed
@allure.feature('Базовое тестирование'+get_app_version())
@allure.story('6) Создание/удаление YML фида')
@allure.severity('critical')
def test_create_delete_yml_feed(get_driver, get_init_data):
    """
     1) Авторизация в системе T4MP.v2
     2) Выбор пайплайна и МП
     3) Открытие "Feeds list"
     4) Нажатие кнопки "Add feed"
     5) Открытие списка "File type"
     6) Выбор типа "Yandex Feed"
     7) Заполнение поля "Name"
     8) Заполнение поля "Url products"
     9) Заполнение поля "Url prices"
    10) Заполнение поля "Url stocks"
    11) Нажатие кнопки "Save"
    12) Возврат на "Feeds list"
    13) Возврат в "Edit feed config"
    14) Проверка сохраненного "Url products"
    15) Проверка сохраненного "Url prices"
    16) Проверка сохраненного "Url stocks"
    17) Проверка сохраненного "Name" фида
    """


    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)
    dict_xpath_product_feed = init_dict_xpath_product_feed(dict_init_data)
    dict_xpath_base = init_dict_xpath_base(dict_init_data)

    # Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) Выбор пайплайна и МП
    choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed)

    # 3) общая страница -> Feeds list (клик)
    prod_feed = wait_of_element_located(dict_xpath_product_feed['1'], driver)
    prod_feed.click()

    # 4) Feeds list -> "Add feed" (клик)
    add_feed = wait_of_element_located(dict_xpath_product_feed['2'], driver)
    add_feed.click()

    # 5) Add feed config -> "File type" (клик)
    type_file = wait_of_element_located(dict_xpath_product_feed['7.0'], driver)
    type_file.click()

    # 6) Add feed config -> "File type" (Yandex Feed) (клик)
    type_file_yml = wait_of_element_located(dict_xpath_product_feed['7.2'], driver)
    type_file_yml.click()

    # 7) Add feed config -> "Name" (ввод)
    name_input = wait_of_element_located(dict_xpath_product_feed['3'], driver)
    name_input.send_keys(dict_init_data["yml_name_feed"])

    # 8) Add feed config -> "Url products" (ввод)
    url_input = wait_of_element_located(dict_xpath_product_feed['4'], driver)
    url_input.send_keys(dict_init_data["yml_url_location"])

    # 9) Add feed config -> "Url prices" (ввод)
    url_input = wait_of_element_located(dict_xpath_product_feed['5'], driver)
    url_input.send_keys(dict_init_data["yml_url_location"])

    # 10) Add feed config -> "Url stocks" (ввод)
    url_input = wait_of_element_located(dict_xpath_product_feed['6'], driver)
    url_input.send_keys(dict_init_data["yml_url_location"])

    # 11) Add feed config -> "Save" (клик)
    button_save_feed = wait_of_element_located(dict_xpath_product_feed['8'], driver)
    button_save_feed.click()

    # 12) Add feed config -> Feeds list (клик)
    arrow_left = wait_of_element_located(dict_xpath_product_feed['10'], driver)
    arrow_left.click()

    # 13) Feeds list -> Edit feed config (клик)
    table_edit = wait_of_element_located(dict_xpath_product_feed['12'], driver)
    table_edit.click()

    # 14) Проверка сохраненного "Url products"
    url_input = wait_of_element_located(dict_xpath_product_feed['4'], driver)
    val = url_input.get_attribute("value")
    assert val == dict_init_data["yml_url_location"]

    # 15) Проверка сохраненного "Url prices"
    url_input = wait_of_element_located(dict_xpath_product_feed['5'], driver)
    val = url_input.get_attribute("value")
    assert val == dict_init_data["yml_url_location"]

    # 16) Проверка сохраненного "Url stocks"
    url_input = wait_of_element_located(dict_xpath_product_feed['6'], driver)
    val = url_input.get_attribute("value")
    assert val == dict_init_data["yml_url_location"]

    # 17) Проверка сохраненного "Name" фида
    name_input = wait_of_element_located(dict_xpath_product_feed['3'], driver)
    val = name_input.get_attribute("value")
    assert val == dict_init_data["yml_name_feed"]