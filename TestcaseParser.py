import json
from pathlib import Path
from typing import Type

from model import TestSuite  # предполагается, что у тебя есть класс/датакласс TestSuite


class TestcasesParser:
    @staticmethod
    def parse(path: str, model: Type[TestSuite] = TestSuite) -> TestSuite:
        """
        Аналог Java-метода parse.
        Читает JSON-файл и мапит его в объект TestSuite.
        """
        try:
            json_str = Path(path).read_text(encoding="utf-8")
            data = json.loads(json_str)
            # Ожидается, что TestSuite умеет инициализироваться из dict (например, датакласс с **data)
            return model(**data)
        except Exception as e:
            raise RuntimeError("Failed to parse testcases.json") from e

