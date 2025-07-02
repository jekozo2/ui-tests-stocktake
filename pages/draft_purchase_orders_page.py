from playwright.sync_api import Page

from pages.base_page import BasePage


class DraftPurchaseOrdersPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.last_saved_draft_purchase_order_row = page.locator("//tbody/tr").last
        self.last_saved_draft_purchase_reference = self.last_saved_draft_purchase_order_row.locator("xpath=./td[1]")
        self.last_saved_draft_purchase_supplier = self.last_saved_draft_purchase_order_row.locator("xpath=./td[2]")
        self.last_saved_draft_purchase_created_date = self.last_saved_draft_purchase_order_row.locator("xpath=./td[3]")
        self.last_saved_draft_purchase_total = self.last_saved_draft_purchase_order_row.locator("xpath=./td[4]")
        self.last_saved_draft_purchase_date_saved = self.last_saved_draft_purchase_order_row.locator("xpath=./td[5]")
