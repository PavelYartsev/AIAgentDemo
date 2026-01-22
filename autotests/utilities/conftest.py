import pytest
import logging
from utilities.logger import setup_logger

def pytest_configure(config):
    setup_logger()

@pytest.fixture(scope="session")
def playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        yield playwright