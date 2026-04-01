# Импортируем expected_conditions.
# Это набор готовых ожиданий Selenium:
# видимость элемента, кликабельность, наличие текста и т.д.
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Базовый класс для всех page object в проекте.

    Здесь будут лежать только общие действия:
    - открыть страницу
    - найти элемент
    - кликнуть
    - заполнить поле
    - получить текст
    - проверить видимость элемента

    Почему так:
    если одни и те же действия копировать в каждую страницу,
    код быстро начнет дублироваться.
    """

    def __init__(self, driver, wait):
        """
        Конструктор базовой страницы.

        :param driver: экземпляр Selenium WebDriver
        :param wait: экземпляр WebDriverWait, который приходит из фикстуры

        Мы сохраняем driver и wait в объекте,
        чтобы потом использовать их во всех методах страницы.
        """
        self.driver = driver
        self.wait = wait

    def open(self, url):
        """
        Открывает нужный URL в браузере.

        Этот метод общий, потому что любая страница
        может потребовать открыть себя по адресу.
        """
        self.driver.get(url)

    def find_element(self, locator):
        """
        Ищет элемент и ждет, пока он станет видимым.

        Почему не просто driver.find_element():
        потому что UI может отрисоваться не мгновенно,
        и без ожиданий тесты будут нестабильными.

        visibility_of_element_located означает:
        - элемент есть в DOM
        - элемент видим пользователю
        - у него есть размер, то есть с ним можно работать
        """
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element is not visible by locator: {locator}"
        )

    def click(self, locator):
        """
        Кликает по элементу.

        Здесь мы ждем не просто видимость,
        а именно кликабельность элемента.
        Это надежнее для кнопок, ссылок и интерактивных элементов.
        """
        element = self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element is not clickable: {locator}"
        )
        element.click()

    def fill(self, locator, value: str, clear=True):
        """
        Заполняет поле текстом.

        :param locator: локатор элемента
        :param value: текст, который вводим
        :param clear: очищать ли поле перед вводом

        Логика такая:
        1. Находим поле.
        2. При необходимости очищаем его.
        3. Если value не пустое, отправляем текст в поле.
        """
        element = self.find_element(locator)

        if clear:
            element.clear()

        if value:
            element.send_keys(value)

    def text(self, locator) -> str:
        """
        Возвращает текст элемента.

        Используется, например, для:
        - ошибок авторизации
        - заголовков страниц
        - сообщений об успехе
        """
        return self.find_element(locator).text

    def is_visible(self, locator) -> bool:
        """
        Проверяет, что элемент видим.

        Если wait не упал по таймауту,
        значит элемент найден и видим.
        Возвращаем True.
        """
        self.find_element(locator)
        return True