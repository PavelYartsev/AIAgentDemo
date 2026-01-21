import logging
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)