import logging
import random
from datetime import datetime

from playwright.sync_api import Page, expect

from modules.product import Product
from modules.purchase import Purchase
from pages.base_page import BasePage
from utils.helpers import format_to_two_decimal_string


class NewPurchaseOrderPage(BasePage):
    PRODUCT_DROPDOWN = "#currentProduct"
    UNIT_DROPDOWN = "#currentUnit"
    ADDED_PRODUCT_BY_TITLE = "//strong[@class='product-name' and text()='{}']/following-sibling::*[@class='{}']"
    ADDED_PRODUCT_ACTIONS_BY_TITLE = "//strong[@class='product-name' and text()='{}']/../following-sibling::div[@class='item-actions']//button[@class='inline-button edit-btn']"
    ADDED_PRODUCT_EDIT_ACTION_BY_TITLE = "//strong[@class='product-name' and text()='{}']/../following-sibling::div[@class='item-actions']//button[@class='inline-button edit-btn']"
    ADDED_PRODUCT_DELETE_ACTION_BY_TITLE = "//strong[@class='product-name' and text()='{}']/../following-sibling::div[@class='item-actions']//button[@class='inline-button delete-btn']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.supplier_dropdown = page.locator("#purchaseSupplier")
        self.purchase_date_field = page.locator("#purchaseDate")
        self.purchase_type_dropdown = page.locator("#purchaseType")
        self.purchase_reference_input = page.locator("#purchaseReference")
        self.product_dropdown = page.locator(self.PRODUCT_DROPDOWN)
        self.product_unit_dropdown = page.locator(self.UNIT_DROPDOWN)
        self.product_quantity_input = page.locator("#currentQuantity")
        self.product_cost_input = page.locator("#currentCost")
        self.product_total_field = page.locator("#currentTotal")
        self.purchase_add_item_button = page.locator("#addItemToListBtn")
        self.purchase_submit_button = page.locator("#createPurchaseBtn")
        self.purchase_save_as_draft_button = page.locator("#saveDraftBtn")
        self.purchase_cancel_button = page.locator("#cancelPurchaseBtn")
        self.unify_items_checkbox = page.locator("#unifyItemsCheckbox")
        self.items_list_container = page.locator("#purchaseItemsList")
        self.purchase_total_value = page.locator("#purchaseTotal")
        self.added_item_container = page.locator(".added-item")

    def select_supplier(self, supplier_name: str):
        self.supplier_dropdown.select_option(supplier_name)
        return self

    def type_purchase_date(self, purchase_date: str):
        self.purchase_date_field.type(purchase_date)
        return self

    def select_purchase_type(self, purchase_type: str):
        self.purchase_type_dropdown.select_option(purchase_type)
        return self

    def fill_purchase_reference(self, reference: str):
        self.purchase_reference_input.fill(reference)
        return self

    def select_product(self, product_name: str):
        self.product_dropdown.select_option(product_name)
        return self

    def select_unit(self, product_unit: str):
        self.product_unit_dropdown.select_option(product_unit)
        return self

    def fill_quantity(self, quantity: int):
        self.product_quantity_input.fill(str(quantity))
        return self

    def fill_cost(self, cost: float):
        self.product_cost_input.fill(str(cost))
        return self

    def add_item(self, product: Product):
        logging.info(f"Add item {product.name} to purchase.")

        self.purchase_add_item_button.click()

        # Assert item is added to Items List
        added_products_names = \
            [product.locator(".product-name").inner_text() for product in self.added_item_container.all()]

        assert product.name in added_products_names, (
            f"Expected product {product.name} to be added to items list, but it was not found!")

        for unit in self.page.locator(self.ADDED_PRODUCT_BY_TITLE.format(product.name, 'unit')).all():
            assert unit.inner_text() == product.unit['name']

        for quantity in self.page.locator(self.ADDED_PRODUCT_BY_TITLE.format(product.name, 'quantity')).all():
            assert quantity.inner_text() == str(product.quantity)

        actual_cost = (float(set([cost.inner_text() for cost in
                                  self.page.locator(
                                      self.ADDED_PRODUCT_BY_TITLE.format(product.name, 'cost')).all()]).pop()))

        assert actual_cost == float(product.cost), \
            f"The expected cost for the added item {float(product.cost)} should equal the Actual {actual_cost}."

        for total in self.page.locator(self.ADDED_PRODUCT_BY_TITLE.format(product.name, 'total')).all():
            assert format_to_two_decimal_string(total.inner_text()) == format_to_two_decimal_string(
                product.quantity * float(product.cost)), \
                (f"Expected added item total {(product.quantity * float(product.cost))} to equal "
                 f"Actual {float(total.inner_text())}")

        for edit_btn in self.page.locator(self.ADDED_PRODUCT_EDIT_ACTION_BY_TITLE.format(product.name)).all():
            expect(edit_btn).to_be_visible()
            expect(edit_btn).to_be_enabled()

        for delete_btn in self.page.locator(self.ADDED_PRODUCT_DELETE_ACTION_BY_TITLE.format(product.name)).all():
            expect(delete_btn).to_be_visible()
            expect(delete_btn).to_be_enabled()

        # Assert item details are cleared from Product inputs:
        expect(self.supplier_dropdown).not_to_be_enabled()
        expect(self.product_dropdown.locator("option:checked")).to_have_text("Select product")
        expect(self.product_unit_dropdown).not_to_be_enabled()
        expect(self.product_quantity_input).to_be_enabled()
        expect(self.product_quantity_input).to_be_empty()
        expect(self.product_cost_input).to_be_enabled()
        expect(self.product_cost_input).to_be_empty()
        expect(self.product_total_field).to_be_enabled()
        expect(self.product_total_field).to_be_empty()

        return self

    def add_edited_item(self, product: Product):
        logging.info(f"Add edited item {product.name} to purchase.")

        self.purchase_add_item_button.click()

        # Assert item details are cleared from Product inputs:
        expect(self.supplier_dropdown).not_to_be_enabled()
        expect(self.product_dropdown.locator("option:checked")).to_have_text("Select product")
        expect(self.product_unit_dropdown).not_to_be_enabled()
        expect(self.product_quantity_input).to_be_enabled()
        expect(self.product_quantity_input).to_be_empty()
        expect(self.product_cost_input).to_be_enabled()
        expect(self.product_cost_input).to_be_empty()
        expect(self.product_total_field).to_be_enabled()
        expect(self.product_total_field).to_be_empty()

        return self

    def submit_purchase(self, reference: str):
        logging.info(f"Submit purchase with reference '{reference}' as New Purchase Order.")

        self.purchase_submit_button.click()
        return self

    def save_purchase_as_draft(self, reference: str):
        logging.info(f"Save purchase with reference '{reference}' as Draft Purchase Order.")

        self.purchase_save_as_draft_button.click()
        return self

    def cancel_purchase_create(self, reference: str):
        logging.info(f"Cancel create of purchase with reference '{reference}'.")

        self.purchase_cancel_button.click()
        return self

    def edit_added_item(self, test_context):
        item_to_edit = test_context.new_purchase.products[0]
        update_item = test_context.new_purchase.products[1]

        logging.info(f"Edit the first existing in Items List added item with title {item_to_edit.name}.")

        # Get the total purchase before moving added item to edit
        preliminary_purchase_total = float(self.purchase_total_value.inner_text())

        preliminary_added_items_count: int = self.added_item_container.count()

        # Click on Edit Button for the first item in the list of added items
        self.page.locator(self.ADDED_PRODUCT_EDIT_ACTION_BY_TITLE.format(item_to_edit.name)).click()

        # Get the total purchase when an added item has been moved to edit (Added Items list is with one item less)
        purchase_total_after_item_moved_to_edit: float = float(self.purchase_total_value.inner_text())

        actual_purchase_total_after_item_moved_to_edit = round(float(preliminary_purchase_total - (
                float(item_to_edit.cost) * item_to_edit.quantity)), 2)
        assert purchase_total_after_item_moved_to_edit == actual_purchase_total_after_item_moved_to_edit, \
            (f"Expected {purchase_total_after_item_moved_to_edit} to equal"
             f"Actual {actual_purchase_total_after_item_moved_to_edit}")

        assert self.added_item_container.count() + 1 == preliminary_added_items_count, \
            (f"Expected the number of added items to have decreased to {preliminary_added_items_count - 1} "
             f"after clicking Edit Item, but got {self.added_item_container.count()}.")

        expect(self.supplier_dropdown).to_be_enabled() \
            if self.added_item_container.count() == 0 \
            else expect(self.supplier_dropdown).not_to_be_enabled()
        expect(self.product_dropdown.locator("option:checked")).to_have_text(item_to_edit.name)
        expect(self.product_unit_dropdown.locator("option:checked")).to_have_text(item_to_edit.unit['name'])
        assert int(self.product_quantity_input.input_value()) == item_to_edit.quantity
        assert float(self.product_cost_input.input_value()) == float(item_to_edit.cost)
        assert (float(self.product_total_field.input_value()) ==
                round((float(item_to_edit.cost) * item_to_edit.quantity), 2))

        # Update the value for the edited item
        updated_product = Product(
            name=update_item.name,
            unit=update_item.unit,
            quantity=random.randint(1, 6),
            cost=float(random.randint(1, 100))
        )

        self.fill_edit_purchase_product_details(updated_product)

        self.add_edited_item(updated_product)

        expected_total_purchase_order_amount: float = round(
            purchase_total_after_item_moved_to_edit + (updated_product.quantity * float(updated_product.cost)), 2)

        assert float(format_to_two_decimal_string(
            self.purchase_total_value.inner_text())) == expected_total_purchase_order_amount, \
            (f"Expected total Purchase Amount {expected_total_purchase_order_amount} to equal "
             f"Actual: {float(self.purchase_total_value.inner_text())}.")

        test_context.new_purchase.products.append(updated_product)

    def populate_new_purchase_order(self, purchase: Purchase):
        """
        The method is used to populate all provided data from a Purchase object into the New Purchase Order form.
        After populating all provided data into the respective fields, the Purchase Order is submitted.

        :param purchase: the Purchase object providing the data that will be populated.
        """

        expect(self.purchase_date_field).to_be_enabled()
        expect(self.purchase_date_field).to_have_value(datetime.now().strftime("%Y-%m-%d"))
        expect(self.purchase_type_dropdown).to_be_enabled()
        expect(self.purchase_type_dropdown).to_have_value("invoice")
        expect(self.purchase_reference_input).to_be_enabled()
        expect(self.purchase_reference_input).to_be_empty()
        expect(self.product_dropdown).not_to_be_enabled()
        expect(self.product_unit_dropdown).to_be_enabled()
        assert len(self.return_values_from_select(self.UNIT_DROPDOWN)) == 1
        expect(self.product_quantity_input).to_be_enabled()
        expect(self.product_quantity_input).to_be_empty()
        expect(self.product_quantity_input).to_be_enabled()
        expect(self.product_cost_input).to_be_empty()
        expect(self.product_cost_input).to_be_enabled()
        expect(self.product_total_field).to_be_empty()
        expect(self.product_total_field).to_be_enabled()
        expect(self.purchase_add_item_button).to_be_enabled()
        expect(self.purchase_submit_button).to_be_enabled()
        expect(self.purchase_save_as_draft_button).to_be_enabled()
        expect(self.purchase_cancel_button).to_be_enabled()
        expect(self.unify_items_checkbox).to_be_enabled()
        expect(self.unify_items_checkbox).not_to_be_checked()
        expect(self.items_list_container).to_be_empty()
        expect(self.purchase_total_value).to_have_text("0.00")

        # Start populating new Purchase Order fields
        if purchase.supplier['name'] is not None:
            self.select_supplier(purchase.supplier['name'])
            expect(self.supplier_dropdown).to_be_enabled()
            expect(self.product_dropdown).to_be_enabled()
            expect(self.product_unit_dropdown).not_to_be_enabled()

        if purchase.purchase_date is not None:
            self.type_purchase_date(purchase.purchase_date.strftime("%d%m%Y"))

        if purchase.purchase_type is not None:
            self.select_purchase_type(purchase.purchase_type)

        if purchase.reference is not None:
            self.fill_purchase_reference(purchase.reference)

        total_purchase_order_amount = 0

        for product in purchase.products:
            self.fill_purchase_product_details(product)
            self.add_item(product)
            total_purchase_order_amount = total_purchase_order_amount + (float(product.quantity) * float(product.cost))

        assert self.purchase_total_value.inner_text() == "{:.2f}".format(total_purchase_order_amount), \
            f"Expected total Purchase Amount {":.2f".format(total_purchase_order_amount)} to equal Actual: {self.purchase_total_value.inner_text()}."

    def fill_purchase_product_details(self, product: Product):
        """
        The method is used to populate the provided data for a Product from a Product object into the Purchase Order
        form.

        :param product: the product object providing the data.
        """
        if product.name is not None:
            expect(self.product_unit_dropdown).not_to_be_enabled()
            self.select_product(product.name)
            expect(self.product_total_field).to_have_value("0.00")
            expect(self.product_unit_dropdown).to_be_enabled()

        if product.unit is not None:
            self.select_unit(product.unit['name'])
        if product.quantity is not None:
            self.fill_quantity(product.quantity)
        if product.cost is not None:
            self.fill_cost(product.cost)
            assert self.product_total_field.input_value() == "{:.2f}".format(
                float(product.quantity) * float(product.cost)), \
                f"Expected product total {"{:.2f}".format(float(product.quantity) * float(product.cost))} to equal Actual: {self.product_total_field.input_value()}."

    def fill_edit_purchase_product_details(self, product: Product):
        """
        The method is used to populate by editing the provided data for a Product
        from a Product object into the Purchase Order form.

        :param product: the product object providing the data.
        """
        expect(self.product_unit_dropdown).to_be_enabled()
        self.select_product(product.name)

        if product.unit is not None:
            self.select_unit(product.unit['name'])
        if product.quantity is not None:
            self.fill_quantity(product.quantity)
        if product.cost is not None:
            self.fill_cost(product.cost)

            expected_item_total = format_to_two_decimal_string(product.quantity * float(product.cost))
            assert self.product_total_field.input_value() == expected_item_total, \
                (f"Expected product total {expected_item_total} to equal "
                 f"Actual: {self.product_total_field.input_value()}.")

    def select_unify_same_items_checkbox(self, is_checked):
        """
        Checks the current state of the 'Unify same items' checkbox and updates it if necessary.

        :param is_checked: Desired state of the 'Unify same items' checkbox (True for checked, False for unchecked).
        """

        expect(self.unify_items_checkbox).to_be_enabled()
        if self.unify_items_checkbox.is_checked() != is_checked:
            self.unify_items_checkbox.check()
