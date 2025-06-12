import logging
import random

from pytest_bdd import given, scenarios, when, then, parsers

from modules.product_group import ProductGroup
from modules.product_supplier import ProductSupplier
from modules.product_type import ProductType
from modules.product_unit import ProductUnit
from tests.conftest import ROOT_DIR

scenarios(ROOT_DIR / "tests" / "features" / "product.feature")


@given("user is on dashboard page")
def dummy_test_step_no_params():
    logging.info("Executing dummy test step no params.")


@given(parsers.re("the user navigates to create New (?:Type|Unit|Group|Supplier) from the New Product module"))
def navigate_to_submodule_from_product_module(product_page):
    logging.info("Navigate to submodule from the Product Module from the Dashboard.")
    product_page.new_product_side_menu_button.click()


@when("the user submits the type form after filling correctly all required fields", target_fixture="product_type")
def submit_after_filling_the_new_product_type_form(product_page):
    logging.info("Populate the New Type fields and Submit the Create Product Type form.")

    product_type = ProductType(
        name=f"Test Type ({random.randint(10000, 99999)})",
        description=f"Test Type Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_type(product_type)

    return product_type


@when("the user submits the unit form after filling correctly all required fields", target_fixture="product_unit")
def submit_after_filling_the_new_product_unit_form(product_page):
    logging.info("Populate the New Unit fields and Submit the Create Product Unit form.")

    product_unit = ProductUnit(
        name=f"Test Unit ({random.randint(10000, 99999)})",
        unit_yield=float(random.randint(1, 100)),
        description=f"Test Unit Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_unit(product_unit)

    return product_unit


@when("the user submits the group form after filling correctly all required fields", target_fixture="product_group")
def submit_after_filling_the_new_product_group_form(product_page):
    logging.info("Populate the New Group fields and Submit the Create Product Group form.")

    product_group = ProductGroup(
        name=f"Test Group ({random.randint(10000, 99999)})",
        description=f"Test Group Description ({random.randint(10000, 99999)})"
    )

    product_page.create_new_group(product_group)

    return product_group


@when("the user submits the supplier form after filling correctly all required fields",
      target_fixture="product_supplier")
def submit_after_filling_the_new_product_supplier_form(product_page):
    logging.info("Populate the New Supplier fields and Submit the Create Product Supplier form.")

    product_supplier = ProductSupplier(
        name=f"Test Supplier ({random.randint(10000, 99999)})",
        email=f"test_supplier_{random.randint(10000, 99999)}@gmail.com"
    )

    product_page.create_new_supplier(product_supplier)

    return product_supplier


@then("the new type has been created successfully")
def validate_new_product_type_exists_in_the_new_product_module(product_page, product_type):
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
def validate_new_product_unit_exists_in_the_new_product_module(product_page, product_unit):
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
def validate_new_product_group_exists_in_the_new_product_module(product_page, product_group):
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
def validate_new_product_supplier_exists_in_the_new_product_module(product_page, product_supplier):
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
