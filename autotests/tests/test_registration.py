import json
import pytest
from playwright.sync_api import Page
from ..pages.registration_page import RegistrationPage
from ..pages.results_page import ResultsPage


class TestRegistration:
    @pytest.fixture
    def registration_page(self, page: Page):
        return RegistrationPage(page)

    @pytest.fixture
    def results_page(self, page: Page):
        return ResultsPage(page)

    @pytest.fixture
    def test_data(self):
        with open("test_data/test_data.json") as f:
            return json.load(f)

    def test_verify_first_name_field(self, registration_page, test_data):
        registration_page.enter_first_name(test_data["valid_first_name"])
        assert registration_page.page.input_value(registration_page.first_name_field) == test_data["valid_first_name"]

    def test_verify_last_name_field(self, registration_page, test_data):
        registration_page.enter_last_name(test_data["valid_last_name"])
        assert registration_page.page.input_value(registration_page.last_name_field) == test_data["valid_last_name"]

    def test_verify_email_field(self, registration_page, test_data):
        registration_page.enter_email(test_data["valid_email"])
        assert registration_page.page.input_value(registration_page.email_field) == test_data["valid_email"]

    def test_verify_mobile_field(self, registration_page, test_data):
        registration_page.enter_mobile(test_data["valid_mobile"])
        assert registration_page.page.input_value(registration_page.mobile_field) == test_data["valid_mobile"]

    def test_verify_current_address_field(self, registration_page, test_data):
        registration_page.enter_current_address(test_data["valid_current_address"])
        assert registration_page.page.input_value(registration_page.current_address_field) == test_data[
            "valid_current_address"]

    def test_verify_gender_selection(self, registration_page):
        registration_page.select_gender("Male")
        assert registration_page.page.is_checked(registration_page.gender_male)
        registration_page.select_gender("Female")
        assert registration_page.page.is_checked(registration_page.gender_female)
        registration_page.select_gender("Other")
        assert registration_page.page.is_checked(registration_page.gender_other)

    def test_verify_date_of_birth_selection(self, registration_page, test_data):
        registration_page.select_date_of_birth(test_data["valid_date_of_birth"])
        assert registration_page.page.input_value(registration_page.date_of_birth_field) == test_data[
            "valid_date_of_birth"]

    def test_verify_subjects_field_with_autocomplete_selection(self, registration_page, test_data):
        registration_page.select_subject(test_data["valid_subject"])
        assert registration_page.page.input_value(registration_page.subjects_field) == test_data["valid_subject"]

    def test_verify_hobbies_selection_using_checkboxes(self, registration_page, test_data):
        registration_page.select_hobby(test_data["valid_hobby"])
        assert registration_page.page.is_checked(registration_page.hobbies_sports)

    def test_verify_picture_field_upload(self, registration_page, test_data):
        registration_page.upload_picture(test_data["valid_picture_path"])
        assert registration_page.page.input_value(registration_page.picture_field) == test_data["valid_picture_path"]

    def test_verify_state_selection_from_the_drop_down_list(self, registration_page, test_data):
        registration_page.select_state(test_data["valid_state"])
        assert registration_page.page.inner_text(registration_page.state_dropdown) == test_data["valid_state"]

    def test_verify_city_selection_after_selecting_the_state(self, registration_page, test_data):
        registration_page.select_state(test_data["valid_state"])
        registration_page.select_city(test_data["valid_city"])
        assert registration_page.page.inner_text(registration_page.city_dropdown) == test_data["valid_city"]

    def test_verify_submit_button_is_clickable_when_required_fields_are_filled_in_correctly(self, registration_page,
                                                                                            test_data):
        registration_page.enter_first_name(test_data["valid_first_name"])
        registration_page.enter_last_name(test_data["valid_last_name"])
        registration_page.enter_email(test_data["valid_email"])
        registration_page.enter_mobile(test_data["valid_mobile"])
        registration_page.enter_current_address(test_data["valid_current_address"])
        registration_page.select_gender("Male")
        registration_page.select_date_of_birth(test_data["valid_date_of_birth"])
        registration_page.select_subject(test_data["valid_subject"])
        registration_page.select_hobby(test_data["valid_hobby"])
        registration_page.upload_picture(test_data["valid_picture_path"])
        registration_page.select_state(test_data["valid_state"])
        registration_page.select_city(test_data["valid_city"])
        assert registration_page.page.is_enabled(registration_page.submit_button)

    def test_click_submit_and_check_that_the_modal_window_with_the_title_appears(self, registration_page, results_page,
                                                                                 test_data):
        registration_page.enter_first_name(test_data["valid_first_name"])
        registration_page.enter_last_name(test_data["valid_last_name"])
        registration_page.enter_email(test_data["valid_email"])
        registration_page.enter_mobile(test_data["valid_mobile"])
        registration_page.enter_current_address(test_data["valid_current_address"])
        registration_page.select_gender("Male")
        registration_page.select_date_of_birth(test_data["valid_date_of_birth"])
        registration_page.select_subject(test_data["valid_subject"])
        registration_page.select_hobby(test_data["valid_hobby"])
        registration_page.upload_picture(test_data["valid_picture_path"])
        registration_page.select_state(test_data["valid_state"])
        registration_page.select_city(test_data["valid_city"])
        registration_page.click_submit()
        results_page.verify_modal_title("Thanks for submitting the form")

    def test_verify_that_the_results_table_displays_all_entered_data(self, registration_page, results_page, test_data):
        registration_page.enter_first_name(test_data["valid_first_name"])
        registration_page.enter_last_name(test_data["valid_last_name"])
        registration_page.enter_email(test_data["valid_email"])
        registration_page.enter_mobile(test_data["valid_mobile"])
        registration_page.enter_current_address(test_data["valid_current_address"])
        registration_page.select_gender("Male")
        registration_page.select_date_of_birth(test_data["valid_date_of_birth"])
        registration_page.select_subject(test_data["valid_subject"])
        registration_page.select_hobby(test_data["valid_hobby"])
        registration_page.upload_picture(test_data["valid_picture_path"])
        registration_page.select_state(test_data["valid_state"])
        registration_page.select_city(test_data["valid_city"])
        registration_page.click_submit()
        expected_data = {
            "Student Name": f"{test_data['valid_first_name']} {test_data['valid_last_name']}",
            "Student Email": test_data["valid_email"],
            "Mobile": test_data["valid_mobile"],
            "Date of Birth": test_data["valid_date_of_birth"],
            "Subjects": test_data["valid_subject"],
            "Hobbies": test_data["valid_hobby"],
            "Address": test_data["valid_current_address"],
            "State and City": f"{test_data['valid_state']} {test_data['valid_city']}"
        }
        results_page.verify_results_table(expected_data)
