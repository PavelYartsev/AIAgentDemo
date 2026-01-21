import re


class PiiMasker:
    """Маскирует PII (персональные данные) в тексте"""

    # Те же регулярные выражения, что в оригинале Java
    EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_PATTERN = r"\+?\d[\d\s\-()]{7,}"
    PASSWORD_PATTERN = r"(?i)(password\s*[:=]\s*)\S+"

    @staticmethod
    def mask(text: str) -> str:
        """
        Маскирует PII в тексте:
        - email → [EMAIL]
        - телефон → [PHONE]
        - password:xxx → password:[SECRET]
        """
        masked = text

        # Заменяем по тому же порядку, что в Java
        masked = re.sub(PiiMasker.EMAIL_PATTERN, "[EMAIL]", masked, flags=re.IGNORECASE)
        masked = re.sub(PiiMasker.PHONE_PATTERN, "[PHONE]", masked)
        masked = re.sub(PiiMasker.PASSWORD_PATTERN, r"\g<0>[SECRET]", masked, flags=re.IGNORECASE)

        return masked


# Пример использования и тест
if __name__ == "__main__":
    test_cases = [
        "Contact: john.doe@example.com or +7(495)123-45-67",
        'Config: password=secret123, email=user@test.ru',
        "Call +380501234567 or john@gmail.com. password : mypass456",
        "No PII here: just text 123-456"
    ]

    print("=== PII Masker Test ===\n")
    for text in test_cases:
        original = text
        masked = PiiMasker.mask(text)
        print(f"Original:  {original}")
        print(f"Masked:    {masked}")
        print("-" * 50)
