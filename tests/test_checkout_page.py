from pages.InventoryPage import InventoryPage


def test_fill_out_page_is_visible(inventory_page: InventoryPage):
    cart_page = inventory_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    assert checkout_page.get_page_title().text_content() == "Checkout: Your Information"
    assert checkout_page.get_continue_button().is_visible()


def test_all_information(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    cart_page = inventory_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    checkout_page.fill_checkout_information("John", "Doe", "12345")
    checkout_page.continue_to_overview()

    assert checkout_page.get_page_title().text_content() == "Checkout: Overview"
    assert checkout_page.get_subtotal_label().is_visible()
    assert checkout_page.get_total_label().is_visible()
    assert checkout_page.get_finish_button().is_visible()


def test_verify_thank_you_message(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    cart_page = inventory_page.go_to_cart()
    checkout_page = cart_page.go_to_checkout()

    checkout_page.fill_checkout_information("John", "Doe", "12345")
    checkout_page.continue_to_overview()
    checkout_page.finish_order()

    assert checkout_page.get_complete_header().text_content() == "Thank you for your order!"
    assert "Your order has been dispatched" in checkout_page.get_complete_text().text_content()
