def init_dict_xpath_login(dict_init_data):

    dict_xpath_login = {
        # T4MP -> "Email"
        '0': "//input[@id='email']",
        # T4MP -> "Password"
        '1': "//input[@id='password']",
        # T4MP -> "Sing in"
        '2': "//button[@data-test-id='login']",
        # T4MP -> Pipelines
        '3': "//strong"
    }
    return dict_xpath_login

def init_dict_xpath_product_feed(dict_init_data):

    dict_xpath_feed_products = {
        # Pipelines -> выбор пайплайна
        '0': "//div[text()='" + dict_init_data["pipeline"] + "']",
        # выбранный пайплайн -> Feeds list
        '1': "//span[@aria-label='setting']",
        # Feeds list -> "Add feed"
        '2': "//button[@data-test-id='add-feed']",
        # Add feed config -> "Name"
        '3': "//input[@id='name']",
        # Add feed config -> "Url products"
        '4': "//input[@id='urlProducts']",
        # Add feed config -> "Url prices"
        '5': "//input[@id='urlPrices']",
        # Add feed config -> "Url stocks"
        '6': "//input[@id='urlStocks']",
        # Add feed config -> "File type"
        '7.0': "//div[@class='ant-select-selector']",
        # Add feed config -> "File type" (CSV)
        '7.1': "//div[@title='Csv']",
        # Add feed config -> "File type" (Yandex Feed)
        '7.2': "//div[@title='Yandex Feed']",
        # Add feed config -> "File type" (Google Feed)
        '7.3': "//div[@title='Google Feed']",
        # Add feed config -> "File type" (Custom)
        '7.4': "//div[@title='Custom']",
        # Add feed config -> "Save"
        '8': "//button[@data-test-id='save-feed']",
        # Add feed config -> "Load products"
        '9': "//button[@data-test-id='load-products']",
        # Add feed config -> Feeds list
        '10': "//span[@aria-label='arrow-left']",
        # Ожидание статуса загрузки "success"
        '11': "//div[text()='" + dict_init_data["yml_name_feed"] + "']/parent::div/parent::div/parent::div/parent::td/following-sibling::td[2]/div/div/div/span",
        # Feeds list -> Edit feed config
        '12': "//div[text()='" + dict_init_data["yml_name_feed"] + "']/parent::div/parent::div/parent::div/parent::td/following-sibling::td[5]/div/div/div/span",
        # Edit feed config -> "Delete feed"
        '13': "//button[@data-test-id='delete-feed']",
        #  Feeds list -> X (выход) (клик)
        '14': "//span[@aria-label='close']",
        # общая страница -> Feed Products
        '15': "//span[@aria-label='file-add']",

        '16': "//tr[@data-row-key='110']"
    }
    return dict_xpath_feed_products


def init_dict_xpath_base(dict_init_data):

    dict_xpath_base = {
        # листинг пайплайнов -> 1й пайплайн
        '0': "//div[@data-test-id='id-1']",
        # общая стр пайплайна -> Wildberries
        '1': "//div[text()='Wildberries']",
        # Feed Products -> 1й товар карточка
        '2': "//tbody[@class='ant-table-tbody']//tr[2]//td[3]/div/div/div[2]/div/div/a",
        # 1й товар карточка -> Feed Products
        '3': "//span[@aria-label='arrow-left']",
        # общая страница -> Edit Products
        '4': "//span[@aria-label='edit']",
        # Edit Products -> 1й товар карточка
        '5': "//tbody[@class='ant-table-tbody']//tr[2]//td[2]/div/div/div[2]/div/div/a",
        # общая страница -> Published on marketplace
        '6': "//div[@data-test-id='marketplaceProducts']"
    }
    return dict_xpath_base




