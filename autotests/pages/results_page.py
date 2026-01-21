from base_page import BasePage


class ResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.results_table = ".table-responsive"
        self.modal_title = ".modal-title"

    def verify_modal_title(self, expected_title: str):
        self.log_info(f"Verifying modal title: {expected_title}")
        assert self.page.inner_text(self.modal_title) == expected_title

    def verify_results_table(self, expected_data: dict):
        self.log_info("Verifying results table")
        for key, value in expected_data.items():
            assert self.page.inner_text(
                f"//td[contains(text(), '{key}')]/following-sibling::td[contains(text(), '{value}')]")
