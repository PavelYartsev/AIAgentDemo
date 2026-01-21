import os
import json
import requests


class GeminiClient:
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
    API_KEY = os.getenv("GEMINI_API_KEY")

    @classmethod
    def call(cls, prompt: str) -> str:
        if not cls.API_KEY or cls.API_KEY.strip() == "":
            raise RuntimeError("GEMINI_API_KEY not set")

        try:
            # Аналог safePrompt из Java, но через JSON безопаснее
            body = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "You are Senior QA automation engineer. Return structured output."
                            }
                        ]
                    }
                ],

                "generationConfig": {
                    "temperature": 0.2
                }
            }

            headers = {
                "Content-Type": "application/json",
                # "Authorization": f"Bearer {cls.API_KEY}",
            }

            response = requests.post(cls.API_URL + cls.API_KEY, headers=headers, data=json.dumps(body))
            response.raise_for_status()

            # Возвращаем «сырой» JSON как строку, как и в Java
            print(response.text)
            return response.text

        except Exception as e:
            raise RuntimeError(str(e)) from e
