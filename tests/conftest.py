import logging
import os
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.new_purchase_order_page import NewPurchaseOrderPage
from pages.product_page import ProductPage
from pages.purchase_order_history_page import PurchaseOrderHistoryPage

ROOT_DIR = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:8000"
LOGIN_STATE_FILE = ROOT_DIR / "login_state.json"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )


@pytest.fixture(scope="session")
def credentials():
    load_dotenv(dotenv_path=ROOT_DIR / ".env")

    creds = {
        "email": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD"),
    }

    missing = [key for key, value in creds.items() if value is None]
    if missing:
        raise ValueError(f"Missing keys in .env file: {', '.join(missing)}")

    return creds


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, request) -> Browser:
    headless = request.config.getoption("--headless")
    browser = playwright_instance.chromium.launch(
        headless=headless,
        args=["--start-maximized"]
    )
    yield browser
    browser.close()


@pytest.fixture
def context(browser, request) -> BrowserContext:
    video_dir = Path("test_artifacts/videos")
    video_dir.mkdir(parents=True, exist_ok=True)

    scenario_tags = request.node.get_closest_marker("use_store_state")

    request.node.use_state = scenario_tags is not None and LOGIN_STATE_FILE.exists()

    context = browser.new_context(
        record_video_dir=str(video_dir),
        no_viewport=True,
        storage_state=str(LOGIN_STATE_FILE) if request.node.use_state else None
    )

    yield context
    context.close()


@pytest.fixture
def page(context, request) -> Page:
    page = context.new_page()

    if request.node.use_state:
        page.goto(BASE_URL + "/login")
        page.fill("#email", "test_user@gmail.com")
        page.fill("#password", "Test600!")
        page.click("//button[@type='submit' and text()='Login']")
    else:
        page.goto(BASE_URL + "/login")

    # Log browser console messages
    page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))

    yield page
    page.close()


# def pytest_bdd_before_scenario(request, scenario):
#     if "use_"


@pytest.fixture(scope="session", autouse=True)
def generate_login_state(playwright_instance, request):
    if LOGIN_STATE_FILE.exists():
        return

    headless = request.config.getoption("--headless")

    browser = playwright_instance.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    # Perform login manually
    page.goto(BASE_URL + "/login")
    page.fill("#email", "test_user@gmail.com")
    page.fill("#password", "Test600!")
    page.click("//button[@type='submit' and text()='Login']")

    # Save login state
    context.storage_state(path=LOGIN_STATE_FILE)
    print(f"[STATE CREATED] Login state saved to: {LOGIN_STATE_FILE}")

    context.close()
    browser.close()


def save_login_state(page: Page):
    page.context.storage_state(path=LOGIN_STATE_FILE)
    print(f"[STATE SAVED] Login state saved to {LOGIN_STATE_FILE}")


def pytest_sessionfinish(session, exitstatus):
    if LOGIN_STATE_FILE.exists():
        LOGIN_STATE_FILE.unlink()
        print(f"[CLEANUP] Deleted login state file: {LOGIN_STATE_FILE}")


def pytest_runtest_makereport(item, call):
    if call.when == "call":
        outcome = call.excinfo
        test_name = item.name
        context = item.funcargs.get("context")
        page = item.funcargs.get("page")

        if outcome is not None:
            # Test failed
            if context and page:
                screenshot_dir = Path("test_artifacts/screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                screenshot_path = screenshot_dir / f"{test_name}.png"
                try:
                    page.screenshot(path=str(screenshot_path))
                    print(f"[SCREENSHOT] Saved to: {screenshot_path}")
                except PlaywrightError as e:
                    print(f"[ERROR] Failed to take screenshot: {e}")

                try:
                    video_path = page.video.path()
                    print(f"[VIDEO] Saved to: {video_path}")
                except (AttributeError, PlaywrightError) as e:
                    print(f"[ERROR] Could not retrieve video path: {e}")
        else:
            # Test passed, clean up video if it exists
            try:
                video_path = page.video.path()
                if video_path and os.path.exists(video_path):
                    os.remove(video_path)
            except (AttributeError, PlaywrightError, FileNotFoundError) as e:
                print(f"[INFO] Skipping video cleanup: {e}")


@pytest.fixture
def test_context():
    class Ctx:
        product_type = None
        product_unit = None
        product_group = None
        product_supplier = None
        product = None

    return Ctx()


@pytest.fixture
def auth_headers():
    login_url = f"{BASE_URL}/auth/login"
    credentials = {
        "email": "test_user@gmail.com",
        "password": "Test600!"
    }

    response = requests.post(login_url, json=credentials)
    assert response.status_code == 200, f"Login failed: {response.text}"

    token = response.json().get("access_token")
    assert token, "No access token returned"

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(page: Page) -> DashboardPage:
    return DashboardPage(page)


@pytest.fixture(scope="function")
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture(scope="function")
def new_purchase_order_page(page: Page) -> NewPurchaseOrderPage:
    return NewPurchaseOrderPage(page)


@pytest.fixture(scope="function")
def purchase_order_history_page(page: Page) -> PurchaseOrderHistoryPage:
    return PurchaseOrderHistoryPage(page)
