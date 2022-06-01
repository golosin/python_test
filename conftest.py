import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from Base.Init_Test_Data import init_data


@pytest.fixture
def get_chrome_options():
    options = chrome_options()
    options.add_argument('headless')  # если не нужен UI браузер использовать headless
    # options.add_argument('--start-maximized')
    return options


@pytest.fixture
def get_webdriver(get_chrome_options):
    options = get_chrome_options
    driver = webdriver.Remote(
        command_executor=f"http://selenium__standalone-chrome:4444/wd/hub",
        options=options
    )
    # driver = webdriver.Chrome(options=options)
    return driver


@pytest.fixture
def get_init_data():
    dict_init_data = init_data()
    return dict_init_data


@pytest.fixture(scope='function')
def get_driver(get_webdriver, get_init_data):
    driver = get_webdriver
    dict_init_data = get_init_data
    url = dict_init_data["environment"]
    driver.get(url)
    yield driver
    driver.close()
