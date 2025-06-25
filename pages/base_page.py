from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.error_message = page.locator("//div[@class='error-message']")

    def return_values_from_select(self, selector: str):
        """
        The method is used to retrieve all values from select element.

        :param selector: the select element
        :return: list of all values from the select
        """
        values = self.page.query_selector(selector).query_selector_all("option")

        values_text = []

        for value in values:
            if value.text_content() != "":
                values_text.append(value.text_content().strip())
        return values_text

    def verify_error_message(self, expected_message):
        (expect(self.error_message,
                f"Expect error message '{expected_message}' to equal Actual {self.error_message.inner_text()}")
         .to_contain_text(expected_message))
