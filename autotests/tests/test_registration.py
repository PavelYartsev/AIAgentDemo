import pytest
import json
from pages.registration_page import RegistrationPage

class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, playwright, request):
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.registration_page = RegistrationPage(self.page)
        self.page.goto("https://demoqa.com/automation-practice-form")
        yield
        self.browser.close()

    @pytest.mark.parametrize("test_case", [
        ("REGISTRATION_01", "Verify first name and last name input"),
        ("REGISTRATION_02", "Verify email input"),
        ("REGISTRATION_03", "Verify 10-digit mobile number input"),
        ("REGISTRATION_04", "Verify current address input"),
        ("REGISTRATION_05", "Verify gender selection"),
        ("REGISTRATION_06", "Verify date of birth selection"),
        ("REGISTRATION_07", "Verify subject(s) input with autocomplete selection"),
        ("REGISTRATION_08", "Verify hobbies selection using checkboxes"),
        ("REGISTRATION_09", "Verify file upload in the Picture field"),
        ("REGISTRATION_10", "Verify State selection from the drop-down list"),
        ("REGISTRATION_11", "Verify City selection after selecting the State"),
        ("REGISTRATION_12", "Verify Submit button is clickable when required fields are filled in correctly"),
        ("REGISTRATION_13", "Verify modal window appears after clicking Submit"),
        ("REGISTRATION_14", "Verify results table displays all entered data")
    ])
    def test_registration(self, test_case):
        test_id, test_title = test_case
        with open("test_data/test_data.json") as f:
            test_data = json.load(f)
        self.registration_page.fill_registration_form(test_data["valid_registration_data"])
        # Add assertions based on the test case
        # Example for REGISTRATION_01:
        if test_id == "REGISTRATION_01":
            self.registration_page.check_element_text(self.registration_page.first_name_field, test_data["valid_registration_data"]["first_name"])
            self.registration_page.check_element_text(self.registration_page.last_name_field, test_data["valid_registration_data"]["last_name"])
        # Add more assertions for other test cases