def test_admin_login_success(login_page, registered_user):
    # Если registered_user вернулся как словарь,
    # берем логин и пароль по ключам.
    if isinstance(registered_user, dict):
        login = registered_user["login"]
        password = registered_user["password"]
    else:
        # Если registered_user вернулся как объект модели,
        # берем логин и пароль как атрибуты.
        login = registered_user.login
        password = registered_user.password

    # Выполняем позитивный сценарий логина.
    login_page.login(login, password)

    # Проверяем, что после входа появилось сообщение об успехе.
    assert login_page.check_success_message("Успешно! Вход выполнен.")