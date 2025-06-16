from playwright.sync_api import Page

from pages.base_page import BasePage


class NewPurchaseOrderPage(BasePage):

    PRODUCT_DROPDOWN = "#currentProduct"

    def __init__(self, page: Page):
        super().__init__(page)
        self.supplier_dropdown = page.locator("#purchaseSupplier")
        self.product_dropdown = page.locator(self.PRODUCT_DROPDOWN)
