from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from locators.user_form_locators import AddUserFormLocators
from pages.base_page import BasePage


class AddUserPage(BasePage):
    """
    Page object страницы добавления пользователя.
    """

    def __init__(self, driver, wait):
        """
        Передаем driver и wait в базовый класс.
        """
        super().__init__(driver, wait)

    def open_add_user_page(self):
        """
        Со страницы списка пользователей переходим
        на страницу добавления пользователя
        через пункт меню "Добавить пользователя".
        """
        self.click(locator=AddUserFormLocators.ADD_USER_NAV_BUTTON)
        return self

    def is_add_user_page_opened(self):
        """
        Проверяем, что страница добавления пользователя открыта.

        В качестве признака открытия страницы
        используем видимость поля имени.
        """
        return self.is_visible(AddUserFormLocators.NAME)

    def enter_name(self, name):
        """
        Вводим имя нового пользователя в поле имени.
        """
        self.fill(locator=AddUserFormLocators.NAME, value=name)

    def enter_age(self, age):
        """
        Вводим возраст нового пользователя в поле возраста.
        """
        self.fill(locator=AddUserFormLocators.AGE, value=age)

    def enter_gender(self, gender):
        """
        Вводим пол нового пользователя в поле пола.
        """
        self.fill(locator=AddUserFormLocators.GENDER, value=gender)

    def enter_birthday(self, birthday):
        """
        Вводим дату рождения нового пользователя.

        Для этого поля используем JavaScript,
        потому что обычный send_keys может заполнять дату некорректно.
        После установки значения дополнительно вызываем события,
        чтобы страница обработала изменение так же,
        как при ручном вводе пользователем.
        """
        element = self.find_element(AddUserFormLocators.DATE)

        self.driver.execute_script(
            """
            arguments[0].value = '';
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            birthday
        )

    def set_active_status(self):
        """
        Устанавливаем чекбокс "Активен",
        если он еще не выбран.
        """
        checkbox = self.find_element(AddUserFormLocators.STATUS_ACTIVE)

        # Если чекбокс еще не установлен,
        # нажимаем на него один раз.
        if not checkbox.is_selected():
            checkbox.click()

    def click_save_button(self):
        """
        Нажимаем кнопку сохранения пользователя.
        """
        self.click(locator=AddUserFormLocators.SAVE_TABLE)

    def go_to_users_table(self):
        """
        После сохранения пользователя переходим
        к таблице пользователей.
        """
        self.click(locator=AddUserFormLocators.GO_TABLE)
        return self

    def is_users_page_opened(self):
        """
        Проверяем, что открылась страница списка пользователей.

        Ожидаем, что URL будет содержать '/users'.
        """
        try:
            self.wait.until(EC.url_contains("/users"))
            return True
        except TimeoutException:
            return False

    def is_user_present_in_table(self, user_name):
        """
        Проверяем, что пользователь с нужным именем
        отображается в таблице пользователей.
        """
        # Формируем динамический локатор для поиска строки таблицы,
        # в которой есть ячейка с точным текстом имени пользователя.
        user_row_locator = (
            By.XPATH,
            f"//table//tr[td[normalize-space()='{user_name}']]"
        )

        try:
            self.wait.until(
                EC.visibility_of_element_located(user_row_locator)
            )
            return True
        except TimeoutException:
            return False

    def add_user(self, name, age, gender, birthday, is_active=True):
        """
        Выполняем полный сценарий добавления пользователя:
        заполняем форму и сохраняем нового пользователя.
        """
        # Заполняем имя пользователя.
        self.enter_name(name)

        # Заполняем возраст пользователя.
        self.enter_age(age)

        # Заполняем пол пользователя.
        self.enter_gender(gender)

        # Заполняем дату рождения пользователя.
        self.enter_birthday(birthday)

        # Если по тестовым данным пользователь должен быть активным,
        # устанавливаем чекбокс "Активен".
        if is_active:
            self.set_active_status()

        # Сохраняем нового пользователя.
        self.click_save_button()
        return self