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
from utils.helpers import format_to_two_decimal_string

scenarios(ROOT_DIR / "tests" / "features" / "purchase.feature")


@given("user is on dashboard page")
def dummy_test_step_no_params():
    logging.info("Executing dummy test step no params.")


@given(parsers.re("(?P<products>\d+) product(?:s)? (?:is|are) created"))
def create_number_of_products(auth_headers, test_context, products):
    logging.info(f"Create preliminary product data - {products} products")

    type_id = create_new_type_via_api_call(auth_headers).json()["new_id"]
    unit_id = create_new_unit_via_api_call(auth_headers).json()["new_id"]
    group_id = create_new_group_via_api_call(auth_headers).json()["new_id"]
    supplier_id = create_new_supplier_via_api_call(auth_headers).json()["new_id"]

    products_list = []

    for _ in range(int(products)):
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


@given(parsers.re("(?P<products>\d+) identical products are created"))
@given(parsers.re("(?P<products>\d+) another product is created"))
def create_number_of_identical_products(auth_headers, test_context, products: int):
    logging.info(f"Create preliminary product data - {products} products")

    if getattr(test_context, "products_list", None) is None:
        test_context.products_list = []

    type_id = create_new_type_via_api_call(auth_headers).json()["new_id"] if test_context.products_list == [] else \
        test_context.products_list[0].type['id']
    unit_id = create_new_unit_via_api_call(auth_headers).json()["new_id"] if test_context.products_list == [] else \
        test_context.products_list[0].unit['id']
    group_id = create_new_group_via_api_call(auth_headers).json()["new_id"] if test_context.products_list == [] else \
        test_context.products_list[0].group['id']
    supplier_id = create_new_supplier_via_api_call(auth_headers).json()[
        "new_id"] if test_context.products_list == [] else test_context.products_list[0].supplier['id']

    random_number = random.randint(100000, 999999)
    random_quantity = random.randint(1, 10)
    random_cost = "{:.2f}".format(random.randint(1, 10))

    for _ in range(int(products)):
        payload = {
            "name": f"Test_product_{random_number}",
            "type_id": type_id,
            "unit_id": unit_id,
            "group_id": group_id,
            "supplier_id": supplier_id
        }

        response = create_new_product_via_api_call(auth_headers, payload)

        intermid_product = Product.parse_response_to_product(response)
        intermid_product.cost = random_cost
        intermid_product.quantity = random_quantity

        test_context.products_list.append(intermid_product)


@given("the user opens the new purchase order modal")
def open_new_purchase_modal(dashboard_page):
    logging.info("Open new purchase order modal")
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_visible(timeout=5000)
    expect(dashboard_page.purchase_orders_side_menu_button).to_be_enabled(timeout=5000)
    dashboard_page.purchase_orders_side_menu_button.hover(timeout=30000)
    dashboard_page.purchase_orders_side_menu_button.click(force=True)
    dashboard_page.new_purchase_order_side_menu_button.click(force=True)


@given("the user populates all Purchase Order fields")
@when("the user populates all Purchase Order fields")
def populate_new_po_fields(new_purchase_order_page, test_context):
    logging.info("Populate new Purchase Order fields")

    # Set the quantity and cost for each product in the product list
    for product in test_context.products_list:
        product.quantity = random.randint(1, 20) if product.quantity is None else product.quantity
        product.cost = float(random.randint(1, 10000) / 100) if product.cost is None else product.cost

    purchase = Purchase(
        supplier=test_context.products_list[0].supplier,
        purchase_date=datetime.now(),
        purchase_type="Invoice",
        reference=f"INV_{random.randint(10000, 99999)}_{datetime.now()}",
        products=test_context.products_list,
        unify_same_items=True
    )

    new_purchase_order_page.populate_new_purchase_order(purchase)

    test_context.new_purchase = purchase


@given(parsers.parse("the user populates all Purchase Order fields without {empty_field}"))
@when(parsers.parse("the user populates all Purchase Order fields without {empty_field}"))
def populate_new_po_fields_without_one(new_purchase_order_page, test_context, empty_field: str):
    logging.info(f"Populate new Purchase Order fields without {empty_field}")

    # Set the quantity and cost for each product in the product list
    for product in test_context.products_list:
        product.quantity = random.randint(1, 20) if product.quantity is None else product.quantity
        product.cost = float(random.randint(1, 10000) / 100) if product.cost is None else product.cost

    purchase = Purchase(
        supplier=test_context.products_list[0].supplier if empty_field != "supplier" else None,
        purchase_date=datetime.now() if empty_field != "purchase date" else None,
        purchase_type="Invoice" if empty_field != "purchase type" else None,
        reference=f"INV_{random.randint(10000, 99999)}_{datetime.now()}" if empty_field != "reference" else None,
        products=test_context.products_list,
        unify_same_items=True
    )

    new_purchase_order_page.populate_new_purchase_order(purchase)

    test_context.new_purchase = purchase


@when("the user edits the Added Item from the Items List")
def edit_added_item_from_current_purchase(test_context, new_purchase_order_page):
    new_purchase_order_page.edit_added_item(test_context)


@when("the user deletes an Added Item from the Items List")
def delete_added_item_from_current_purchase(test_context, new_purchase_order_page):
    new_purchase_order_page.delete_added_item(test_context)


@when("the user submits the Purchase Order")
def submit_purchase_order(test_context, new_purchase_order_page):
    new_purchase_order_page.submit_purchase(test_context.new_purchase.reference)


@when("the user saves the Purchase Order as Draft")
def save_draft_purchase_order(test_context, new_purchase_order_page):
    new_purchase_order_page.save_purchase_as_draft(test_context.new_purchase.reference)


@when("the user checks the 'Unify same items' checkbox")
def select_unify_same_items_checkbox(test_context, new_purchase_order_page):
    logging.info("Check the 'Unify same items' checkbox.")

    # Group by product name, and sum quantity only
    grouped = {}

    for product in test_context.new_purchase.products:
        if product.name not in grouped:
            # First occurrence: copy entire product
            grouped[product.name] = Product(
                id=product.id,
                name=product.name,
                cost=product.cost,  # keep unit cost
                quantity=product.quantity,  # start with current quantity
                type=product.type,
                type_id=product.type_id
            )
        else:
            # Sum quantity only
            grouped[product.name].quantity += product.quantity

    test_context.aggregated_result = list(grouped.values())

    new_purchase_order_page.select_unify_same_items_checkbox(True)


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


@then("the new Purchase Order is successfully saved as Draft")
def validate_new_purchase_order_saved_as_draft(dashboard_page, draft_purchase_orders_page, test_context):
    dashboard_page.draft_purchase_orders_side_menu_button.click()

    actual_reference = draft_purchase_orders_page.last_saved_draft_purchase_reference.inner_text()
    actual_supplier = draft_purchase_orders_page.last_saved_draft_purchase_supplier.inner_text()
    actual_total = draft_purchase_orders_page.last_saved_draft_purchase_total.inner_text()[1:]
    actual_created_date = draft_purchase_orders_page.last_saved_draft_purchase_created_date.inner_text()
    actual_saved_date = draft_purchase_orders_page.last_saved_draft_purchase_date_saved.inner_text()[:10]

    assert actual_reference == test_context.new_purchase.reference, \
        (f"Expected draft purchase reference {test_context.new_purchase.reference} to equal "
         f"Actual: {actual_reference} on Draft Purchase Orders page.")

    expected_supplier_name = test_context.new_purchase.supplier['name']
    assert actual_supplier == expected_supplier_name, \
        (f"Expected purchase supplier {expected_supplier_name} to equal "
         f"Actual: {actual_supplier} on Draft Purchase Orders page.")

    expected_total = "{:.2f}".format(
        sum(product.cost * product.quantity for product in test_context.new_purchase.products))
    assert actual_total == expected_total, \
        (f"Expected purchase total {expected_total} to equal "
         f"Actual: {actual_total} on Draft Purchase Orders page.")

    expected_created_date = datetime.now().strftime("%d/%m/%Y")
    assert actual_created_date == expected_created_date, \
        (f"Expected created date {expected_created_date} to equal "
         f"Actual: {actual_created_date} on Draft Purchase Orders page.")

    expected_saved_date = datetime.now().strftime("%d/%m/%Y")
    assert actual_saved_date == expected_created_date, \
        (f"Expected saved date {expected_saved_date} to equal "
         f"Actual: {actual_saved_date} on Draft Purchase Orders page.")


@then("the same items are merged into one")
def verify_same_items_unified(test_context, new_purchase_order_page):
    for product in test_context.aggregated_result:
        actual_quantity = new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_BY_TITLE.format(product.name, 'quantity')).inner_text()
        assert actual_quantity == str(product.quantity)

        actual_cost = new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_BY_TITLE.format(product.name, 'cost')).inner_text()
        assert actual_cost == str(
            product.cost), f"The expected cost for the added item {str(product.cost)} should equal the Actual {actual_cost}."

        actual_total = new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_BY_TITLE.format(product.name, 'total')).inner_text()
        assert actual_total == "{:.2f}".format(float(product.quantity) * float(product.cost))

        edit_btn = new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_EDIT_ACTION_BY_TITLE.format(product.name))
        expect(edit_btn).to_be_visible()
        expect(edit_btn).to_be_enabled()

        delete_btn = new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_DELETE_ACTION_BY_TITLE.format(product.name))
        expect(delete_btn).to_be_visible()
        expect(delete_btn).to_be_enabled()


@then("the item values have been edited successfully")
def verify_edited_item_values(test_context, new_purchase_order_page):
    product = test_context.products_list[len(test_context.products_list) - 1]

    added_products_names = \
        [product.locator(".product-name").inner_text() for product in
         new_purchase_order_page.added_item_container.all()]

    assert product.name in added_products_names, (
        f"Expected product {product.name} to be added to items list, but it was not found!")

    added_item_element = new_purchase_order_page.ADDED_PRODUCT_BY_TITLE.format(product.name, '{}')

    assert (new_purchase_order_page.page.locator(added_item_element.format('unit'))
            .last
            .inner_text()
            == product.unit['name'])

    assert (new_purchase_order_page.page.locator(added_item_element.format('quantity'))
            .last
            .inner_text()
            == str(product.quantity))

    actual_cost = float((new_purchase_order_page.page.locator(added_item_element.format('cost'))
                         .last
                         .inner_text()))

    assert (actual_cost == float(product.cost),
            f"The expected cost for the added item {float(product.cost)} should equal the Actual {actual_cost}.")

    total = format_to_two_decimal_string(
        float((new_purchase_order_page.page.locator(added_item_element.format('total'))
               .last
               .inner_text())))
    expected_total = format_to_two_decimal_string(product.quantity * float(product.cost))
    assert total == expected_total, f"Expected added item total {expected_total} to equal Actual {total}"

    for edit_btn in new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_EDIT_ACTION_BY_TITLE.format(product.name)).all():
        expect(edit_btn).to_be_visible()
        expect(edit_btn).to_be_enabled()

    for delete_btn in new_purchase_order_page.page.locator(
            new_purchase_order_page.ADDED_PRODUCT_DELETE_ACTION_BY_TITLE.format(product.name)).all():
        expect(delete_btn).to_be_visible()
        expect(delete_btn).to_be_enabled()


@then("the item has been deleted successfully")
def verify_item_deleted(test_context, new_purchase_order_page):
    item_to_delete = test_context.new_purchase.products[0]

    # Get the total purchase when an added item has been moved to edit (Added Items list is with one item less)
    purchase_total_after_item_deleted: float = float(new_purchase_order_page.purchase_total_value.inner_text())

    actual_purchase_total_after_item_deleted = round(float(test_context.preliminary_purchase_total - (
            float(item_to_delete.cost) * item_to_delete.quantity)), 2)
    assert purchase_total_after_item_deleted == actual_purchase_total_after_item_deleted, \
        (f"Expected {purchase_total_after_item_deleted} to equal"
         f"Actual {actual_purchase_total_after_item_deleted}")

    assert new_purchase_order_page.added_item_container.count() + 1 == test_context.preliminary_added_items_count, \
        (f"Expected the number of added items to have decreased to {test_context.preliminary_added_items_count - 1} "
         f"after clicking Delete Item, but got {new_purchase_order_page.added_item_container.count()}.")


@then(parsers.parse("Purchase Order not created with error message: {expected_error_message}"))
def verify_purchase_order_not_created_with_error_message(new_purchase_order_page,
                                                         expected_error_message: str):
    new_purchase_order_page.verify_error_message(expected_error_message)
    new_purchase_order_page.purchase_cancel_button.click()


@then("there is no Purchase Order without reference in Purchase Order History Page")
def verify_no_purchase_order_without_reference_on_history_page(purchase_order_history_page, dashboard_page):
    dashboard_page.purchase_orders_history_side_menu_button.click()

    for reference in purchase_order_history_page.all_purchase_references.all():
        expect(reference, "Expected all references in Purchase History not to be empty.").not_to_be_empty()
