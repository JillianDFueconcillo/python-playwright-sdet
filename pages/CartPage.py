from playwright.sync_api import Page

from pages.CheckoutPage import CheckoutPage


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page_title = page.locator("[data-test=\"title\"]")
        self.inventory_item = page.locator("[data-test=\"inventory-item\"]")
        self.item_name = page.locator("[data-test=\"inventory-item-name\"]")
        self.item_description = page.locator("[data-test=\"inventory-item-desc\"]")
        self.inventory_price = page.locator("[data-test=\"inventory-item-price\"]")
        self.checkout_button = page.locator("[data-test=\"checkout\"]")
        self.continue_shopping = page.locator("[data-test=\"continue-shopping\"]")
        self.remove_item = page.locator("[data-test=\"remove-sauce-labs-backpack\"]")

    def go_to_checkout(self) -> CheckoutPage:
        self.checkout_button.click()
        return CheckoutPage(self.page)


    # Getters
    def get_page_title(self):
        return self.page_title

    def get_checkout_button(self):
        return self.checkout_button

    def get_item_count(self):
        return self.inventory_item.count()

    def get_item_name(self):
        return self.item_name.all_text_contents()
