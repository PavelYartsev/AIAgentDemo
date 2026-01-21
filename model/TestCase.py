# model/TestCase.py
from dataclasses import dataclass
from typing import List


@dataclass
class TestCase:
    id: str
    title: str
    type: str
    steps: List[str]
    expected: str