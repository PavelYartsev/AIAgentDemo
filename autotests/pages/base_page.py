import logging
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def fill_field(self, selector, value):
        self.logger.info(f"Filling field {selector} with value {value}")
        self.page.fill(selector, value)

    def click(self, selector):
        self.logger.info(f"Clicking on element {selector}")
        self.page.click(selector)

    def select_option(self, selector, option):
        self.logger.info(f"Selecting option {option} from {selector}")
        self.page.select_option(selector, option)

    def check_element_text(self, selector, expected_text):
        self.logger.info(f"Checking if element {selector} contains text {expected_text}")
        element = self.page.locator(selector)
        assert expected_text in element.text_content(), f"Expected text '{expected_text}' not found in {selector}"