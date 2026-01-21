class JsonExtractor:
    @staticmethod
    def extract_json(text: str) -> str:
        """
        Аналог Java-метода extractJson.
        Удаляет markdown-ограждения ```json / ``` и возвращает
        подстроку от первой '{' до последней '}' включительно.
        """
        if text is None:
            raise RuntimeError("LLM returned null")

        # remove markdown fences
        cleaned = (
            text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # try to cut everything before first {
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise RuntimeError("No JSON object found in LLM output")

        return cleaned[start : end + 1].strip()
