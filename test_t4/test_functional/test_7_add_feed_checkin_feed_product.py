from Base.Base_functions import wait_of_element_located, get_app_version, login_T4, choice_pipeline_mp, \
    wait_of_invisibility_of_element_located, wait_of_elements_located, find_text_in_element
from Base.Dictionary_xpath import init_dict_xpath_login, init_dict_xpath_product_feed, init_dict_xpath_base
from Base.parse_yml_feed import parsing_data_feed
import allure
import time
from datetime import datetime

# Функция загрузки YML feed
@allure.feature('Тест стенд v.'+get_app_version())
@allure.story('Функциональное тестирование')
@allure.title('7) Импорт YML фида (без вариантов)')
@allure.severity('critical')
def test_add_feed_checkin_feed_product(get_driver, get_init_data):
    """
     1) Авторизация в системе T4MP.v2
     2) Выбор пайплайна и МП
     3) Открытие "Feeds list"
     4) Нажатие кнопки "Add feed"
     5) Открытие списка "File type"
     6) Выбор типа "Yandex Feed"
     7) Заполнение поля "Url" для "Product source"
     8) Нажатие кнопки "Save"
     9) Поиск добавленного фида в "Feeds list"
    10) Выбор добавленного фида
    11) Нажатие кнопки загрузки фида
    12) ожидание когда пропадет эллемент "Feed product import started"
    13) Переход на "feed list"
    14) Ожидание статуса "Success" для добавленного фида
    15) Закрытие "Feed list"
    16) Открытие "Product feed"
    17) Ввод в поле "Search" названия добавленного продукта
    18) Поиск в "Feed products" добавленного товара по дате добавления
    19) Проверка значения "id" в таблице и в YML feed
    20) Проверка значения "Product" в таблице и "name" в YML feed
    21) Проверка значения "Sale" в таблице и "price" в YML feed
    22) Проверка значения "Vendor" в таблице и в YML feed
    23) Проверка значения "Stock" в таблице и в YML feed
    24) Переход на общую страницу
    25) Переход на "feed list"
    26) Открытие добавленного фида
    27) Нажатие кнопки "Delete feed"
    28) Подверждение удаления фида
    """


    driver = get_driver
    dict_init_data = get_init_data
    dict_xpath_login = init_dict_xpath_login(dict_init_data)
    dict_xpath_product_feed = init_dict_xpath_product_feed(dict_init_data)
    dict_xpath_base = init_dict_xpath_base(dict_init_data)
    feed_data = parsing_data_feed()

    # 1) Авторизация
    login_T4(driver, dict_init_data, dict_xpath_login)

    # 2) Выбор пайплайна и МП
    choice_pipeline_mp(driver, dict_xpath_base, dict_xpath_product_feed, get_init_data)

    # 3) общая страница -> Feeds list (клик)
    prod_feed = wait_of_element_located('выбор страницы "Feeds list"', dict_xpath_product_feed['1'], driver)
    prod_feed.click()

    # 4) Feeds list -> "Add feed" (клик)
    add_feed = wait_of_element_located('нажатие кнопки "Add feed"', dict_xpath_product_feed['2'], driver)
    add_feed.click()

    # 5) Add feed config -> "File type" (клик)
    type_file = wait_of_element_located('выбор списка "File type"', dict_xpath_product_feed['7.0'], driver)
    type_file.click()

    # 6) Add feed config -> "File type" (Yandex Feed) (клик)
    type_file_yml = wait_of_element_located('выбор из списка "Yandex Feed"', dict_xpath_product_feed['7.2'], driver)
    type_file_yml.click()

    # 7) Add feed config -> "Url" (ввод)
    url_input = wait_of_element_located('ввод в поле "Url" для "Product source"', dict_xpath_product_feed['4'], driver)
    url_input.send_keys(dict_init_data["yml_url_location"])

    # 8) Add feed config -> "Save" (клик)
    button_save_feed = wait_of_element_located('нажатие кнопки "Save"', dict_xpath_product_feed['8'], driver)
    button_save_feed.click()
    time.sleep(2)

    # Время сохранения фида
    str_data_load = datetime.now().strftime("%d.%m.%Y %H:%M")
    data_load = datetime.strptime(str_data_load, "%d.%m.%Y %H:%M")

    # 9) Поиск добавленного фида в "Feeds list"
    row_feed = wait_of_elements_located('ожидание строк таблицы загруженных в DOM "Feeds list"',
                                        dict_xpath_product_feed['19'], driver)
    str_find_feed = ''
    for row in row_feed:
        str_data_feed = row.text
        str_data_feed = str_data_feed.replace('\n', ' ')
        if str_data_feed.find('Success') == -1 and str_data_feed.find('Error') == -1:
            str_find_feed = str_data_feed
    time.sleep(1)

    print(str_find_feed)

    # 10) "Feeds list" -> добавленный фид
    find_feed = wait_of_element_located('выбор добавленного фида',
                                        dict_xpath_product_feed['19'] + "/a[text()='" + str_find_feed + "']", driver)
    find_feed.click()

    # 11) Add feed config -> "Load products"
    button_load = wait_of_element_located('нажатие кнопки "Load products"', dict_xpath_product_feed['5'], driver)
    button_load.click()
    time.sleep(2)

    # 12) ожидание когда пропадет эллемент "Feed product import started"
    wait_import_started = wait_of_invisibility_of_element_located('ожидание "Feed product import started"',
                                                                  dict_xpath_product_feed['16'], driver)

    # 13) feed config -> feed list
    back_feed_list = wait_of_element_located('нажатие кнопки "<--"', dict_xpath_product_feed['10'], driver)
    back_feed_list.click()

    # 14) Ожидание статуса "Success" для добавленного фида
    wait_success_feed = find_text_in_element('ожидание "Success" для фида',
                                    dict_xpath_product_feed['19'] + "/a[text()='" + str_find_feed + "']" + "/parent::div/div",
                                             driver, "Success")

    # 15) Закрытие "Feed list"
    close_feed_list = wait_of_element_located('закрытие "Feed list"', dict_xpath_product_feed['14'], driver)
    close_feed_list.click()

    # 16) общая страница -> Feed Products (клик)
    product_feed = wait_of_element_located('выбор кубика "Feed Products"', dict_xpath_product_feed['15'], driver)
    product_feed.click()

    # 17) Feed products -> "Search"
    search = wait_of_element_located('ввод названия продукта в поле "Search by name or ID"',
                                     dict_xpath_product_feed['17'], driver)
    search.send_keys(feed_data[0][3])
    search.send_keys(u'\ue007')

    # 18) Поиск в Feed products добавленного товара по дате добавления
    str_data_end = ""
    t_delta = datetime.strptime("01.01.0001 01:01", "%d.%m.%Y %H:%M")
    find_data = datetime.strptime("01.01.0001 01:01", "%d.%m.%Y %H:%M")
    int_t_delta = 0
    str_data_row = wait_of_element_located('ожидание 1ой строка в таблице "Feed products"',
                                           "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div", driver).text

    while str_data_row != str_data_end:
        str_data_end = str_data_row
        row_products = wait_of_elements_located('ожидание строк таблицы загруженных в DOM "Feed products"',
                                                "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div", driver)
        for row in row_products:
            row.location_once_scrolled_into_view
            str_data_row = row.text
            data_row = datetime.strptime(str_data_row.replace('\n', ' '), "%d.%m.%Y %H:%M")
            t_delta = data_row - data_load
            int_t_delta = abs(t_delta.total_seconds())
            print(int_t_delta)
            print(data_row)
            print()
            if int_t_delta <= 120:
                find_data = data_row
                break
        if int_t_delta <= 120:
            break
        time.sleep(2)
    assert int_t_delta <= 120, 'проверка что добавленный товар найден в таблице "Feed products"'

    str_find_data = find_data.strftime("%d.%m.%Y %H:%M")
    str_only_data = str_only_time = str_find_data

    str_only_data = str_only_data[:10]
    str_only_time = str_only_time[11:]

    # 19) Проверка значения "id" в таблице и в YML feed
    xpath_id = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data + \
               "']/following-sibling::div/span[text()='" + str_only_time + "']/../../../../../td[2]"
    id_check = wait_of_element_located('ожидание эллемента "id" в таблице "Feed products" для импортированного товара',
                                       xpath_id, driver)
    str_id_check = id_check.text[:id_check.text.find('\n')]
    assert str_id_check == feed_data[0][0], '"id" в таблице "Feed products" д.б. равен "id" в YML feed'

    # 20) Проверка значения "Product" в таблице и "name" в YML feed
    xpath_name = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data +\
                 "']/following-sibling::div/span[text()='" + str_only_time + "']/../../../../../td[3]"
    name_check = wait_of_element_located('ожидание эллемента "Product" в таблице "Feed products" для импортированного товара',
                                         xpath_name, driver)
    assert name_check.text == feed_data[0][3], '"Product" в таблице "Feed products" д.б. равен "name" в YML feed'

    # 21) Проверка значения "Sale" в таблице и "price" в YML feed
    xpath_sale = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data +\
                 "']/following-sibling::div/span[text()='" + str_only_time + "']/../../../../../td[4]"
    sale_check = wait_of_element_located('ожидание эллемента "Sale" в таблице "Feed products" для импортированного товара',
                                         xpath_sale, driver)
    str_sale_check = sale_check.text[:sale_check.text.find(' ')]
    assert str_sale_check == feed_data[0][1], '"Sale" в таблице "Feed products" д.б. равен "price" в YML feed'

    # 22) Проверка значения "Vendor" в таблице и в YML feed
    xpath_vendor = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data +\
                   "']/following-sibling::div/span[text()='" + str_only_time + "']/../../../../../td[7]"
    vendor_check = wait_of_element_located('ожидание эллемента "Vendor" в таблице "Feed products" для импортированного товара',
                                           xpath_vendor, driver)
    assert vendor_check.text == feed_data[0][4], '"Vendor" в таблице "Feed products" д.б. равен "vendor" в YML feed'

    # 23) Проверка значения "Stock" в таблице и в YML feed
    xpath_stock = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data +\
                   "']/following-sibling::div/span[text()='" + str_only_time + "']/../../../../../td[5]"
    stock_check = wait_of_element_located('ожидание эллемента "Stock" в таблице "Feed products" для импортированного товара',
                                           xpath_stock, driver)
    assert stock_check.text == feed_data[0][5], '"Stock" в таблице "Feed products" д.б. равен "count" в YML feed'

    # 24) Feed Products -> общая страница
    arrow_left = wait_of_element_located('возвращение на общую страницу', dict_xpath_product_feed['10'], driver)
    arrow_left.click()

    # 25) общая страница -> Feeds list (клик)
    prod_feed = wait_of_element_located('выбор страницы "Feeds list"', dict_xpath_product_feed['1'], driver)
    prod_feed.click()

    # 26) "Feeds list" -> добавленный фид
    find_feed = wait_of_element_located('выбор добавленного фида',
                                        dict_xpath_product_feed['19'] + "/a[text()='" + str_find_feed + "']", driver)
    find_feed.click()

    # 27) feed config -> "Delete feed"
    delete_feed = wait_of_element_located('удаление фида',
                                        dict_xpath_product_feed['13'], driver)
    delete_feed.click()
    time.sleep(2)

    # 28) delete feed -> "YES
    yes_feed = wait_of_element_located('удаление фида - "YES"',
                                        dict_xpath_product_feed['20'], driver)
    yes_feed.click()

    # # 18) Открытие карточки импортированного товара
    # xpath_name = "//tbody[@class='ant-table-tbody']/tr/td[8]/div/div/div[text()='" + str_only_data + \
    #              "']/following-sibling::div/span[text()='" + str_only_time + \
    #              "']/../../../../../td[3]/div/div/div[2]/div/div/a"
    # name_check = wait_of_element_located(
    #     'открытие карточки импортированного товара',
    #     xpath_name, driver)
    # name_check.click()

    time.sleep(2)
