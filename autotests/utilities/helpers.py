import os
from playwright.sync_api import sync_playwright


def get_playwright():
    return sync_playwright().start()


def get_browser(browser_type="chromium"):
    playwright = get_playwright()
    browser = playwright[browser_type].launch(headless=False)
    return browser


def get_page(browser):
    return browser.new_page()


def close_browser(browser):
    browser.close()


def close_playwright(playwright):
    playwright.stop()
