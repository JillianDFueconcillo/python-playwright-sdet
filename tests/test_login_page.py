import pytest

from pages.LoginPage import LoginPage


def test_login_credentials(login_page: LoginPage):
    assert "standard_user" in login_page.get_login_credentials().inner_html()
    assert "secret_sauce" in login_page.get_login_password().inner_html()


def test_login_success(login_page: LoginPage):
    inventory_page = login_page.login_standard_user()
    assert inventory_page.get_title().text_content() == "Products"


@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "visual_user",
    ],
)
def test_login_success2(login_page: LoginPage, username: str):
    inventory_page = login_page.login_user(username, "secret_sauce")
    assert inventory_page.get_title().text_content() == "Products"


@pytest.mark.parametrize(
    "username, error",
    [
        ("locked_out_user", "Epic sadface: Sorry, this user has been locked out."),
        ("not_a_user", "Epic sadface: Username and password do not match any user in this service"),
    ],
)
def test_login_fails(login_page: LoginPage, username: str, error: str):
    login_page.login_user(username, "secret_sauce")

    actual_error = login_page.get_error_message().text_content()
    assert error in actual_error
