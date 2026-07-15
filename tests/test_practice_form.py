# test case 1: Click Action
from playwright.sync_api import Page, expect


def test_practice_form(page: Page) -> None:
    page.goto("https://demoqa.com/automation-practice-form")

    page.get_by_role("textbox", name="First Name").fill("efwefweffe")
    page.get_by_role("textbox", name="Last Name").fill("wqefwefwef")
    page.get_by_role("textbox", name="name@example.com").fill(
        "fwefwifiwoefjweoi38@email.com"
    )
    page.get_by_role("radio", name="Female").check()
    page.get_by_role("textbox", name="Mobile Number").fill("5555555555")

    # Datepicker: year/month are <select>s; day is a gridcell you click
    page.locator("#dateOfBirthInput").click()
    page.locator(".react-datepicker__year-select").select_option("1915")
    page.locator(".react-datepicker__month-select").select_option("June")
    page.locator(
        ".react-datepicker__day--014:not(.react-datepicker__day--outside-month)"
    ).click()

    page.get_by_role("checkbox", name="Sports").check()

    page.locator("#uploadPicture").set_input_files("tests/uploadpicture.jpg")
    page.get_by_role("button", name="Submit").click()

    expect(page.locator("#example-modal-sizes-title-lg")).to_have_text(
        "Thanks for submitting the form"
    )
