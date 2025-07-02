import logging

from playwright.sync_api import Page

from modules.product import Product
from modules.product_group import ProductGroup
from modules.product_supplier import ProductSupplier
from modules.product_type import ProductType
from modules.product_unit import ProductUnit
from pages.dashboard_page import DashboardPage


class ProductPage(DashboardPage):
    PRODUCT_TYPE_DROPDOWN_SELECTOR = "#productType"
    PRODUCT_UNIT_DROPDOWN_SELECTOR = "#productUnit"
    PRODUCT_GROUP_DROPDOWN_SELECTOR = "#productGroup"
    PRODUCT_SUPPLIER_DROPDOWN_SELECTOR = "#productSupplier"

    def __init__(self, page: Page):
        super().__init__(page)
        self.add_new_type_button = page.locator("//select[@id='productType']/following-sibling::button[text()='+ New']")
        self.add_new_unit_button = page.locator("//select[@id='productUnit']/following-sibling::button[text()='+ New']")
        self.add_new_group_button = page.locator(
            "//select[@id='productGroup']/following-sibling::button[text()='+ New']")
        self.add_new_supplier_button = page.locator(
            "//select[@id='productSupplier']/following-sibling::button[text()='+ New']")
        self.new_type_name_input = page.locator("#newTypeName")
        self.new_unit_name_input = page.locator("#newUnitName")
        self.new_group_name_input = page.locator("#newGroupName")
        self.new_supplier_name_input = page.locator("#newSupplierName")
        self.new_unit_yield_input = page.locator("#newUnitYield")
        self.new_supplier_email_input = page.locator("#newSupplierEmail")
        self.new_type_description_input = page.locator("#newTypeDescription")
        self.new_unit_description_input = page.locator("#newUnitDescription")
        self.new_group_description_input = page.locator("#newGroupDescription")
        self.create_type_button = page.locator("#createTypeBtn")
        self.create_unit_button = page.locator("#createUnitBtn")
        self.create_group_button = page.locator("#createGroupBtn")
        self.create_supplier_button = page.locator("#createSupplierBtn")
        self.create_product_button = page.locator("#createProductBtn")
        self.product_name_input = page.locator("#productName")
        self.product_type_dropdown = page.locator(self.PRODUCT_TYPE_DROPDOWN_SELECTOR)
        self.product_unit_dropdown = page.locator(self.PRODUCT_UNIT_DROPDOWN_SELECTOR)
        self.product_group_dropdown = page.locator(self.PRODUCT_GROUP_DROPDOWN_SELECTOR)
        self.product_supplier_dropdown = page.locator(self.PRODUCT_SUPPLIER_DROPDOWN_SELECTOR)
        self.new_product_close_button = page.locator("//div[@id='newProductModal']//span[text()='×']")

    def create_new_type(self, product_type: ProductType):
        """
        The method is used to create new Product Type, by clicking on +New type button
        from the New Product module, filling the respective fields and clicking 'Create Type' button.

        :param product_type: the Product Type dataclass providing the respective data.
        """

        logging.info("Create new Type from New Product Module -> New Type Sub-Module.")
        self.add_new_type_button.click()
        self.new_type_name_input.fill(product_type.name)
        self.new_type_description_input.fill(product_type.description)
        self.create_type_button.click()
        self.new_product_close_button.click()

    def create_new_unit(self, product_unit: ProductUnit):
        """
        The method is used to create new Product Unit, by clicking on +New unit button
        from the New Product module, filling the respective fields and clicking 'Create Unit' button.

        :param product_unit: the Product Unit dataclass providing the respective data.
        """

        logging.info("Create new Unit from New Product Module -> New Unit Sub-Module.")
        self.add_new_unit_button.click()
        self.new_unit_name_input.fill(product_unit.name)
        self.new_unit_yield_input.fill(str(product_unit.unit_yield))
        self.new_unit_description_input.fill(product_unit.description)
        self.create_unit_button.click()
        self.new_product_close_button.click()

    def create_new_group(self, product_group: ProductGroup):
        """
        The method is used to create new Product Group, by clicking on +New group button
        from the New Product module, filling the respective fields and clicking 'Create Group' button.

        :param product_group: the Product Group dataclass providing the respective data.
        """

        logging.info("Create new Group from New Product Module -> New Group Sub-Module.")
        self.add_new_group_button.click()
        self.new_group_name_input.fill(product_group.name)
        self.new_group_description_input.fill(product_group.description)
        self.create_group_button.click()
        self.new_product_close_button.click()


    def create_new_supplier(self, product_supplier: ProductSupplier):
        """
        The method is used to create new Product Supplier, by clicking on +New supplier button
        from the New Product module, filling the respective fields and clicking 'Create Supplier' button.

        :param product_supplier: the Product Supplier dataclass providing the respective data.
        """

        logging.info("Create new Supplier from New Product Module -> New Supplier Sub-Module.")
        self.add_new_supplier_button.click()
        self.new_supplier_name_input.fill(product_supplier.name)
        self.new_supplier_email_input.fill(product_supplier.email)
        self.create_supplier_button.click()
        self.new_product_close_button.click()


    def create_new_product(self, product: Product):
        """
        The method is used to create new Product, by clicking on the New Product module,
        filling the respective fields and clicking 'Create Product' button.

        :param product: the Product dataclass providing the respective data.
        """

        logging.info("Create new Product from New Product Module.")
        self.product_name_input.fill(product.name)
        self.product_type_dropdown.select_option(product.type)
        self.product_unit_dropdown.select_option(product.unit)
        self.product_group_dropdown.select_option(product.group)
        self.product_supplier_dropdown.select_option(product.supplier)
        self.create_product_button.click()
