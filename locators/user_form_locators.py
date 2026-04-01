from selenium.webdriver.common.by import By


class AdminLoginLocators:

    """Локаторы формы входа"""
    LOGIN_NAV_BUTTON = (By.CSS_SELECTOR, 'a[href="/login"]')
    LOGIN = (By.ID, 'loginField')
    PASSWORD = (By.ID, 'passwordField')
    LOGIN_BUTTON = (By.ID, 'add-btn')

    #RESULT_MESSAGE = (By.CLASS_NAME, "alert-info")
    """Локатор успешного сообщения пока не используем,
    потому что после успешного входа сайт делает редирект
    на страницу списка пользователей."""

    RESULT_MESSAGE_ERR = (By.CLASS_NAME, "alert-danger")


class AddUserFormLocators:
    """Локаторы добавления пользователей"""
    ADD_USER_NAV_BUTTON = (By.CSS_SELECTOR, 'a[href="/add-user"]')
    NAME = (By.ID, 'name')
    AGE = (By.ID, 'age')
    GENDER = (By.ID, 'gender')
    DATE = (By.ID, 'date_birthday')
    STATUS_ACTIVE = (By.ID, 'isActive')
    SAVE_TABLE = (By.ID, 'add-btn')
    GO_TABLE = (By.LINK_TEXT, "Перейти к таблице пользователей")






