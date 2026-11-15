from playwright.sync_api import Page


class ProductPage:
    """A single product's detail screen at /inventory-item.html."""

    def __init__(self, page: Page) -> None:
        # Locators — scraped from inventory-item.html (data-test on the live DOM).
        self.page = page
        self.details = page.locator("[data-test=\"inventory-item\"]")
        self.image = self.details.locator("img[data-test$=\"-img\"]")
        self.name = page.locator("[data-test=\"inventory-item-name\"]")
        self.description = page.locator("[data-test=\"inventory-item-desc\"]")
        self.price = page.locator("[data-test=\"inventory-item-price\"]")

        # Detail page uses add-to-cart / remove — not add-to-cart-{item_id}.
        self.add_to_cart_button = page.locator("[data-test=\"add-to-cart\"]")
        self.remove_button = page.locator("[data-test=\"remove\"]")
        self.back_to_products_button = page.locator("[data-test=\"back-to-products\"]")
        self.cart_link = page.locator("[data-test=\"shopping-cart-link\"]")
        self.cart_badge = page.locator("[data-test=\"shopping-cart-badge\"]")

    # Methods (Wrapper)
    def open(self, item_id: int):
        self.page.goto(f"/inventory-item.html?id={item_id}")
        return self

    def add_to_cart(self):
        self.add_to_cart_button.click()
        self.remove_button.wait_for()
        return self

    def remove_from_cart(self):
        self.remove_button.click()
        self.add_to_cart_button.wait_for()
        return self

    def back_to_products(self):
        from pages.InventoryPage import InventoryPage

        self.back_to_products_button.click()
        inventory_page = InventoryPage(self.page)
        inventory_page.get_sort_dropdown().wait_for()
        return inventory_page

    def open_cart(self):
        from pages.CartPage import CartPage

        self.cart_link.click()
        cart_page = CartPage(self.page)
        cart_page.get_checkout_button().wait_for()
        return cart_page

    # Getters (are used for assertions later.)
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_image(self):
        return self.image

    def get_add_to_cart_button(self):
        return self.add_to_cart_button

    def get_remove_button(self):
        return self.remove_button

    def get_back_to_products_button(self):
        return self.back_to_products_button

    def get_price(self):
        price_text = self.price.text_content()
        return float(price_text.replace("$", ""))

    def get_cart_badge(self):
        return self.cart_badge

    # CLASSES SHOULD NOT HAVE ANY ASSERTS(or Expects)
