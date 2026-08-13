from playwright.sync_api import Page
from pages.CartPage import CartPage

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

        self.cart_icon = page.locator("[data-test=\"shopping-cart-link\"]")
        self.add_to_cart_backpack = page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]")
        self.add_to_cart_bike_light = page.locator("[data-test=\"add-to-cart-sauce-labs-bike-light\"]")

    # Methods (Wrapper)
    def sort_products_by(self, option: str):
        # option is one of: az, za, lohi, hilo
        self.sort_dropdown.select_option(option)

    def go_to_cart(self) -> CartPage:
        self.cart_icon.click()
        return CartPage(self.page)

    def add_item_to_cart(self, item):
        #   sauce-labs-backpack
        #   self.add_item_to_cart().click()
        self.page.locator(f"[data-test=\"add-to-cart-{item}\"]").click()
        return self

    # Getters (are used for assertions later.)
    def get_title(self):
        return self.title

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