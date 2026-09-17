import pytest

from pages.CheckoutPage import CheckoutPage


def test_checkout_happy(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "Snake", "00001")
    assert checkout_started.get_title().text_content() == "Checkout: Overview"
    #                  Returns a List
    assert checkout_started.get_item_names() == ["Sauce Labs Backpack"]

    checkout_started.finish()
    assert checkout_started.get_complete_header().text_content() == "Thank you for your order!"


# Parameterized example: the same flow with different customers.
@pytest.mark.parametrize(
    "first_name, last_name, postal_code",
    [
        ("Solid", "Snake", "00001"),
        ("Ada", "Lovelace", "SW1A 1AA"),
        ("Grace", "Hopper", "12345"),
        ("Alan", "Turing", "M1 1AE"),
    ],
)
def test_checkout_with_different_customers(
    checkout_started: CheckoutPage, first_name, last_name, postal_code
):
    checkout_started.fill_information(first_name, last_name, postal_code).finish()
    assert checkout_started.get_complete_header().text_content() == "Thank you for your order!"


# Exact checkout-step-one copy (h3[data-test=error]). Empty first name is
# checked first, so first+last empty and all-empty use the first-name message.
FIRST_NAME_REQUIRED = "Error: First Name is required"
LAST_NAME_REQUIRED = "Error: Last Name is required"
POSTAL_CODE_REQUIRED = "Error: Postal Code is required"


# Parameterized sad path: the SAME fill_information() method, but here we expect
# an error. The page object stays neutral; the test decides what "correct" means.
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, error",
    [
        ("", "Snake", "00001", FIRST_NAME_REQUIRED),
        ("Solid", "", "00001", LAST_NAME_REQUIRED),
        ("Solid", "Snake", "", POSTAL_CODE_REQUIRED),
        ("", "", "00001", FIRST_NAME_REQUIRED),
        ("", "", "", FIRST_NAME_REQUIRED),
    ],
    ids=[
        "empty_first_name",
        "empty_last_name",
        "empty_postal_code",
        "empty_first_and_last",
        "all_three_empty",
    ],
)
def test_checkout_form_requires_all_fields(
    checkout_started: CheckoutPage, first_name, last_name, postal_code, error
):
    checkout_started.fill_information(first_name, last_name, postal_code)

    #                 expected  vs  actual
    assert checkout_started.get_error_message().text_content() == error
    # And we never left step one
    assert checkout_started.get_title().text_content() == "Checkout: Your Information"


def test_checkout_200_character_values(checkout_started: CheckoutPage):
    long_value = "A" * 200
    checkout_started.fill_information(long_value, long_value, long_value)
    # TODO: Sauce Demo does not document a max length, truncation, or error for
    # 200-character checkout fields. Confirm whether Continue reaches
    # "Checkout: Overview" or stays on step one, then assert that outcome.


def test_checkout_unicode_values(checkout_started: CheckoutPage):
    checkout_started.fill_information("名前", "фамилия", "東京-100-0001")
    # TODO: Sauce Demo does not document whether unicode first name, last name,
    # or postal code is accepted. Confirm whether Continue reaches
    # "Checkout: Overview" or shows an error, then assert that outcome.


# The overview totals: subtotal is the price of what we added ($29.99).
def test_checkout_overview_subtotal(checkout_started: CheckoutPage):
    checkout_started.fill_information("Solid", "Snake", "00001")

    assert checkout_started.get_subtotal() == 29.99
    # Total is subtotal plus tax, so it must be larger
    assert checkout_started.get_total() > checkout_started.get_subtotal()


# After ordering, "Back Home" returns us to the products page.
def test_back_home_after_order(completed_order: CheckoutPage):
    assert completed_order.back_home().get_title().text_content() == "Products"
