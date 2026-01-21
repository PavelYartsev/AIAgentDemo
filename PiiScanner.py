import re
from typing import List, Dict, Any
from collections import defaultdict
from PiiReport import PiiReport


class PiiScanner:
    """Сканер персональных данных (PII)"""

    # Расширенные паттерны для поиска PII
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        re.IGNORECASE
    )

    PHONE_PATTERN = re.compile(
        r"\+?[\d\s\-()]{10,}",  # Улучшенный паттерн телефонов
        re.IGNORECASE
    )

    PASSWORD_PATTERN = re.compile(
        r"(?i)(password|pass|pwd)[\s:=]*['\"]?\S+['\"]?",
        re.IGNORECASE
    )

    PRODUCT_KEY_PATTERN = re.compile(
        r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-?[A-Z0-9]{0,5}",
        re.IGNORECASE
    )

    @classmethod
    def scan(cls, text: str) -> PiiReport:
        """Сканирует текст на наличие PII"""
        report = PiiReport()

        # Сканируем все типы PII
        cls._find_all(text, report)

        return report

    @classmethod
    def _find_all(cls, text: str, report: PiiReport):
        """Находит все типы PII в тексте"""
        patterns = [
            (cls.EMAIL_PATTERN, "EMAIL"),
            (cls.PHONE_PATTERN, "PHONE"),
            (cls.PASSWORD_PATTERN, "PASSWORD"),
            (cls.PRODUCT_KEY_PATTERN, "PRODUCT_KEY")
        ]

        for pattern, pii_type in patterns:
            cls._find(text, pattern, pii_type, report)

    @classmethod
    def _find(cls, text: str, pattern: re.Pattern, pii_type: str,
              report: PiiReport):
        """Вспомогательный метод поиска совпадений"""
        for match in pattern.finditer(text):
            full_match = match.group()
            report.add(f"{pii_type}: {full_match}")


# Пример использования и тест
if __name__ == "__main__":
    # Тестовый текст с PII из ваших файлов
    test_text = """
    Visual Studio Professional 2015
    Key : HMGNV-WCYXV-X7G9W-YCX63-B98R2
    HM6NR-QXX7C-DFW2Y-8B82K-WTYJV
    borodicht@gmail.com
    +7 (495) 123-45-67
    password: secret123
    pass = mypass456
    """

    scanner = PiiScanner()
    report = scanner.scan(test_text)

    print(report)
    print("\nJSON:", report.to_dict())
