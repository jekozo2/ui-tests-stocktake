import logging

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DashboardPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.toggle_side_menu_button = page.locator(".sidebar-toggle")
        self.stocktake_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='Stocktake']")
        self.new_product_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='New Product']")
        self.transfers_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='Transfers']")
        self.requests_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='Requests']")
        self.purchase_orders_side_menu_button = page.locator("#purchaseOrdersBtn")
        self.new_purchase_order_side_menu_button = page.locator(
            "//div[@id='purchaseSubmenu']//span[text()='New Purchase Order']")
        self.draft_purchase_orders_side_menu_button = page.locator(
            "//div[@id='purchaseSubmenu']//span[text()='Draft Purchase Orders']")
        self.purchase_orders_history_side_menu_button = page.locator(
            "//div[@id='purchaseSubmenu']//span[text()='Purchase Orders History']")
        self.stores_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='Stores']")
        self.logout_side_menu_button = page.locator("//div[@class='sidebar-menu']//span[text()='Logout']")
        self.success_message = page.locator(".success-message")
        self.new_purchase_order_module_header_text = page.locator("#newPurchaseHeaderText")

    def navigate_to_new_purchase_order_from_dashboard(self):
        logging.info("Navigate to New Purchase Order from Dashboard.")

        self.purchase_orders_side_menu_button.click()
        self.new_purchase_order_side_menu_button.click()
        expect(self.new_purchase_order_module_header_text).to_be_visible(timeout=10000)
