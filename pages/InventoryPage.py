from playwright.sync_api import Page

from pages.CartPage import CartPage
from pages.ProductPage import ProductPage


class InventoryPage:
    def __init__(self, page: Page) -> None:
        # Locators
        self.page = page
        self.title = page.locator("[data-test=\"title\"]")

        self.inventory_items = page.locator("[data-test=\"inventory-item\"]")
        self.item_names = page.locator("[data-test=\"inventory-item-name\"]")
        self.item_descriptions = page.locator("[data-test=\"inventory-item-desc\"]")
        self.item_prices = page.locator("[data-test=\"inventory-item-price\"]")

        self.sort_dropdown = page.locator("[data-test=\"product-sort-container\"]")
        self.sort_options = self.sort_dropdown.locator("option")

        self.cart_link = page.locator("[data-test=\"shopping-cart-link\"]")
        self.cart_badge = page.locator("[data-test=\"shopping-cart-badge\"]")
        self.inventory_container = page.locator("[data-test=\"inventory-container\"]")

        self.menu_button = page.locator("#react-burger-menu-btn")
        self.close_menu_button = page.locator("#react-burger-cross-btn")
        self.all_items_link = page.locator("[data-test=\"inventory-sidebar-link\"]")
        self.about_link = page.locator("[data-test=\"about-sidebar-link\"]")
        self.logout_link = page.locator("[data-test=\"logout-sidebar-link\"]")
        self.reset_link = page.locator("[data-test=\"reset-sidebar-link\"]")

    # Methods (Wrapper)
    def open(self):
        self.page.goto("/inventory.html")
        return self

    def add_item_to_cart(self, item_id: str):
        self.get_add_to_cart_button(item_id).click()
        return self

    def remove_item_from_cart(self, item_id: str):
        self.get_remove_button(item_id).click()
        return self

    def sort_products_by(self, option: str):
        self.sort_dropdown.select_option(option)
        return self

    def open_menu(self):
        self.menu_button.click()
        self.logout_link.wait_for()
        return self

    def close_menu(self):
        self.close_menu_button.click()
        self.logout_link.wait_for(state="hidden")
        return self

    def reset_app_state(self):
        self.open_menu()
        self.reset_link.click()
        self.cart_badge.wait_for(state="hidden")
        self.close_menu()
        return self

    def logout(self):
        from pages.LoginPage import LoginPage

        self.open_menu()
        self.logout_link.click()
        login_page = LoginPage(self.page)
        login_page.get_login_button().wait_for()
        return login_page

    def open_cart(self) -> CartPage:
        self.cart_link.click()
        cart_page = CartPage(self.page)
        cart_page.get_checkout_button().wait_for()
        return cart_page

    def open_first_product(self) -> ProductPage:
        self.item_names.first.click()
        product_page = ProductPage(self.page)
        product_page.get_back_to_products_button().wait_for()
        return product_page

    def open_product(self, item_name: str) -> ProductPage:
        self.item_names.filter(has_text=item_name).click()
        product_page = ProductPage(self.page)
        product_page.get_back_to_products_button().wait_for()
        return product_page

    # Getters (are used for assertions later.)
    def get_title(self):
        return self.title

    def get_inventory_container(self):
        return self.inventory_container

    def get_sort_dropdown(self):
        return self.sort_dropdown

    def get_product_count(self):
        return self.inventory_items.count()

    def get_sort_option_count(self):
        return self.sort_options.count()

    def get_selected_sort(self):
        # Returns the value of the selected option, for example "az"
        return self.sort_dropdown.input_value()

    def get_item_names(self):
        return self.item_names.all_text_contents()

    def get_item_descriptions(self):
        return self.item_descriptions.all_text_contents()

    def get_item_prices(self):
        # Turn "$29.99" into 29.99 so we can compare numbers
        prices = []
        for price_text in self.item_prices.all_text_contents():
            prices.append(float(price_text.replace("$", "")))
        return prices

    def get_add_to_cart_button(self, item_id: str):
        return self.page.locator(f"[data-test=\"add-to-cart-{item_id}\"]")

    def get_remove_button(self, item_id: str):
        return self.page.locator(f"[data-test=\"remove-{item_id}\"]")

    def get_cart_badge(self):
        return self.cart_badge

    def get_cart_badge_count(self):
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())

    def get_about_link(self):
        return self.about_link

    # CLASSES SHOULD NOT HAVE ANY ASSERTS(or Expects)