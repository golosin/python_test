from Base.Base_functions import wait_of_element_located, login_T4
from Base.Dictionary_xpath import init_dict_xpath_login
import allure

# Функция авторизации в системе
@allure.feature('Базовое тестирование')
@allure.story('1) Авторизация в системе T4MP.v2')
@allure.severity('blocker')
def test_login(get_driver, get_init_data):
# def test_login():
    """
    1) Авторизация в системе T4MP.v2
    2) Переход к листингу пайплайнов
    """


    # assert  1==1
    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)


    # 1) Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) T4MP -> Pipelines (ожидание появления эллемента)
    pipl = wait_of_element_located(dict_xpath_login['3'], driver)
