from urllib.parse import urlparse

import pytest

from pages.InventoryPage import InventoryPage
from pages.LoginPage import LoginPage

INVENTORY_REQUIRES_LOGIN = (
    "Epic sadface: You can only access '/inventory.html' when you are logged in."
)
BAD_CREDENTIALS = (
    "Epic sadface: Username and password do not match any user in this service"
)


def _assert_inventory_not_visible(inventory_page: InventoryPage, login_page: LoginPage):
    assert not inventory_page.get_title().is_visible()
    assert not inventory_page.get_sort_dropdown().is_visible()
    assert inventory_page.get_product_count() == 0
    assert login_page.get_login_button().is_visible()


# Level 1 check element exit, or are visible and work
def test_sort_dropdown_visible(inventory_page: InventoryPage):
    assert inventory_page.get_sort_dropdown().is_visible()


# Test actual functionality
@pytest.mark.parametrize(
    "options",
    [
        ("az"),
        ("za"),
        ("lohi"),
        ("hilo"),
    ],
)
def test_sort_options(inventory_page: InventoryPage, options):
    inventory_page.sort_products_by(options)

    assert inventory_page.get_selected_sort() == options


def test_sort_dropdown_count(inventory_page: InventoryPage):
    assert inventory_page.get_sort_option_count() == 4


def test_inventory_blocked_without_login_direct_url(
    login_page: LoginPage, logged_out_inventory_page: InventoryPage
):
    logged_out_inventory_page.open()

    _assert_inventory_not_visible(logged_out_inventory_page, login_page)
    assert (
        login_page.get_error_message().inner_text().strip() == INVENTORY_REQUIRES_LOGIN
    )


def test_inventory_blocked_without_login_redirect(
    login_page: LoginPage, logged_out_inventory_page: InventoryPage
):
    login_page.login_user("", "")

    _assert_inventory_not_visible(logged_out_inventory_page, login_page)
    assert urlparse(login_page.page.url).path in ("/", "")


def test_inventory_blocked_after_wrong_login_direct_url(
    login_page: LoginPage, logged_out_inventory_page: InventoryPage
):
    login_page.login_user("standard_user", "wrong_password")
    logged_out_inventory_page.open()

    _assert_inventory_not_visible(logged_out_inventory_page, login_page)
    assert (
        login_page.get_error_message().inner_text().strip() == INVENTORY_REQUIRES_LOGIN
    )


def test_inventory_blocked_after_wrong_login_redirect(
    login_page: LoginPage, logged_out_inventory_page: InventoryPage
):
    inventory_page = login_page.login_user("standard_user", "wrong_password")

    _assert_inventory_not_visible(inventory_page, login_page)
    assert urlparse(login_page.page.url).path in ("/", "")
    assert login_page.get_error_message().inner_text().strip() == BAD_CREDENTIALS