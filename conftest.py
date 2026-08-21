import os
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv

from pages.CheckoutPage import CheckoutPage
from pages.LoginPage import LoginPage
from pages.InventoryPage import InventoryPage


load_dotenv()



# Sauce Demo's public credentials. GitHub Actions resolves missing secrets to
# "", so `or` is required — `os.getenv` alone would still log in as empty.
USERNAME = os.getenv("SAUCE_USERNAME") or "standard_user"
PASSWORD = os.getenv("SAUCE_PASSWORD") or "secret_sauce"
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

AUTH_STATE_PATH = "playwright/.auth/state.json"

# browser > context > page
@pytest.fixture(scope="session")
def auth_state(browser):

    # Created the path
    os.makedirs(os.path.dirname(AUTH_STATE_PATH), exist_ok=True)
    context = browser.new_context(base_url=BASE_URL)

    login_page = LoginPage(context.new_page())
    login_page.open()
    login_page.login_user(USERNAME, PASSWORD)
    # Setup guard: prove the login WORKED before saving the session.
    # Without this, a failed login saves a logged-out state.json and every
    # downstream test times out on inventory locators instead.
    try:
        login_page.page.wait_for_url("**/inventory.html")
    except Exception:
        error = login_page.get_error_message()
        error_text = error.inner_text() if error.is_visible() else "(no error banner)"
        pytest.fail(
            f"auth_state login never reached inventory.html "
            f"(url={login_page.page.url!r}, error={error_text!r}). "
            "SAUCE_USERNAME / SAUCE_PASSWORD must be Sauce Demo credentials "
            "(standard_user / secret_sauce), not a Sauce Labs account."
        )
    context.storage_state(path=AUTH_STATE_PATH)
    context.close()

    return AUTH_STATE_PATH

@pytest.fixture                            # runs per test
def logged_in_page(new_context, auth_state):
    return new_context(storage_state=auth_state).new_page()   # fresh page, already logged in

# Fixtures
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """A LoginPage already open at the login screen."""
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture
def inventory_page(logged_in_page: Page) -> InventoryPage:
    """Logged in as standard_user, sitting on the products page."""
    logged_in_page.goto("/inventory.html")
    return InventoryPage(logged_in_page)

@pytest.fixture
def checkout_started(inventory_page: InventoryPage) -> CheckoutPage:
    inventory_page.add_item_to_cart("sauce-labs-backpack")
    #          Inventory.open_cart() - > CartPage : CartPage.start_checkout() ->CheckoutPage
    return inventory_page.open_cart().start_checkout()

@pytest.fixture
def completed_order(checkout_started: CheckoutPage) -> CheckoutPage:
    return checkout_started.fill_information("Solid", "Snake", "00001").finish()


@pytest.fixture
def cart_with(inventory_page: InventoryPage):
    def _cart_with(*item_ids: str):
        for item_id in item_ids:
            inventory_page.add_item_to_cart(item_id)
        return inventory_page.open_cart()
    return _cart_with