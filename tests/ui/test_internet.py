# Test Case 1: Click Action
import uuid
from pathlib import Path

from playwright.sync_api import Page
import pytest


def test_click_action(page: Page):
    add_element_button = page.get_by_role("button", name="Add Element")
    delete_button = page.get_by_role("button", name="Delete")
    # 1. Go to Page
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    # 2. Click on the Add Element button
    add_element_button.click()
    add_element_button.click()
    # 3. Click on the Delete button
    delete_button.first.click()
    # for b in delete_button.all():
    #     b.click()
    assert delete_button.is_visible()



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




def test_checkboxes(page: Page):
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    boxes = page.get_by_role("checkbox")

    boxes.first.check()
    boxes.last.uncheck()

    assert boxes.first.is_checked()
    assert not boxes.last.is_checked()


def test_dropdown(page: Page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dropdown = page.locator("#dropdown")

    dropdown.select_option("2")
    dropdown.select_option(label="Option 1")
    dropdown.select_option(index=2)
    assert dropdown.input_value() == "2"

def test_hovers(page: Page):
    page.goto("https://the-internet.herokuapp.com/hovers")
    image= page.locator(".figure").first
    image.hover()
    assert page.get_by_role("heading", name="name: user1").is_visible()

def test_upload(page: Page):
    page.goto("https://the-internet.herokuapp.com/upload")
    resume = Path(__file__).resolve().parents[2] / "test_data" / "resume.txt"
    page.locator("#file-upload").set_input_files(resume)
    page.locator("#file-submit").click()
    assert "resume.txt" in page.locator("#uploaded-files").text_content()

def test_drag_and_drop(page: Page):
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    a = page.locator("#column-a")
    b = page.locator("#column-b")

    a.drag_to(b)
    b.drag_to(a)

def test_context_menu(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/context_menu")
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("#hot-spot").click(button="right")


def test_upload_then_download_roundtrip(page: Page, tmp_path) -> None:
    """Upload a unique file, then download a file that actually exists on /download.

    the-internet stores /upload and /download in different folders, so the file
    we upload will not show up on /download. Prove upload by filename, then
    download the first listed file (page.expect_download waits for the event;
    that is not Playwright expect()).
    """
    file_name = f"pliskin-{uuid.uuid4().hex[:8]}.txt"
    local_file = tmp_path / file_name
    local_file.write_text("uploaded by the pliskin_june11 test suite")

    page.goto("https://the-internet.herokuapp.com/upload")
    page.locator("#file-upload").set_input_files(local_file)
    page.locator("#file-submit").click()
    assert page.locator("#uploaded-files").text_content().strip() == file_name

    page.goto("https://the-internet.herokuapp.com/download")
    file_link = page.locator(".example a").first
    listed_name = file_link.text_content().strip()
    assert listed_name

    with page.expect_download() as download_info:
        file_link.click()
    download = download_info.value
    assert download.suggested_filename == listed_name
    saved = tmp_path / listed_name
    download.save_as(saved)
    assert saved.exists()
    assert saved.stat().st_size > 0


def test_hidden_ad(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/entry_ad")
    modal = page.locator("#modal")
    # Wait for the modal to load
    modal.wait_for(state="visible")
    assert modal.is_visible()

    page.get_by_text("Close", exact=True).click()
    modal.wait_for(state="hidden")
    assert not modal.is_visible()