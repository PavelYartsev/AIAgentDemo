import os
import requests


class MistralClient:
    API_URL = "https://api.mistral.ai/v1/chat/completions"
    API_KEY = os.getenv("MISTRAL_API_KEY")

    @classmethod
    def call(cls, prompt: str) -> str:
        if not cls.API_KEY:
            raise RuntimeError("MISTRAL_API_KEY not set")

        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": "You are a QA automation engineer. Return structured output."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls.API_KEY}"
        }

        try:
            response = requests.post(cls.API_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
