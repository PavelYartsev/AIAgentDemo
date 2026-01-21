from base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_field = "#firstName"
        self.last_name_field = "#lastName"
        self.email_field = "#userEmail"
        self.mobile_field = "#userNumber"
        self.current_address_field = "#currentAddress"
        self.gender_male = "#gender-radio-1"
        self.gender_female = "#gender-radio-2"
        self.gender_other = "#gender-radio-3"
        self.date_of_birth_field = "#dateOfBirthInput"
        self.subjects_field = "#subjectsInput"
        self.hobbies_sports = "#hobbies-checkbox-1"
        self.hobbies_reading = "#hobbies-checkbox-2"
        self.hobbies_music = "#hobbies-checkbox-3"
        self.picture_field = "#uploadPicture"
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
        if gender.lower() == "male":
            self.page.click(self.gender_male)
        elif gender.lower() == "female":
            self.page.click(self.gender_female)
        elif gender.lower() == "other":
            self.page.click(self.gender_other)

    def select_date_of_birth(self, date_of_birth: str):
        self.log_info(f"Selecting date of birth: {date_of_birth}")
        self.page.fill(self.date_of_birth_field, date_of_birth)

    def select_subject(self, subject: str):
        self.log_info(f"Selecting subject: {subject}")
        self.page.fill(self.subjects_field, subject)
        self.page.press(self.subjects_field, "Enter")

    def select_hobby(self, hobby: str):
        self.log_info(f"Selecting hobby: {hobby}")
        if hobby.lower() == "sports":
            self.page.click(self.hobbies_sports)
        elif hobby.lower() == "reading":
            self.page.click(self.hobbies_reading)
        elif hobby.lower() == "music":
            self.page.click(self.hobbies_music)

    def upload_picture(self, file_path: str):
        self.log_info(f"Uploading picture: {file_path}")
        self.page.set_input_files(self.picture_field, file_path)

    def select_state(self, state: str):
        self.log_info(f"Selecting state: {state}")
        self.page.select_option(self.state_dropdown, state)

    def select_city(self, city: str):
        self.log_info(f"Selecting city: {city}")
        self.page.select_option(self.city_dropdown, city)

    def click_submit(self):
        self.log_info("Clicking submit button")
        self.page.click(self.submit_button)
