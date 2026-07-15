from calendar import firstweekday
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
    page.get_by_role("textbox", name="First Name").click()
    page.get_by_role("textbox", name="First Name").fill(first)
    page.get_by_role("textbox", name="Last Name").click()
    page.get_by_role("textbox", name="Last Name").fill(last)
    page.get_by_role("textbox", name="Last Name").click()
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill(email)
    page.get_by_role("radio", name="Male", exact=True).click()
    page.get_by_role("textbox", name="Mobile Number").click()
    page.get_by_role("textbox", name="Mobile Number").fill("1234567891")
    page.get_by_role("textbox", name="Mobile Number").click()
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Thanks for submitting the form")).to_be_visible()
    page.get_by_text("Thanks for submitting the form").dblclick()
    page.locator("div").filter(has_text="Thanks for submitting the form").nth(3).click()
    page.get_by_text("Thanks for submitting the form").dblclick()
    page.locator("div").filter(has_text="Thanks for submitting the form").nth(3).click()
