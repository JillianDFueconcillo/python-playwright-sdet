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


CATALOG_NAMES = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]
CATALOG_PRICES_AZ = [29.99, 9.99, 15.99, 49.99, 7.99, 15.99]


def test_inventory_shows_six_products(inventory_page: InventoryPage):
    assert inventory_page.get_title().text_content() == "Products"
    assert inventory_page.get_product_count() == 6
    assert inventory_page.get_item_names() == CATALOG_NAMES
    assert inventory_page.get_item_prices() == CATALOG_PRICES_AZ
    assert all(description for description in inventory_page.get_item_descriptions())


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


def test_default_sort_is_name_a_to_z(inventory_page: InventoryPage):
    assert inventory_page.get_selected_sort() == "az"
    assert inventory_page.get_item_names() == CATALOG_NAMES


def test_sort_name_z_to_a(inventory_page: InventoryPage):
    inventory_page.sort_products_by("za")

    assert inventory_page.get_item_names() == list(reversed(CATALOG_NAMES))


def test_sort_price_low_to_high(inventory_page: InventoryPage):
    inventory_page.sort_products_by("lohi")

    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices)
    assert prices[0] == 7.99
    assert prices[-1] == 49.99


def test_sort_price_high_to_low(inventory_page: InventoryPage):
    inventory_page.sort_products_by("hilo")

    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices, reverse=True)
    assert prices[0] == 49.99
    assert prices[-1] == 7.99


def test_add_and_remove_from_inventory_updates_badge(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart("sauce-labs-backpack")

    assert inventory_page.get_remove_button("sauce-labs-backpack").is_visible()
    assert not inventory_page.get_add_to_cart_button("sauce-labs-backpack").is_visible()
    assert inventory_page.get_cart_badge_count() == 1

    inventory_page.remove_item_from_cart("sauce-labs-backpack")

    assert inventory_page.get_add_to_cart_button("sauce-labs-backpack").is_visible()
    assert inventory_page.get_cart_badge_count() == 0


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