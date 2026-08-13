from pages.InventoryPage import InventoryPage


def test_cart_page_load(inventory_page: InventoryPage):
    cart_page = inventory_page.go_to_cart()

    assert cart_page.get_page_title().text_content() == "Your Cart"
    assert cart_page.get_checkout_button().is_visible()

# Parameterise Later
def test_add_item_to_cart(page: Page):
    login_page = LoginPage(page)
    inventory_page = login_page.login_standard_user()

def test_add_item_to_cart(inventory_page: InventoryPage):
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    cart_page = inventory_page.go_to_cart()

    # assert the item count went up
    assert cart_page.get_item_count() == 1
    # assert the item name is correct
    assert cart_page.get_item_count() == ["Sauce Labs Backpack"]


    # Parameterized example: same steps, four different products.
    # PYTEST runs this test once per row, so one test becomes four.
    @pytest.mark.parametrize(
        "item_id, item_name",
        [
        (sauce-labs-backpack", "Sauce Labs Backpack"),
        ("sauce-labs-bike-light", "Sauce Labs Bike Light"),
        ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
        ("sauce-labs-onesie", "Sauce Labs Onesie"),
        ],
    )
def test_each_product_can_be_added(page: Page, item_id, item_name:
    inventory_page.add_item_to_cart(item_id)
    cart_page = inventory_page.go_to_cart()

    assert cart_page.get_item_count() == 1
    assert item_name in cart_page.get_item_names()


#1 Assignmentt 1: add two, check both names, remove one, count is 1
def test_remove_one_item_from_cart(inventory_page: InventoryPage,):

    inventory_page.add_item_to_cart("sauce-labs-backpack")
    inventory_page.add_item_to_cart("sauce-labs-bike-light")

    cart_page = inventory_page.open_cart()

    # both products are in the cart
    assert cart_page.get_item_count() == 2
    names = cart_page.get_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names

    # remove one of them
    cart_page.remove_item("sauce-labs-backpack")

    assert cart_page.get_item_count() == 1
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]


    # remove_item returns self, so calls can be chained.
    def rest_remove_both_items_by_chaining(page: Page):

        inventory_page.add_item_to_cart("sauce-labs-backpack")
        inventory_page.add_item_to_cart("sauce-labs-bike-light")

        cart_page = inventory_page.open_cart()
        cart_page.remove_item("sauce-labs-backpack").remove_item("sauce-labs-bike-light")

        assert cart_page.get_item_count() == 0

# Assignement 4: logout. cartpage..logout() imports LoginPage inside the method,
# which is how we avoid the circular import between the page files
def test_logout_from_cart(inventory_page: InventoryPage):
    cart_page = inventory_page.open_cart()
    login_page_again = cart_page.logout()

    # Back on the login scree: the credentials box is on show again
    assert login_page_again.get_login_credentials().visible()