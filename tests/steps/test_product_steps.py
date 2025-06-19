import logging
import random

from pytest_bdd import given, scenarios, when, then, parsers

from modules.product import Product
from modules.product_group import ProductGroup
from modules.product_supplier import ProductSupplier
from modules.product_type import ProductType
from modules.product_unit import ProductUnit
from tests.conftest import ROOT_DIR

scenarios(ROOT_DIR / "tests" / "features" / "product.feature")


@given(parsers.re("the user wants to create New (?:Type|Unit|Group|Supplier|Product) from the New Product module"))
@given("user is on dashboard page")
def dummy_test_step_no_params():
    logging.info("Executing dummy test step no params.")


@given("there is an existing product type")
@when("the user submits the type form after filling correctly all required fields")
def submit_after_filling_the_new_product_type_form(test_context, product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()

    logging.info("Populate the New Type fields and Submit the Create Product Type form.")

    product_type = ProductType(
        name=f"Test Type ({random.randint(10000, 99999)})",
        description=f"Test Type Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_type(product_type)

    test_context.product_type = product_type


@given("there is an existing product unit")
@when("the user submits the unit form after filling correctly all required fields")
def submit_after_filling_the_new_product_unit_form(test_context, product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()

    logging.info("Populate the New Unit fields and Submit the Create Product Unit form.")

    product_unit = ProductUnit(
        name=f"Test Unit ({random.randint(10000, 99999)})",
        unit_yield=float(random.randint(1, 100)),
        description=f"Test Unit Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_unit(product_unit)

    test_context.product_unit = product_unit


@given("there is an existing product group")
@when("the user submits the group form after filling correctly all required fields")
def submit_after_filling_the_new_product_group_form(test_context, product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()

    logging.info("Populate the New Group fields and Submit the Create Product Group form.")

    product_group = ProductGroup(
        name=f"Test Group ({random.randint(10000, 99999)})",
        description=f"Test Group Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_group(product_group)

    test_context.product_group = product_group


@given("there is an existing product supplier")
@when("the user submits the supplier form after filling correctly all required fields")
def submit_after_filling_the_new_product_supplier_form(test_context, product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()

    logging.info("Populate the New Supplier fields and Submit the Create Product Supplier form.")

    product_supplier = ProductSupplier(
        name=f"Test Supplier ({random.randint(10000, 99999)})",
        email=f"test_supplier_{random.randint(10000, 99999)}@gmail.com"
    )

    product_page.create_new_supplier(product_supplier)

    test_context.product_supplier = product_supplier


@when("the user submits the product form after filling correctly all required fields")
def submit_after_filling_the_new_product_supplier_form(test_context, product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()

    logging.info("Populate the New Product fields and Submit the Create Product form.")

    product = Product(
        name=f"Test Product ({random.randint(10000, 99999)})",
        type=test_context.product_type.name,
        unit=test_context.product_unit.name,
        group=test_context.product_group.name,
        supplier=test_context.product_supplier.name,
    )

    product_page.create_new_product(product)

    test_context.product = product


@then("the new type has been created successfully")
def validate_new_product_type_exists_in_the_new_product_module(test_context, product_page):
    product_type = test_context.product_type
    logging.info(f"Validate the New Type {product_type.name} exists within the new product type dropdown values.")

    expected_success_message = "Product type created successfully!"
    actual_success_message = product_page.success_message.inner_text()

    assert actual_success_message == expected_success_message, \
        f"Expected {expected_success_message} message to be displayed, but got {actual_success_message}."

    product_page.new_product_side_menu_button.click()

    existing_product_types = product_page.return_values_from_select(product_page.PRODUCT_TYPE_DROPDOWN_SELECTOR)

    assert product_type.name in existing_product_types, (
        f"Expected product type '{product_type.name}' to be in the list of existing product types:\n {existing_product_types}.")


@then("the new unit has been created successfully")
def validate_new_product_unit_exists_in_the_new_product_module(test_context, product_page):
    product_unit = test_context.product_unit
    logging.info(f"Validate the New Unit {product_unit.name} exists within the new product unit dropdown values.")

    expected_success_message = "Product unit created successfully!"
    actual_success_message = product_page.success_message.inner_text()

    assert actual_success_message == expected_success_message, (
        f"Expected {expected_success_message} message to be displayed, but got {actual_success_message}.")

    product_page.new_product_side_menu_button.click()

    existing_product_units = product_page.return_values_from_select(product_page.PRODUCT_UNIT_DROPDOWN_SELECTOR)

    assert product_unit.name in existing_product_units, (
        f"Expected product unit '{product_unit.name}' to be in the list of existing product units:\n {existing_product_units}.")


@then("the new group has been created successfully")
def validate_new_product_group_exists_in_the_new_product_module(test_context, product_page):
    product_group = test_context.product_group
    logging.info(f"Validate the New Group {product_group.name} exists within the new product group dropdown values.")

    expected_success_message = "Product group created successfully!"
    actual_success_message = product_page.success_message.inner_text()

    assert actual_success_message == expected_success_message, (
        f"Expected {expected_success_message} message to be displayed, but got {actual_success_message}.")

    product_page.new_product_side_menu_button.click()

    existing_product_groups = product_page.return_values_from_select(product_page.PRODUCT_GROUP_DROPDOWN_SELECTOR)

    assert product_group.name in existing_product_groups, (
        f"Expected product group '{product_group.name}' to be in the list of existing product groups:\n {existing_product_groups}.")


@then("the new supplier has been created successfully")
def validate_new_product_supplier_exists_in_the_new_product_module(test_context, product_page):
    product_supplier = test_context.product_supplier
    logging.info(
        f"Validate the New Supplier {product_supplier.name} exists within the new product supplier dropdown values.")

    expected_success_message = "Supplier created successfully!"
    actual_success_message = product_page.success_message.inner_text()

    assert actual_success_message == expected_success_message, (
        f"Expected {expected_success_message} message to be displayed, but got {actual_success_message}.")

    product_page.new_product_side_menu_button.click()

    existing_product_suppliers = product_page.return_values_from_select(product_page.PRODUCT_SUPPLIER_DROPDOWN_SELECTOR)

    assert product_supplier.name in existing_product_suppliers, (
        f"Expected product supplier '{product_supplier.name}' to be in the list of existing product supplier:\n {existing_product_suppliers}.")


@then("the new product is created successfully")
def validate_new_product_is_created_successfully(test_context, product_page, dashboard_page, new_purchase_order_page):
    product = test_context.product
    logging.info(
        f"Validate the New Product {product.name} created successfully.")

    expected_success_message = "Product created successfully!"
    product_page.page.wait_for_timeout(500)
    actual_success_message = product_page.success_message.inner_text()

    assert actual_success_message == expected_success_message, (
        f"Expected {expected_success_message} message to be displayed, but got {actual_success_message}.")

    # Navigate to Create New Purchase module, in order to verify New Product exists.
    dashboard_page.navigate_to_new_purchase_order_from_dashboard()
    new_purchase_order_page.supplier_dropdown.select_option(product.supplier)
    existing_products = new_purchase_order_page.return_values_from_select(new_purchase_order_page.PRODUCT_DROPDOWN)

    assert product.name in existing_products, (
        f"Expected product '{product.name}' to be in the list of existing products:\n {existing_products}.")
