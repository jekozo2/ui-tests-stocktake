from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page):
        self.page = page

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
