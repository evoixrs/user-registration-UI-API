def test_admin_login_success(login_page, registered_user):
    """
    Проверяем, что зарегистрированный пользователь
    может успешно войти в систему.
    """

    # Подготавливаем тестовые данные для логина.
    # Здесь получаем валидные логин и пароль
    # из фикстуры registered_user.
    if isinstance(registered_user, dict):
        login = registered_user["login"]
        password = registered_user["password"]
    else:
        login = registered_user.login
        password = registered_user.password

    # Проверяем, что можем открыть страницу логина
    # через пункт меню "Вход".
    login_page.open_login_page()

    # Дополнительно убеждаемся,
    # что форма логина действительно открылась.
    assert login_page.is_login_page_opened()

    # Вводим логин зарегистрированного пользователя.
    login_page.enter_login(login)

    # Вводим пароль зарегистрированного пользователя.
    login_page.enter_password(password)

    # Нажимаем кнопку входа.
    login_page.click_login_button()

    # Проверяем, что после успешного входа
    # открылась страница списка пользователей.
    assert login_page.is_users_page_opened()