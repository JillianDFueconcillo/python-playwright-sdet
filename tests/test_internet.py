import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.parametrize(
    "first, last, email",
    [
        ("John", "Smith", "johnsmith@gmail.com"),
        ("Jane", "Doe", "janedoe@gmail.com"),
        ("Maria", "Garcia", "mariagarcia@yahoo.com"),
        ("Wei", "Chen", "weichen@outlook.com"),
        ("Aisha", "Patel", "aishapatel@proton.me"),
    ],
)
def test_form(page: Page, first, last, email) -> None:
    page.goto("https://demoqa.com/automation-practice-form")
    page.get_by_role("textbox", name="First Name").fill(first)
    page.get_by_role("textbox", name="Last Name").fill(last)
    page.get_by_role("textbox", name="name@example.com").fill(email)
    page.get_by_role("radio", name="Male", exact=True).check()
    page.get_by_role("textbox", name="Mobile Number").fill("1231234567")
    page.get_by_role("button", name="Submit").click()
    expect(page.locator("#example-modal-sizes-title-lg")).to_contain_text("Thanks for submitting the form")


@pytest.mark.parametrize(
    "link", 
    [
        "random_data.txt", "sample.txt", "sample.pdf"    
    ],             
)
def test_download(page: Page, link: str) -> None:
    page.goto("https://the-internet.herokuapp.com/download")
    with page.expect_download() as download_info:
        page.get_by_role("link", name=link).click()
    download = download_info.value
    assert link in str(download)

    
def test_hidden_ad(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/entry_ad")
    modal = page.locator("#modal")
    # Wait for the modal to load
    assert modal.is_visible()

    page.get_by_text("Close", exact=True).click()
    modal.wait_for(state="hidden")

    assert not modal.is_visible()
    
    
    
@pytest.mark.parametrize(
    "username, password, expected_text",
    [
        ("tomsmith", "SuperSecretPassword!", "Welcome to the Secure Area. When you are done click logout below."),
        ("invaliduser", "SuperSecretPassword!", "Your username is invalid!"),
        ("tomsmith", "wrongpassword", "Your password is invalid!"),
        ("johndoe", "password123", "Your username is invalid!"),
        ("tomsmith", "SuperSecretPassword", "Your password is invalid!"),
    ],
)
def test_fill_and_press(page: Page, username: str, password: str, expected_text: str) -> None:
    # 1. Go to Page
    page.goto("https://the-internet.herokuapp.com/login")
    username_field = page.get_by_label("Username")
    password_field = page.get_by_label("Password")

    username_field.fill(username)
    username_field.press("Tab")
    password_field.fill(password)
    password_field.press("Enter")

    # Store the text from the page as actual result THEN compare against expected result in assert statement
    if expected_text.startswith("Welcome"):
        actual_text = page.get_by_role("heading", name="Welcome to the Secure Area.").text_content()
    else:
        actual_text = page.locator("#flash").text_content()
    assert expected_text in actual_text