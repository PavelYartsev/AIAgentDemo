from pages.base_page import BasePage

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
        self.hobbies_sports = "#hobbiesWrapper > .custom-control:nth-child(1) > .custom-control-input"
        self.hobbies_reading = "#hobbiesWrapper > .custom-control:nth-child(2) > .custom-control-input"
        self.hobbies_music = "#hobbiesWrapper > .custom-control:nth-child(3) > .custom-control-input"
        self.upload_picture_button = "#uploadPicture"
        self.state_field = "#state"
        self.city_field = "#city"
        self.submit_button = "#submit"
        self.modal_title = ".modal-title"
        self.results_table = ".table-responsive"

    def fill_registration_form(self, data):
        self.fill_field(self.first_name_field, data["first_name"])
        self.fill_field(self.last_name_field, data["last_name"])
        self.fill_field(self.email_field, data["email"])
        self.fill_field(self.mobile_field, data["mobile"])
        self.fill_field(self.current_address_field, data["current_address"])
        self.click(self.gender_male if data["gender"] == "Male" else self.gender_female if data["gender"] == "Female" else self.gender_other)
        self.fill_field(self.date_of_birth_field, data["date_of_birth"])
        self.fill_field(self.subjects_field, data["subjects"])
        self.click(self.hobbies_sports if "Sports" in data["hobbies"] else self.hobbies_sports)
        self.click(self.hobbies_reading if "Reading" in data["hobbies"] else self.hobbies_reading)
        self.click(self.hobbies_music if "Music" in data["hobbies"] else self.hobbies_music)
        self.click(self.upload_picture_button)
        self.select_option(self.state_field, data["state"])
        self.select_option(self.city_field, data["city"])