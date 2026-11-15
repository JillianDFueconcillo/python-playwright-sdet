from pages.InventoryPage import InventoryPage


def test_about_link_points_to_sauce_labs(inventory_page: InventoryPage):
    inventory_page.open_menu()

    assert inventory_page.get_about_link().get_attribute("href") == "https://saucelabs.com/"


def test_reset_app_state_clears_cart(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    assert inventory_page.get_cart_badge_count() == 1

    inventory_page.reset_app_state()

    assert inventory_page.get_cart_badge_count() == 0
    assert inventory_page.open_cart().get_item_count() == 0


def test_logout_from_inventory(inventory_page: InventoryPage):
    login_page = inventory_page.logout()

    assert login_page.get_login_button().is_visible()
    assert login_page.page.url.rstrip("/") == "https://www.saucedemo.com"


def test_all_items_from_cart_returns_to_products(cart_with):
    inventory_page = cart_with("sauce-labs-backpack").open_all_items()

    assert inventory_page.get_title().text_content() == "Products"
    assert inventory_page.get_remove_button("sauce-labs-backpack").is_visible()
