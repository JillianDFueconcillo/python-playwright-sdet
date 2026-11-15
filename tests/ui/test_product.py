import pytest

from pages.InventoryPage import InventoryPage
from pages.ProductPage import ProductPage


def test_first_product_details_load(product_page: ProductPage):
    assert product_page.get_name().text_content() == "Sauce Labs Backpack"
    assert product_page.get_price() == 29.99
    assert product_page.get_image().is_visible()
    assert product_page.get_add_to_cart_button().is_visible()


def test_add_first_product_to_cart_from_details(product_page: ProductPage):
    product_page.add_to_cart()

    assert product_page.get_remove_button().is_visible()
    assert not product_page.get_add_to_cart_button().is_visible()
    assert product_page.get_cart_badge().text_content() == "1"

    cart_page = product_page.open_cart()

    assert cart_page.get_title().text_content() == "Your Cart"
    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Backpack"]
    assert cart_page.get_item_prices() == [29.99]
    assert cart_page.get_cart_badge_count() == 1


def test_back_to_products_from_details(product_page: ProductPage):
    inventory_page = product_page.back_to_products()

    assert inventory_page.get_title().text_content() == "Products"
    assert inventory_page.get_product_count() == 6


def test_remove_from_product_details(product_page: ProductPage):
    product_page.add_to_cart().remove_from_cart()

    assert product_page.get_add_to_cart_button().is_visible()
    assert not product_page.get_remove_button().is_visible()
    assert product_page.get_cart_badge().count() == 0


@pytest.mark.parametrize(
    "name, price",
    [
        ("Sauce Labs Backpack", 29.99),
        ("Sauce Labs Bike Light", 9.99),
        ("Sauce Labs Bolt T-Shirt", 15.99),
        ("Sauce Labs Fleece Jacket", 49.99),
        ("Sauce Labs Onesie", 7.99),
        ("Test.allTheThings() T-Shirt (Red)", 15.99),
    ],
)
def test_each_product_details_page(inventory_page: InventoryPage, name, price):
    product_page = inventory_page.open_product(name)

    assert product_page.get_name().text_content() == name
    assert product_page.get_price() == price
    assert product_page.get_description().is_visible()
    assert product_page.get_image().is_visible()
    assert product_page.get_add_to_cart_button().is_visible()
