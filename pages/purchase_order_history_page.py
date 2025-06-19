from playwright.sync_api import Page

from pages.base_page import BasePage


class PurchaseOrderHistoryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.last_created_purchase_order_row = page.locator("//tbody/tr[1]")
        self.last_created_purchase_reference = self.last_created_purchase_order_row.locator("xpath=./td[1]")
        self.last_created_purchase_type = self.last_created_purchase_order_row.locator("xpath=./td[2]")
        self.last_created_purchase_supplier = self.last_created_purchase_order_row.locator("xpath=./td[3]")
        self.last_created_purchase_total = self.last_created_purchase_order_row.locator("xpath=./td[4]")
        self.last_created_purchase_purchase_date = self.last_created_purchase_order_row.locator("xpath=./td[5]")
        self.last_created_purchase_created_date = self.last_created_purchase_order_row.locator("xpath=./td[6]")
