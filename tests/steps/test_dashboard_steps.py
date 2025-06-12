import logging

from playwright.sync_api import expect
from pytest_bdd import given, scenarios, when, then

from tests.conftest import ROOT_DIR

scenarios(ROOT_DIR / "tests" / "features" / "dashboard.feature")


@given("user is on dashboard page")
@when("the user inspects the following sections")
def dummy_test_step():
    logging.info("Into dummy test step without params.")


@then("they are all visible and enabled")
def verify_dashboard_buttons_visible_enabled(dashboard_page):
    expect(dashboard_page.toggle_side_menu_button).to_be_visible()
    expect(dashboard_page.toggle_side_menu_button).to_be_enabled()
    expect(dashboard_page.stocktake_side_menu_button).to_be_visible()
    expect(dashboard_page.stocktake_side_menu_button).to_be_enabled()
    expect(dashboard_page.new_product_side_menu_button).to_be_visible()
    expect(dashboard_page.new_product_side_menu_button).to_be_enabled()
    expect(dashboard_page.transfers_side_menu_button).to_be_visible()
    expect(dashboard_page.transfers_side_menu_button).to_be_enabled()
    expect(dashboard_page.requests_side_menu_button).to_be_visible()
    expect(dashboard_page.requests_side_menu_button).to_be_enabled()
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_visible()
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_enabled()
    dashboard_page.purchase_orders_side_menu_button.click()
    expect(dashboard_page.new_purchase_order_side_menu_button).to_be_visible()
    expect(dashboard_page.new_purchase_order_side_menu_button).to_be_enabled()
    expect(dashboard_page.draft_purchase_orders_side_menu_button).to_be_visible()
    expect(dashboard_page.draft_purchase_orders_side_menu_button).to_be_enabled()
    expect(dashboard_page.purchase_orders_history_side_menu_button).to_be_visible()
    expect(dashboard_page.purchase_orders_history_side_menu_button).to_be_enabled()
    expect(dashboard_page.stores_side_menu_button).to_be_visible()
    expect(dashboard_page.stores_side_menu_button).to_be_enabled()
    expect(dashboard_page.logout_side_menu_button).to_be_visible()
    expect(dashboard_page.logout_side_menu_button).to_be_enabled()
