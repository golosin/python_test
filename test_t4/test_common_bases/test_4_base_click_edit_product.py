from Base.Base_functions import wait_of_element_located, login_T4, choice_pipeline_mp, get_app_version
from Base.Dictionary_xpath import init_dict_xpath_login, init_dict_xpath_product_feed, init_dict_xpath_base
import allure

# Проверка открытия "Product feed" и 1-ой карточки товаров из списка
@allure.feature('Тест стенд v.'+get_app_version())
@allure.story('Базовое тестирование')
@allure.title('4) Открытие "Edit products" и 1-ой карточки товаров из списка')
@allure.severity('blocker')
def test_base_click_edit_product(get_driver, get_init_data):
    """
    1) Авторизация в системе T4MP.v2
    2) Выбор пайплайна и МП
    3) Открытие "Edit products"
    4) Открытие 1-ой карточки товаров из списка
    5) Возврат на страницу "Edit products"
    6) Возврат на страницу кубиков
    """

    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)
    dict_xpath_product_feed = init_dict_xpath_product_feed(dict_init_data)
    dict_xpath_base = init_dict_xpath_base(dict_init_data)

    # 1) Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) Выбор пайплайна и МП
    choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed, get_init_data)

    # 3) общая страница -> Edit Products (клик)
    product_feed = wait_of_element_located('выбор кубика "Edit Products"',
                                           dict_xpath_base['4'], driver)
    product_feed.click()

    # 4) Edit Products -> 1й товар карточка (клик)
    product_feed = wait_of_element_located('выбор 1ой карточки товара',
                                           dict_xpath_base['5'], driver)
    product_feed.click()

    # 5) 1й товар карточкаа -> Edit Products (клик)
    product_feed = wait_of_element_located('возврат на "Edit Products"',
                                           dict_xpath_base['3'], driver)
    product_feed.click()

    # 6) Edit Products -> общая страница (клик)
    product_feed = wait_of_element_located('выход из "Edit Products" на общую страницу',
                                           dict_xpath_base['3'], driver)
    product_feed.click()
