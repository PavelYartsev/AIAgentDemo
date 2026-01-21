import pytest
import logging
from utilities.logger import setup_logger

def pytest_configure(config):
    setup_logger()

@pytest.fixture(scope="session")
def logger():
    return logging.getLogger(__name__)