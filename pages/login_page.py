from locators.user_form_locators import AdminLoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object страницы логина.
    """

    def __init__(self, driver, wait):
        """
        Передаем driver и wait в базовый класс.
        """
        super().__init__(driver, wait)

    def open_login_page(self):
        """
        С главной страницы переходим на страницу логина
        через пункт меню "Вход".
        """
        self.click(locator=AdminLoginLocators.LOGIN_NAV_BUTTON)
        return self

    def is_login_page_opened(self):
        """
        Проверяем, что страница логина открыта.
        """
        return self.is_visible(AdminLoginLocators.LOGIN)

    def enter_login(self, login):
        """
        Вводим логин в поле логина.
        """
        self.fill(locator=AdminLoginLocators.LOGIN, value=login)

    def enter_password(self, password):
        """
        Вводим пароль в поле пароля.
        """
        self.fill(locator=AdminLoginLocators.PASSWORD, value=password)

    def click_login_button(self):
        """
        Нажимаем кнопку входа.
        """
        self.click(locator=AdminLoginLocators.LOGIN_BUTTON)

    def login(self, login, password):
        """
        Полный сценарий авторизации.
        """
        self.open_login_page()
        self.enter_login(login)
        self.enter_password(password)
        self.click_login_button()
        return self

    def get_success_message(self):
        """
        Получаем текст успешного сообщения.
        """
        return self.text(locator=AdminLoginLocators.RESULT_MESSAGE)

    def get_error_message(self):
        """
        Получаем текст сообщения об ошибке.
        """
        return self.text(locator=AdminLoginLocators.RESULT_MESSAGE_ERR)

    def check_success_message(self, expected_text):
        """
        Сравниваем фактический успешный текст с ожидаемым.
        """
        return self.get_success_message() == expected_text

    def check_error_message(self, expected_text):
        """
        Сравниваем фактический текст ошибки с ожидаемым.
        """
        return self.get_error_message() == expected_text