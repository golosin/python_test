from selenium.webdriver.common.keys import Keys
from Base.Base_functions import wait_of_element_located, get_app_version, login_T4, choice_pipeline_mp, \
    wait_of_invisibility_of_element_located, find_text_in_element, get_WB_stock_price_discount
from Base.Dictionary_xpath import init_dict_xpath_login, init_dict_xpath_product_feed, init_dict_xpath_base
from Base.parse_yml_feed import parsing_data_feed
import allure
import time
from datetime import datetime

# Функция загрузки YML feed
@allure.feature('Тест стенд v.'+get_app_version())
@allure.story('Функциональное тестирование')
@allure.title('8) Изменение цен/остатков на WB через YML feed')
@allure.severity('critical')
def test_add_feed_checkin_feed_product(get_driver, get_init_data):
    """
     1) Авторизация в системе T4MP.v2
     2) Выбор пайплайна и МП
     3) Открытие "Feed Products"
     4) Ввод в поле "Search" ID тестового товара
     5) Проверка значения "id" в таблице для тестового товара
     6) Получение значения "Sale" в таблице для тестового товара'
     7) Получение значения "Stock" в таблице для тестового товара'
     8) Запрос к API WB, получение "price" и "stock"
     9) Исходя из текущего "price" и "stock" выбор "YML feed" для изменения цен и остатков
    10) Возврат на страницу кубиков
    11) Открытие "Feeds list"
    12) Выбор "WB feed"
    13) Открытие списка "File type"
    14) Выбор типа "Yandex Feed"
    15) Заполнение поля "Url" для "WB source"
    16) Нажатие кнопки "Save"
    17) Ожидание когда пропадет элемент "Feed config save"
    18) Выбор "WB feed"
    19) Нажатие кнопки "Load products"
    20) Ожидание когда пропадет эллемент "Feed product import started"
    21) Переход на "feed list" нажатием кнопки "<--"
    22) Ожидание статуса "Success" для добавленного фида
    23) Закрытие "Feed list"
    24) Открытие "Feed Products"
    25) Проверка значения "id" в таблице для тестового товара
    26) Получение значения "Sale" в таблице для тестового товара'
    27) Получение значения "Stock" в таблице для тестового товара'
    28) Сравнение измененных "price" и "stock", с значениями в таблице "Feed products"
    29) Запрос к API WB, получение "price" и "stock", сравнение со значениями в таблице "Feed products"
    """


    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)
    dict_xpath_product_feed = init_dict_xpath_product_feed(dict_init_data)
    dict_xpath_base = init_dict_xpath_base(dict_init_data)
    feed_data = parsing_data_feed()

    id_prod = 100591961  # "ID" тестового товара
    # Данные первого фида
    feed_change_1 = [100000, 0, "https://www.dropbox.com/s/pq7z3p963fn6na8/dop_feed_1_prod_stock_0.xml?dl=0"]
    # Данные второго фида
    feed_change_2 = [222222, 2, "https://www.dropbox.com/s/jpzcno80ui3ruyl/dop_feed_1_prod_stock_2.xml?dl=0"]
    # Ссылка для загрузки фида изменения цен и остатков
    change_feed_url = ''

    # 1) Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) Выбор пайплайна и МП
    choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed)

    # 3) общая страница -> Feed Products (клик)
    product_feed = wait_of_element_located('выбор кубика "Feed Products"',
                                           dict_xpath_product_feed['15'], driver)
    product_feed.click()

    # 4) Feed products -> "Search"
    search = wait_of_element_located('ввод "ID" продукта в поле "Search by name or ID"',
                                     dict_xpath_product_feed['17'], driver)
    search.send_keys(id_prod)
    search.send_keys(u'\ue007')

    # 5) Проверка значения "id" в таблице для тестового товара
    xpath_id = "//tbody[@class='ant-table-tbody']/tr[2]/td[2]"
    id_check = wait_of_element_located('ожидание эллемента "id" в таблице "Feed products" для тестового товара',
                                       xpath_id, driver)
    str_id_check = id_check.text[:id_check.text.find('\n')]
    assert str_id_check == str(id_prod), '"id" в таблице "Feed products" д.б. равен "id" для тестового товара'

    # 6) Получение значения "Sale" в таблице для тестового товара'
    xpath_sale = "//tbody[@class='ant-table-tbody']/tr[2]/td[4]"
    sale_check = wait_of_element_located(
        'ожидание эллемента "Sale" в таблице "Feed products" для тестового товара',
        xpath_sale, driver)
    str_sale_table = sale_check.text[:sale_check.text.find(' ')]

    # 7) Получение значения "Stock" в таблице для тестового товара'
    xpath_stock = "//tbody[@class='ant-table-tbody']/tr[2]/td[5]"
    stock_check = wait_of_element_located(
        'ожидание эллемента "Stock" в таблице "Feed products" для тестового товара',
        xpath_stock, driver)
    str_stock_table = stock_check.text

    print('=============================================')
    print('Значения из листинга "Product feed" ДО загрузки фида:')
    print('id - ' + str_id_check)
    print('stock - ' + str_stock_table)
    print('price - ' + str_sale_table)
    print('текущее время - ' + datetime.now().strftime("%d.%m.%Y %H:%M"))
    print('=============================================')

    print('Ответ WB API ДО загрузки фида:')
    # 8) Запрос к API WB, получение "price" и "stock", сравнение со значениями в таблице "Feed products"
    api_wb = get_WB_stock_price_discount(id_prod)
    # assert str(api_wb[0]) == str_sale_table, '"price" на МП WB д.б. равен "Sale" в таблице "Feed products"'
    # assert str(api_wb[1]) == str_stock_table, '"stock" на МП WB д.б. равен "stock" в таблице "Feed products"'

    print('текущее время - ' + datetime.now().strftime("%d.%m.%Y %H:%M"))
    print('=============================================')

    # 9) Исходя из текущего "price" и "stock" выбор "YML feed" для изменения цен и остатков
    if api_wb[0] == feed_change_1[0] and api_wb[1] == feed_change_1[1]:
        change_feed_url = feed_change_2[2]
        feed_price = feed_change_2[0]
        feed_stock = feed_change_2[1]
    elif api_wb[0] == feed_change_2[0] and api_wb[1] == feed_change_2[1]:
        change_feed_url = feed_change_1[2]
        feed_price = feed_change_1[0]
        feed_stock = feed_change_1[1]
    else:
        change_feed_url = feed_change_1[2]
        feed_price = feed_change_1[0]
        feed_stock = feed_change_1[1]
    change_feed_url = change_feed_url.replace(".xml?dl=0", ".xml?dl=1")

    print('url загружаемого фида - ' + change_feed_url)
    print('будущие значения stock - ' + str(feed_stock))
    print('будущие значения price - ' + str(feed_price))
    print('текущее время - ' + datetime.now().strftime("%d.%m.%Y %H:%M"))
    print('=============================================')


    # 10) Feed Products -> общая страница (клик)
    product_feed = wait_of_element_located('выход из "Feed Products" на общую страницу',
                                           dict_xpath_base['3'], driver)
    product_feed.click()

    # 11) общая страница -> Feeds list (клик)
    prod_feed = wait_of_element_located('выбор страницы "Feeds list"', dict_xpath_product_feed['1'], driver)
    prod_feed.click()

    # 12) Выбор "WB feed"
    wb_feed = wait_of_element_located('выбор страницы "WB feed"', dict_xpath_product_feed['18'], driver)
    wb_feed.click()

    # 13) Add feed config -> "File type" (клик)
    type_file = wait_of_element_located('выбор списка "File type"', dict_xpath_product_feed['7.0'], driver)
    type_file.click()

    # 14) Add feed config -> "File type" (Yandex Feed) (клик)
    type_file_yml = wait_of_element_located('выбор из списка "Yandex Feed"', dict_xpath_product_feed['7.2'], driver)
    type_file_yml.click()

    # 15) WB feed config -> "Url" (ввод)
    url_input = wait_of_element_located('ввод в поле "Url" для "Product source"', dict_xpath_product_feed['4.1'], driver)
    url_input.click()
    url_input.send_keys(Keys.CONTROL, 'a')
    url_input.send_keys(u'\ue017')
    url_input.send_keys(change_feed_url)

    # 16) WB feed config -> "Save" (клик)
    button_save_feed = wait_of_element_located('нажатие кнопки "Save"', dict_xpath_product_feed['8'], driver)
    button_save_feed.click()
    time.sleep(2)

    # 17) ожидание когда пропадет эллемент "Feed config save"
    wait_notice_save = wait_of_invisibility_of_element_located('ожидание "Feed config save"',
                                                               dict_xpath_product_feed['6'], driver)

    # 18) Выбор "WB feed"
    wb_feed = wait_of_element_located('выбор страницы "WB feed"', dict_xpath_product_feed['18'], driver)
    wb_feed.click()

    # 19) WB feed config -> "Load products"
    button_load = wait_of_element_located('нажатие кнопки "Load products"', dict_xpath_product_feed['5'], driver)
    button_load.click()
    time.sleep(2)

    # 20) ожидание когда пропадет эллемент "Feed product import started"
    wait_import_started = wait_of_invisibility_of_element_located('ожидание "Feed product import started"',
                                                                  dict_xpath_product_feed['16'], driver)

    # 21) feed config -> feed list
    back_feed_list = wait_of_element_located('нажатие кнопки "<--"', dict_xpath_product_feed['10'], driver)
    back_feed_list.click()

    # 22) Ожидание статуса "Success" для добавленного фида
    wait_success_feed = find_text_in_element('ожидание "Success" для фида',
                                             dict_xpath_product_feed[
                                                 '19'] + "/a[text()='" + "WildBerries" + "']" + "/parent::div/div",
                                             driver, "Success")

    # 23) Закрытие "Feed list"
    close_feed_list = wait_of_element_located('закрытие "Feed list"', dict_xpath_product_feed['14'], driver)
    close_feed_list.click()

    # 24) общая страница -> Feed Products (клик)
    product_feed = wait_of_element_located('выбор кубика "Feed Products"',
                                           dict_xpath_product_feed['15'], driver)
    product_feed.click()

    # 25) Проверка значения "id" в таблице для тестового товара
    xpath_id = "//tbody[@class='ant-table-tbody']/tr[2]/td[2]"
    id_check = wait_of_element_located('ожидание эллемента "id" в таблице "Feed products" для тестового товара',
                                       xpath_id, driver)
    str_id_check = id_check.text[:id_check.text.find('\n')]
    assert str_id_check == str(id_prod), '"id" в таблице "Feed products" д.б. равен "id" для тестового товара'

    # 26) Получение значения "Sale" в таблице для тестового товара'
    xpath_sale = "//tbody[@class='ant-table-tbody']/tr[2]/td[4]"
    sale_check = wait_of_element_located(
        'ожидание эллемента "Sale" в таблице "Feed products" для тестового товара',
        xpath_sale, driver)
    str_sale_table = sale_check.text[:sale_check.text.find(' ')]

    # 27) Получение значения "Stock" в таблице для тестового товара'
    xpath_stock = "//tbody[@class='ant-table-tbody']/tr[2]/td[5]"
    stock_check = wait_of_element_located(
        'ожидание эллемента "Stock" в таблице "Feed products" для тестового товара',
        xpath_stock, driver)
    str_stock_table = stock_check.text

    print('Значения из листинга "Product feed" ПОСЛЕ загрузки фида:')
    print('id - ' + str_id_check)
    print('stock - ' + str_stock_table)
    print('price - ' + str_sale_table)
    print('текущее время - ' + datetime.now().strftime("%d.%m.%Y %H:%M"))
    print('=============================================')

    # 28) Сравнение измененных "price" и "stock", с значениями в таблице "Feed products"
    assert str(feed_price) == str_sale_table, 'измененный "price" д.б. равен "Sale" в таблице "Feed products"'
    assert str(feed_stock) == str_stock_table, 'измененный "stock" д.б. равен "stock" в таблице "Feed products"'

    # задержка на случай если импорт прошел быстро и в WB не успели обновиться цены
    time.sleep(120)

    print('Ответ WB API ПОСЛЕ загрузки фида:')
    # 29) Запрос к API WB, получение "price" и "stock", сравнение со значениями в таблице "Feed products"
    api_wb = get_WB_stock_price_discount(id_prod)
    assert str(api_wb[0]) == str_sale_table, '"price" на МП WB д.б. равен "Sale" в таблице "Feed products"'
    assert str(api_wb[1]) == str_stock_table, '"stock" на МП WB д.б. равен "stock" в таблице "Feed products"'

    print('текущее время - ' + datetime.now().strftime("%d.%m.%Y %H:%M"))
    print('=============================================')

    time.sleep(5)

