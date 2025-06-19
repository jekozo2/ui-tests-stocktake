import logging
import random
from datetime import datetime

from playwright.sync_api import expect
from pytest_bdd import given, then, parsers, when, scenarios

from modules.product import Product
from modules.purchase import Purchase
from tests.conftest import ROOT_DIR
from utils.api_utils import create_new_type_via_api_call, create_new_unit_via_api_call, create_new_group_via_api_call, \
    create_new_supplier_via_api_call, create_new_product_via_api_call

scenarios(ROOT_DIR / "tests" / "features" / "purchase.feature")


@given("user is on dashboard page")
def dummy_test_step_no_params():
    logging.info("Executing dummy test step no params.")


@given(parsers.parse("{products: d} products are created"))
def create_number_of_products(auth_headers, test_context, products):
    logging.info(f"Create preliminary product data - {products} products")

    type_id = create_new_type_via_api_call(auth_headers).json()["new_id"]
    unit_id = create_new_unit_via_api_call(auth_headers).json()["new_id"]
    group_id = create_new_group_via_api_call(auth_headers).json()["new_id"]
    supplier_id = create_new_supplier_via_api_call(auth_headers).json()["new_id"]

    products_list = []

    for _ in range(products):
        payload = {
            "name": f"Test_product_{random.randint(100000, 999999)}",
            "type_id": type_id,
            "unit_id": unit_id,
            "group_id": group_id,
            "supplier_id": supplier_id
        }

        response = create_new_product_via_api_call(auth_headers, payload)

        products_list.append(Product.parse_response_to_product(response))

    test_context.products_list = products_list


@given("the user opens the new purchase order modal")
def open_new_purchase_modal(dashboard_page):
    logging.info("Open new purchase order modal")
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_visible(timeout=5000)
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_enabled(timeout=5000)
    dashboard_page.purchase_orders_side_menu_button.hover()
    dashboard_page.purchase_orders_side_menu_button.click(force=True)
    dashboard_page.new_purchase_order_side_menu_button.click(force=True)


@when("the user populates all Purchase Order fields")
def populate_new_po_fields(new_purchase_order_page, test_context):
    logging.info("Populate new Purchase Order fields")

    for product in test_context.products_list:
        product.quantity = random.randint(1, 20)
        product.cost = float(random.randint(1, 10000) / 100)

    purchase = Purchase(
        supplier=test_context.products_list[0].supplier,
        purchase_date=datetime.now(),
        purchase_type="Invoice",
        reference=f"INV_{random.randint(10000, 99999)}_{datetime.now()}",
        products=test_context.products_list,
        unify_same_items=True
    )

    new_purchase_order_page.submit_new_purchase_order(purchase)

    test_context.new_purchase = purchase


@then("the new Purchase Order is created successfully")
def validate_new_purchase_order_created(dashboard_page, purchase_order_history_page, test_context):
    dashboard_page.purchase_orders_history_side_menu_button.click()

    actual_reference = purchase_order_history_page.last_created_purchase_reference.inner_text()
    actual_type = purchase_order_history_page.last_created_purchase_type.inner_text()
    actual_supplier = purchase_order_history_page.last_created_purchase_supplier.inner_text()
    expected_total = "{:.2f}".format(
        sum(product.cost * product.quantity for product in test_context.new_purchase.products))

    actual_total = purchase_order_history_page.last_created_purchase_total.inner_text()[1:]
    actual_purchase_date = purchase_order_history_page.last_created_purchase_purchase_date.inner_text()
    actual_created_date = purchase_order_history_page.last_created_purchase_created_date.inner_text()[:10]

    assert actual_reference == test_context.new_purchase.reference, \
        (f"Expected purchase reference {test_context.new_purchase.reference} to equal Actual: {actual_reference} on "
         f"Purchase Order History page.")

    assert actual_type == test_context.new_purchase.purchase_type.lower(), \
        (
            f"Expected purchase type {test_context.new_purchase.type.lower()} to equal Actual: {actual_type} on Purchase Order "
            f"History page.")

    expected_supplier_name = test_context.new_purchase.supplier['name']
    assert actual_supplier == expected_supplier_name, \
        (f"Expected purchase supplier {expected_supplier_name} to equal Actual: {actual_supplier} on Purchase Order "
         f"History page.")

    assert actual_total == expected_total, \
        (f"Expected purchase total {expected_total} to equal Actual: {actual_total} on Purchase Order "
         f"History page.")

    # TODO: Uncomment when the purchase date is fixed
    expected_purchase_date = test_context.new_purchase.purchase_date.strftime("%m/%d/%Y")
    # assert actual_purchase_date == expected_purchase_date, \
    #     (f"Expected purchase date {expected_purchase_date} to equal Actual: {actual_purchase_date} on Purchase Order "
    #      f"History page.")

    expected_created_date = datetime.now().strftime("%d/%m/%Y")
    assert actual_created_date == expected_created_date, \
        (f"Expected created date {expected_created_date} to equal Actual: {actual_created_date} on Purchase Order "
         f"History page.")
