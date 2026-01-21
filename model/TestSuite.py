# model/TestSuite.py
from dataclasses import dataclass
from typing import List

from TestCase import TestCase


@dataclass
class TestSuite:
    testcases: List[TestCase]
