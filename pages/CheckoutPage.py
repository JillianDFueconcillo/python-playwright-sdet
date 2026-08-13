from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page_title = page.locator("[data-test=\"title\"]")
        self.first_name = page.locator("[data-test=\"firstName\"]")
        self.last_name = page.locator("[data-test=\"lastName\"]")
        self.postal_code = page.locator("[data-test=\"postalCode\"]")
        self.continue_button = page.locator("[data-test=\"continue\"]")
        self.cancel_button = page.locator("[data-test=\"cancel\"]")
        self.error_message = page.locator("[data-test=\"error\"]")
        self.subtotal_label = page.locator("[data-test=\"subtotal-label\"]")
        self.tax_label = page.locator("[data-test=\"tax-label\"]")
        self.total_label = page.locator("[data-test=\"total-label\"]")
        self.finish_button = page.locator("[data-test=\"finish\"]")
        self.complete_header = page.locator("[data-test=\"complete-header\"]")
        self.complete_text = page.locator("[data-test=\"complete-text\"]")
        self.back_home_button = page.locator("[data-test=\"back-to-products\"]")

    def fill_checkout_information(self, first: str, last: str, postal_code: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal_code)
        return self

        #Methods
        def fill_out_form(self):
            self.first_name.fill("John")
            self.last_name.fill("Doe")
            self.postal_code.fill("12345")
            self.continue_button.click()
            return self

        #getters
        def get_page_title(self):
            return self.page_title
            
        def get_continue_button(self):
            return self.continue_button

    def get_finish_button(self):
        return self.finish_button

    def get_complete_header(self):
        return self.complete_header

    def get_complete_text(self):
        return self.complete_text

    def get_subtotal_label(self):
        return self.subtotal_label

    def get_total_label(self):
        return self.total_label

    def get_error_message(self):
        return self.error_message
