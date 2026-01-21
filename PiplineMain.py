import json

import GeminiClient
import JsonExtractor
import MistralClient
from PiiScanner import PiiScanner
from PiiReport import PiiReport
from PiiMasker import PiiMasker
from FilesUtil import FilesUtil
from PromptEngine import PromptEngine


class PipelineMain:
    @staticmethod
    def main() -> None:
        print("=== AI QA PIPELINE STARTED ===")

        # STAGE 1. BUILD PROMPT FROM CHECKLIST
        prompt = PromptEngine.build_prompt(
            "prompts/01_scenarios_from_checklist.txt",
            "checklist_submitForm.txt",
        )
        FilesUtil.write("generated/final_prompt.txt", prompt)

        # STAGE 2. PII SCAN & MASK
        print("STAGE 2: Scanning for PII...")
        report: PiiReport = PiiScanner.scan(prompt)
        FilesUtil.write("generated/pii_report.txt", str(report))
        print(f"Found {len(report.findings)} PII items")

        final_prompt = prompt

        if report.findings:
            print("PII detected. Masking input.")
            final_prompt = PiiMasker.mask(prompt)
            FilesUtil.write("generated/prompt_masked.txt", final_prompt)

        # STAGE 3. GENERATE SCENARIOS
        print("STAGE 3: Generating scenarios via LLM...")
        # raw_scenarios = GeminiClient.GeminiClient.call(final_prompt)
        raw_scenarios = MistralClient.MistralClient.call(final_prompt)
        FilesUtil.write("generated/scenarios_raw.json", raw_scenarios)

        scenarios = PipelineMain.extract_assistant_content(raw_scenarios)
        FilesUtil.write("generated/ai_output.txt", scenarios)

        # STAGE 4. GENERATE JSON TESTCASES
        print("STAGE 4: Generating JSON testcases...")
        json_prompt = FilesUtil.read("prompts/02_testcases_json.txt").replace(
            "{{SCENARIOS}}", scenarios
        )
        FilesUtil.write("generated/testcases_prompt.txt", json_prompt)

        # raw_json = GeminiClient.GeminiClient.call(json_prompt)
        raw_json = MistralClient.MistralClient.call(json_prompt)
        FilesUtil.write("generated/testcases_raw.json", raw_json)

        llm_json_text = PipelineMain.extract_assistant_content(raw_json)
        FilesUtil.write("generated/testcases_llm.txt", llm_json_text)

        pure_json = JsonExtractor.extract_json(llm_json_text)
        FilesUtil.write("generated/testcases.json", pure_json)

        print("Testcases generated: generated/testcases.json")
        print("=== AI QA PIPELINE FINISHED ===")


@staticmethod
def extract_assistant_content(raw_json: str) -> str:
    """
    Извлекает все текстовое содержимое из ответа Gemini API.
    Ожидаемая структура - это JSON-объект со списком "candidates",
    где у каждого кандидата есть "content" с "parts", которые содержат "text".
    """
    try:
        data = json.loads(raw_json)
        all_text_parts = []
        for candidate in data.get("candidates", []):
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                all_text_parts.append(part.get("text", ""))
        return "".join(all_text_parts)
    except (json.JSONDecodeError, IndexError, KeyError) as e:
        raise RuntimeError(
            "Failed to extract assistant content from LLM response"
        ) from e


if __name__ == "__main__":
    PipelineMain.main()
