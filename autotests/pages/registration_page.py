from pages.base_page import BasePage

class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_field = "#firstName"
        self.last_name_field = "#lastName"
        self.email_field = "#userEmail"
        self.mobile_field = "#userNumber"
        self.current_address_field = "#currentAddress"
        self.gender_options = {"Male": "#gender-radio-1", "Female": "#gender-radio-2", "Other": "#gender-radio-3"}
        self.date_of_birth_field = "#dateOfBirthInput"
        self.subjects_field = "#subjectsInput"
        self.hobbies_checkboxes = {"Sports": "#hobbies-checkbox-1", "Reading": "#hobbies-checkbox-2", "Music": "#hobbies-checkbox-3"}
        self.upload_picture_field = "#uploadPicture"
        self.state_dropdown = "#state"
        self.city_dropdown = "#city"
        self.submit_button = "#submit"

    def enter_first_name(self, first_name: str):
        self.log_info(f"Entering first name: {first_name}")
        self.page.fill(self.first_name_field, first_name)

    def enter_last_name(self, last_name: str):
        self.log_info(f"Entering last name: {last_name}")
        self.page.fill(self.last_name_field, last_name)

    def enter_email(self, email: str):
        self.log_info(f"Entering email: {email}")
        self.page.fill(self.email_field, email)

    def enter_mobile(self, mobile: str):
        self.log_info(f"Entering mobile: {mobile}")
        self.page.fill(self.mobile_field, mobile)

    def enter_current_address(self, address: str):
        self.log_info(f"Entering current address: {address}")
        self.page.fill(self.current_address_field, address)

    def select_gender(self, gender: str):
        self.log_info(f"Selecting gender: {gender}")
        self.page.click(self.gender_options[gender])

    def select_date_of_birth(self, date: str):
        self.log_info(f"Selecting date of birth: {date}")
        self.page.click(self.date_of_birth_field)
        self.page.fill(self.date_of_birth_field, date)
        self.page.press(self.date_of_birth_field, "Enter")

    def select_subjects(self, subjects: list):
        self.log_info(f"Selecting subjects: {subjects}")
        for subject in subjects:
            self.page.fill(self.subjects_field, subject)
            self.page.press(self.subjects_field, "Enter")

    def select_hobbies(self, hobbies: list):
        self.log_info(f"Selecting hobbies: {hobbies}")
        for hobby in hobbies:
            self.page.click(self.hobbies_checkboxes[hobby])

    def upload_picture(self, file_path: str):
        self.log_info(f"Uploading picture: {file_path}")
        self.page.set_input_files(self.upload_picture_field, file_path)

    def select_state(self, state: str):
        self.log_info(f"Selecting state: {state}")
        self.page.select_option(self.state_dropdown, label=state)

    def select_city(self, city: str):
        self.log_info(f"Selecting city: {city}")
        self.page.select_option(self.city_dropdown, label=city)

    def click_submit(self):
        self.log_info("Clicking submit button")
        self.page.click(self.submit_button)

    def verify_first_name_displayed(self, first_name: str):
        self.log_info(f"Verifying first name displayed: {first_name}")
        assert self.page.input_value(self.first_name_field) == first_name

    def verify_last_name_displayed(self, last_name: str):
        self.log_info(f"Verifying last name displayed: {last_name}")
        assert self.page.input_value(self.last_name_field) == last_name

    def verify_email_displayed(self, email: str):
        self.log_info(f"Verifying email displayed: {email}")
        assert self.page.input_value(self.email_field) == email

    def verify_mobile_displayed(self, mobile: str):
        self.log_info(f"Verifying mobile displayed: {mobile}")
        assert self.page.input_value(self.mobile_field) == mobile

    def verify_current_address_displayed(self, address: str):
        self.log_info(f"Verifying current address displayed: {address}")
        assert self.page.input_value(self.current_address_field) == address

    def verify_gender_selected(self, gender: str):
        self.log_info(f"Verifying gender selected: {gender}")
        assert self.page.is_checked(self.gender_options[gender])

    def verify_date_of_birth_displayed(self, date: str):
        self.log_info(f"Verifying date of birth displayed: {date}")
        assert self.page.input_value(self.date_of_birth_field) == date

    def verify_subjects_displayed(self, subjects: list):
        self.log_info(f"Verifying subjects displayed: {subjects}")
        for subject in subjects:
            assert subject in self.page.input_value(self.subjects_field)

    def verify_hobbies_selected(self, hobbies: list):
        self.log_info(f"Verifying hobbies selected: {hobbies}")
        for hobby in hobbies:
            assert self.page.is_checked(self.hobbies_checkboxes[hobby])

    def verify_picture_uploaded(self, file_name: str):
        self.log_info(f"Verifying picture uploaded: {file_name}")
        assert file_name in self.page.input_value(self.upload_picture_field)

    def verify_state_selected(self, state: str):
        self.log_info(f"Verifying state selected: {state}")
        assert self.page.input_value(self.state_dropdown) == state

    def verify_city_selected(self, city: str):
        self.log_info(f"Verifying city selected: {city}")
        assert self.page.input_value(self.city_dropdown) == city

    def verify_submit_button_clickable(self):
        self.log_info("Verifying submit button clickable")
        assert self.page.is_enabled(self.submit_button)

    def verify_form_submission(self):
        self.log_info("Verifying form submission")
        assert self.page.is_visible("text='Thanks for submitting the form'")

    def verify_results_table(self, data: dict):
        self.log_info("Verifying results table")
        for key, value in data.items():
            assert value in self.page.text_content(f"//td[contains(text(), '{value}')]")