from playwright.sync_api import Page

import pytest

from pages.InventoryPage import InventoryPage

from pages.LoginPage import LoginPage


def test_login_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    # assert (login_page.get_login_credentials.all_text_contents()).to_contain_text("standard_user")
    assert "standard_user" in login_page.get_login_credentials().inner_html()
    assert "secret_sauce" in login_page.get_login_password().inner_html()



def test_login_success(page: Page):
    # Login Object only has Logging Locators and Methods
    login_page = LoginPage(page)
    login_page.open()
    # Calling the login_standard_user also passes on the next PO
    inventory_page = login_page.login_standard_user()
    # Only has access to Inventory stuff
    inventory_page = InventoryPage(page)
    assert inventory_page.get_title().text_content() == "Products"




@pytest.mark.parametrize(
    "username",
    [
        ("standard_user"),
        ("problem_user"),
        ("performance_glitch_user"),
        ("visual_user"),
    ],
)



def test_login_success2(page: Page, username):
    # Login Object only has Logging Locators and Methods
    login_page = LoginPage(page)
    login_page.open()
    # Calling the login_standard_user also passes on the next PO
    inventory_page = login_page.login_user(username, "secret_sauce")
    # Only has access to Inventory stuff
    inventory_page = InventoryPage(page)
    assert inventory_page.get_title().text_content() == "Products"


#negative as well
@pytest.mark.parametrize(
    "username, error",
    [
        ("locked_out_user", "Epic sadface: Sorry, this user has been locked out."),
        ("not_a_user", "Epic sadface: Username and password do not match any user in this service"), 
    ],
)
def test_login_fails(page: Page, username, error):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_user(username, "secret_sauce")

    actual_error = login_page.get_error_message().text_content()
    # expected   vs.       actual
    assert error in actual_error