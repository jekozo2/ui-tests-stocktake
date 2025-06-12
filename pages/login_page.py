import logging

from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.locator("#email")
        self.password_field = page.locator("#password")
        self.submit_button = page.locator("//button[@type='submit' and text()='Login']")
        self.content_user_email = page.locator("#userEmail")
        self.login_error_message = page.locator("#error")

    def populate_email_field_with(self, email: str):
        logging.info(f"Fill login email field with {email}")
        self.email_field.fill(email)
        return self

    def populate_password_field_with(self, password: str):
        logging.info(f"Fill login password field with {password}")
        self.password_field.fill(password)
        return self

    def submit_login_credentials(self):
        logging.info("Submit login credentials")
        self.submit_button.click()
        return self
