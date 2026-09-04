# AGENTS.md

Python SDET framework for **Swag Labs** (browser) and **restful-booker** (REST). Stack: Python 3.12, pytest, Playwright (UI only), requests (API only), Allure.

This file is the source of truth for how to add and change tests. Follow it over older examples in the repo that still import Playwright `expect()`.

## Apps under test

| Suite | App | Base URL |
|---|---|---|
| UI | [Swag Labs](https://www.saucedemo.com/) | `https://www.saucedemo.com/` |
| API | [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) | `https://restful-booker.herokuapp.com` |

## Layout

```
pages/                     Page Object Model — locators, actions, getters. No assertions.
  LoginPage.py
  InventoryPage.py
  CartPage.py
  CheckoutPage.py          Information + overview + complete in one class

api/                       Same idea for HTTP — one method per endpoint. No assertions.
  booking_client.py        BookingAPIClient wrapping a requests session
  builders.py              make_booking() — unique valid payloads

tests/ui/                  Browser tests (pytest-playwright `page` fixture)
tests/api/                 HTTP tests (requests). Own conftest.py.

conftest.py                UI fixtures and auth storage_state
pytest.ini                 base_url, chromium, html + Allure, pythonpath = .
support/allure_hooks.py    Failure attachments; registered via pytest_plugins
.github/workflows/tests.yml  UI job, API job, Allure publish on master
```

Run everything from the **repo root** with `python -m pytest` so `pages` and `api` import.

## Architecture

```
pytest.ini  ── defaults (base_url, browser, artifacts)
     │
conftest.py ── UI fixtures
     │         page → login_page
     │         auth_state (session) → logged_in_page → inventory_page
     │                                              → cart_with(*item_ids)
     │                                              → checkout_started → completed_order
     │
tests/api/conftest.py
     │         api_session → auth_token → booking_client
     │         created_booking  (create → yield → delete)

UI tests  ── page objects ── Playwright locators on a live page
API tests ── BookingAPIClient ── requests.Session (ApiSession adds base URL + timeout)
```

**Page objects and API clients never assert.** They expose locators, getters, and actions. Tests decide what “correct” means with pytest `assert`.

**Page objects are stateless.** They store `page` and locators only. No cached totals, usernames, or step counters. Read live UI state every time.

**Navigation returns the next screen; staying put returns `self`.** That is how tests chain:

```python
cart_page = inventory_page.add_item_to_cart("sauce-labs-backpack").open_cart()
checkout_started.fill_information("Solid", "Snake", "00001").finish()
```

Local imports inside methods (`from pages.LoginPage import LoginPage`) break circular imports. Keep that pattern when a page navigates backward.

## How to write UI tests

1. Put locators and actions in `pages/`. Put the test in `tests/ui/`.
2. Request the fixture that already has the app in the right state. Do not re-login at the top of every test.
3. Assert with pytest `assert` only. Never Playwright `expect()`.
4. Never `time.sleep()` or `page.wait_for_timeout()`. Locator `click` / `fill` / `text_content` / `inner_text` auto-wait.

```python
# Good
def test_locked_out_user_sees_error(login_page: LoginPage):
    login_page.login_user("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.get_error_message().text_content()

def test_inventory_title(inventory_page: InventoryPage):
    assert inventory_page.get_title().text_content() == "Products"
```

```python
# Bad — assertion in the page object, or Playwright expect()
expect(login_page.get_error_message()).to_contain_text("locked out")
time.sleep(3)
assert page.locator("[data-test='title']").is_visible()
```

### UI fixtures (root `conftest.py`)

| Fixture | What the test gets |
|---|---|
| `login_page` | Login screen open (logged out) |
| `inventory_page` | Logged in as `standard_user` on `/inventory.html` |
| `cart_with(*item_ids)` | Factory: add those products, return `CartPage` |
| `checkout_started` | Backpack in cart, on checkout information |
| `completed_order` | Finished order, on the thank-you screen |
| `logged_in_page` | Fresh Playwright `Page` with saved `storage_state` |

`auth_state` logs in once per session and writes `playwright/.auth/state.json`. `inventory_page` and everything downstream reuse that session. Credentials: `SAUCE_USERNAME` / `SAUCE_PASSWORD` from `.env` or CI secrets, defaulting to `standard_user` / `secret_sauce`.

Prefer `data-test` locators, matching the existing page objects.

## How to write API tests

1. Call `BookingAPIClient` methods. Do not use Playwright `APIRequestContext` or `playwright.request`.
2. Build payloads with `make_booking(**overrides)` from `api.builders`.
3. Assert with pytest `assert` on `status_code` and `response.json()`.
4. Use `created_booking` when the test needs an existing record. It yields `(booking_id, payload)` and deletes after the test, including on failure.

```python
def test_created_booking_reads_back(booking_client, created_booking):
    booking_id, payload = created_booking
    r = booking_client.get_booking(booking_id)
    assert r.status_code == 200
    assert r.json() == payload
```

```python
# Bad
response = api_context.post("/booking", data=payload)
expect(response).to_be_ok()
```

`make_booking()` always produces a unique first/last name so parallel or repeated runs do not collide. Override fields for negative cases: `make_booking(totalprice=-5)`.

`ApiSession` in `tests/api/conftest.py` prefixes the base URL and sets `timeout=10`. New HTTP helpers belong on `BookingAPIClient`, not inline `requests.get` in every test (except one-off auth/ping checks).

Mark API modules with `pytestmark = pytest.mark.api` when adding a new file.

## Hard rules

1. **No `assert` / `expect()` in `pages/` or `api/`.** Tests own checks.
2. **UI and API tests use pytest `assert` only.** Never Playwright `expect()`.
3. **API HTTP is `requests` only.**
4. **Never sleep.** Rely on Playwright auto-wait, then assert.
5. **Never weaken a failing check.** Fix the app, locator, wait, or data. Do not skip, delete the assertion, or broaden the expected value to go green.
6. **Each test stands alone.** Create data in the test or a fixture; clean it up after `yield`. No order dependence.
7. **Setup that is not the point of the test belongs in a fixture.**
8. **Secrets stay in `.env` / GitHub secrets.** Never commit credentials.

## Running tests

```bash
python -m venv venv
venv\Scripts\Activate.ps1          # Windows
pip install -r requirements.txt
playwright install chromium

python -m pytest                   # everything
python -m pytest --headed          # watch the browser
python -m pytest tests/api         # API only
python -m pytest --ignore=tests/api
python -m pytest -k checkout
python -m pytest --setup-show
```

Each run writes `report.html`. Failures also leave screenshot, video, and trace under `test-results/`. Open traces at [trace.playwright.dev](https://trace.playwright.dev). Allure raw results go to `allure-results/` (`--alluredir` in `pytest.ini`).

## CI

`.github/workflows/tests.yml` on every push:

- **ui-tests** — `xvfb-run python -m pytest --ignore=tests/api` (needs Chromium + Sauce secrets)
- **api-tests** — `python -m pytest tests/api -v` (no browser)
- **allure-report** — merges both lanes; publishes to GitHub Pages only from `master`

Always upload artifacts with `if: always()` so failures still produce a report.

## When adding work

| Change | Where |
|---|---|
| New screen / control | New or existing class in `pages/` |
| New booking endpoint | Method on `BookingAPIClient` |
| New payload shape | `make_booking()` override or builder |
| New UI scenario | `tests/ui/test_*.py`, request an existing fixture |
| New API scenario | `tests/api/test_*.py`, request `booking_client` / `created_booking` |
| Shared UI setup | Root `conftest.py` |
| Shared API setup | `tests/api/conftest.py` |
| Reporting only | `support/allure_hooks.py` |

Older files under `tests/ui/` (`test_internet.py`, `test_demoqa.py`, `test_login.py`, `test_e2e_swag_labs.py`) may still use `expect()` or raw locators. Do not copy that style. New tests follow this file and `.cursor/rules/new-automated-tests.mdc`.
