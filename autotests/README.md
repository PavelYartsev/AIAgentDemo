# Automation Project for Registration Form

## Project Structure

```
autotests/
├── .gitignore
├── README.md
├── pages
│   ├── base_page.py
│   └── registration_page.py
├── requirements.txt
├── test_data
│   └── test_data.json
├── tests
│   └── test_registration.py
└── utilities
    ├── conftest.py
    ├── helper.py
    └── logger.py
```- **pages/**: Contains Page Object classes for the registration form.
- **test_data/**: Contains test data in JSON format.
- **tests/**: Contains test cases for the registration form.
- **utilities/**: Contains utility files like conftest.py, logger.py, and helper.py.
- **reports/**: Contains allure reports generated after test execution.

## Prerequisites

- Python 3.8 or higher
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd automation_project