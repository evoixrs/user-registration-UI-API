import logging

import pytest
from api_client.client import StoreClient
from api_client.models.register import RegisterModel

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage

logger = logging.getLogger("api_tests")

def pytest_addoption(parser):
     parser.addoption("--api-url", action="store", default="http://127.0.0.1:5000/",
                      help="Base API URL for tested service")
     parser.addoption("--headless", action="store_true",
                      help="Run browser in headless mode")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--api-url")
    """Получаем адрес стенда из параметра запуска pytest"""

@pytest.fixture(scope="session")
def api_client(request):
    url = request.config.getoption("--api-url")
    logger.info(f"Start app on address {url}")
    """Логи, на какой адрес будет отправляться запрос"""

    client = StoreClient(url=url)
    """Экземпляр StoreClient с этим url для общения с API"""

    return client
    """Возвращаем экземпляр, чтобы использовать его в тестах"""


@pytest.fixture
def registered_user(api_client):
    body = RegisterModel().random()
    """Генерация случайного логина и пароля для нового пользователя"""

    reg_response = api_client.register(body=body)
    """Регистрируем пользователя через API с помощью клиента"""

    assert reg_response.status_code == 200
    """Проверка на успешную регистрацию"""

    return body
    """Возвращает логин и пароль"""


@pytest.fixture
def driver(request, base_url):
    is_headless = request.config.getoption("--headless")
    """Получаем headless из параметров запуска pytest"""

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    """Настраиваем параметры запуска Chrome"""

    if is_headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    """Если передан флаг --headless, запускаем браузер без UI"""

    logger.info("Start app on url %s, headless is %s", base_url, is_headless)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)
    """Открываем стартовую страницу"""

@pytest.fixture
def driver(request, base_url):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(base_url)
    yield driver

    logger.info("Stop browser")
    driver.quit()
    """Закрыть браузер после завершения теста"""

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)
    """Возвращаем объект для явных ожиданий элементов и состояний страницы"""

@pytest.fixture
def login_page(driver, wait):
    return LoginPage(driver, wait)
    """Создаем page object страницы логина поверх уже готового driver"""
