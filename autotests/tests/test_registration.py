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

    def load_test_data(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def test_registration_01(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_first_name(test_data["registration"]["valid_data"]["first_name"])
        self.registration_page.enter_last_name(test_data["registration"]["valid_data"]["last_name"])
        self.registration_page.verify_first_name_displayed(test_data["registration"]["valid_data"]["first_name"])
        self.registration_page.verify_last_name_displayed(test_data["registration"]["valid_data"]["last_name"])

    def test_registration_02(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_email(test_data["registration"]["valid_data"]["email"])
        self.registration_page.verify_email_displayed(test_data["registration"]["valid_data"]["email"])

    def test_registration_03(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_mobile(test_data["registration"]["valid_data"]["mobile"])
        self.registration_page.verify_mobile_displayed(test_data["registration"]["valid_data"]["mobile"])

    def test_registration_04(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_current_address(test_data["registration"]["valid_data"]["current_address"])
        self.registration_page.verify_current_address_displayed(test_data["registration"]["valid_data"]["current_address"])

    def test_registration_05(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_gender(test_data["registration"]["valid_data"]["gender"])
        self.registration_page.verify_gender_selected(test_data["registration"]["valid_data"]["gender"])

    def test_registration_06(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_date_of_birth(test_data["registration"]["valid_data"]["date_of_birth"])
        self.registration_page.verify_date_of_birth_displayed(test_data["registration"]["valid_data"]["date_of_birth"])

    def test_registration_07(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_subjects(test_data["registration"]["valid_data"]["subjects"])
        self.registration_page.verify_subjects_displayed(test_data["registration"]["valid_data"]["subjects"])

    def test_registration_08(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_hobbies(test_data["registration"]["valid_data"]["hobbies"])
        self.registration_page.verify_hobbies_selected(test_data["registration"]["valid_data"]["hobbies"])

    def test_registration_09(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.upload_picture(test_data["registration"]["valid_data"]["picture"])
        self.registration_page.verify_picture_uploaded(test_data["registration"]["valid_data"]["picture"])

    def test_registration_10(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_state(test_data["registration"]["valid_data"]["state"])
        self.registration_page.verify_state_selected(test_data["registration"]["valid_data"]["state"])

    def test_registration_11(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.select_city(test_data["registration"]["valid_data"]["city"])
        self.registration_page.verify_city_selected(test_data["registration"]["valid_data"]["city"])

    def test_registration_12(self):
        self.registration_page.verify_submit_button_clickable()

    def test_registration_13(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_first_name(test_data["registration"]["valid_data"]["first_name"])
        self.registration_page.enter_last_name(test_data["registration"]["valid_data"]["last_name"])
        self.registration_page.enter_email(test_data["registration"]["valid_data"]["email"])
        self.registration_page.enter_mobile(test_data["registration"]["valid_data"]["mobile"])
        self.registration_page.enter_current_address(test_data["registration"]["valid_data"]["current_address"])
        self.registration_page.select_gender(test_data["registration"]["valid_data"]["gender"])
        self.registration_page.select_date_of_birth(test_data["registration"]["valid_data"]["date_of_birth"])
        self.registration_page.select_subjects(test_data["registration"]["valid_data"]["subjects"])
        self.registration_page.select_hobbies(test_data["registration"]["valid_data"]["hobbies"])
        self.registration_page.upload_picture(test_data["registration"]["valid_data"]["picture"])
        self.registration_page.select_state(test_data["registration"]["valid_data"]["state"])
        self.registration_page.select_city(test_data["registration"]["valid_data"]["city"])
        self.registration_page.click_submit()
        self.registration_page.verify_form_submission()

    def test_registration_14(self):
        test_data = self.load_test_data("test_data/test_data.json")
        self.registration_page.enter_first_name(test_data["registration"]["valid_data"]["first_name"])
        self.registration_page.enter_last_name(test_data["registration"]["valid_data"]["last_name"])
        self.registration_page.enter_email(test_data["registration"]["valid_data"]["email"])
        self.registration_page.enter_mobile(test_data["registration"]["valid_data"]["mobile"])
        self.registration_page.enter_current_address(test_data["registration"]["valid_data"]["current_address"])
        self.registration_page.select_gender(test_data["registration"]["valid_data"]["gender"])
        self.registration_page.select_date_of_birth(test_data["registration"]["valid_data"]["date_of_birth"])
        self.registration_page.select_subjects(test_data["registration"]["valid_data"]["subjects"])
        self.registration_page.select_hobbies(test_data["registration"]["valid_data"]["hobbies"])
        self.registration_page.upload_picture(test_data["registration"]["valid_data"]["picture"])
        self.registration_page.select_state(test_data["registration"]["valid_data"]["state"])
        self.registration_page.select_city(test_data["registration"]["valid_data"]["city"])
        self.registration_page.click_submit()
        self.registration_page.verify_results_table(test_data["registration"]["valid_data"])