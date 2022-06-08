from Base.Base_functions import wait_of_element_located, login_T4, choice_pipeline_mp, get_app_version
from Base.Dictionary_xpath import init_dict_xpath_login, init_dict_xpath_product_feed, init_dict_xpath_base
import allure


# Проверка выбор пайплайна и МП
@allure.feature('Базовое тестирование v.'+get_app_version())
@allure.story('2) Открытие пайплайна и выбор МП')
@allure.severity('critical')
def test_choice_pipeline(get_driver, get_init_data):
    """
    1) Авторизация в системе T4MP.v2
    2) Выбор пайплайна и МП
    """

    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)
    dict_xpath_product_feed = init_dict_xpath_product_feed(dict_init_data)
    dict_xpath_base = init_dict_xpath_base(dict_init_data)

    # 1) Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) Выбор пайплайна и МП
    choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed)

    # общая страница -> Feed Products (ожидание появления эллемента)
    product_feed = wait_of_element_located(dict_xpath_product_feed['15'], driver)
