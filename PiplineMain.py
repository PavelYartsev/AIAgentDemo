import json

import GeminiClient
import JsonExtractor
import MistralClient
from PiiScanner import PiiScanner
from PiiReport import PiiReport
from PiiMasker import PiiMasker
from FilesUtil import FilesUtil
from PromptEngine import PromptEngine
import re
from pathlib import Path


class PipelineMain:
    @staticmethod
    def extract_assistant_content(raw_json: str) -> str:
        """
        Извлекает текст ассистента из ответа Mistral Chat Completions.
        Ожидается структура вида:
        {
          "id": "...",
          "choices": [
            {
              "index": 0,
              "message": {
                "role": "assistant",
                "content": "..."
              },
              ...
            }
          ],
          ...
        }
        """
        try:
            data = json.loads(raw_json)
            all_contents = []

            for choice in data.get("choices", []):
                message = choice.get("message", {})
                content = message.get("content", "")
                if isinstance(content, str):
                    all_contents.append(content)
                elif isinstance(content, list):
                    # На случай, если content придёт как список чанков
                    for part in content:
                        if isinstance(part, dict):
                            all_contents.append(
                                part.get("text", "") or part.get("content", "")
                            )

            return "".join(all_contents)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise RuntimeError(
                "Failed to extract assistant content from Mistral API response"
            ) from e

    @staticmethod
    def _extract_code_blocks(text: str) -> list[str]:
        """
        Extracts code blocks from a markdown-formatted string.
        Assumes code blocks are delimited by triple backticks (```).
        """
        # Regex to find blocks starting with ``` (optional language) and ending with ```
        pattern = re.compile(r"```(?:\w+)?\n(.*?)\n```", re.DOTALL)
        return pattern.findall(text)

    @staticmethod
    def _parse_project_structure(text: str, root_dir: str = "autotests") -> list[str]:
        """
        Parses the 'Project Structure:' section from the LLM output to extract
        a list of file and directory paths.
        Assumes an indented tree-like structure.
        """
        structure_start_match = re.search(r"Project Structure:\n", text)
        if not structure_start_match:
            print("Warning: 'Project Structure:' section not found in LLM output.")
            return []

        structure_text = text[structure_start_match.end():]
        # Find the end of the structure section, e.g., by another heading or separator
        structure_end_match = re.search(r"\n\n\S+", structure_text)  # Finds next non-indented line
        if structure_end_match:
            structure_text = structure_text[:structure_end_match.start()]

        lines = structure_text.strip().split('\n')
        paths = []
        path_stack = []  # To keep track of current path depth

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            leading_spaces = len(line) - len(line.lstrip(' '))
            depth = leading_spaces // 4  # Assuming 4 spaces per indent level

            clean_name = re.sub(r'^[│\s└├─]+', '', line.strip()).rstrip('/')
            if not clean_name:
                continue

            while len(path_stack) > depth:
                path_stack.pop()

            current_path_parts = path_stack + [clean_name]
            full_path = f"{root_dir}/{'/'.join(current_path_parts)}"
            paths.append(full_path)

            # Look ahead to determine if the current item is a directory
            is_directory = False
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip():
                    next_line_leading_spaces = len(next_line) - len(next_line.lstrip(' '))
                    next_line_depth = next_line_leading_spaces // 4
                    if next_line_depth > depth:
                        is_directory = True

            if is_directory:
                path_stack.append(clean_name)

        return paths

    @staticmethod
    def _parse_file_contents(text: str, root_dir: str = "autotests") -> dict[str, str]:
        """
        Parses the file content sections from the LLM output.
        Assumes content blocks are preceded by '#### path/to/file.py'
        and contain Markdown code blocks.
        """
        file_contents = {}
        # Pattern to find '#### path/to/file' followed by a code block.
        # The path is relative and needs the root_dir prepended.
        pattern = re.compile(
            r"####\s+([^\n]+)\n```(?:\w+)?\n(.*?)\n```",
            re.DOTALL
        )

        for match in pattern.finditer(text):
            # The captured path is relative, e.g., 'pages/base_page.py'
            relative_path = match.group(1).strip().replace('\\', '/')
            # Prepend the root directory to form the full path
            full_path = f"{root_dir}/{relative_path}"
            content = match.group(2).strip()
            file_contents[full_path] = content
        return file_contents


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

        pure_json = JsonExtractor.JsonExtractor.extract_json(llm_json_text)
        FilesUtil.write("generated/testcases.json", pure_json)

        print("Testcases generated: generated/testcases.json")

        # STAGE 5. GENERATE AUTOTESTS AND ADD TO PROJECT
        print("STAGE 5: Generating autotests via LLM...")
        autotest_prompt = FilesUtil.read("prompts/03_automation_tests.txt").replace(
            "{{TESTCASES}}", pure_json
        )
        FilesUtil.write("generated/autotests_prompt.txt", autotest_prompt)

        raw_autotests = MistralClient.MistralClient.call(autotest_prompt)
        FilesUtil.write("generated/autotests_raw.json", raw_autotests)

        autotests_llm_text = PipelineMain.extract_assistant_content(raw_autotests)
        FilesUtil.write("generated/autotests.txt", autotests_llm_text)

        print(f"--- Raw LLM Output (autotests.txt) ---\n{autotests_llm_text}\n--------------------------------------")

        # STAGE 5.5: Integrate generated autotests into project structure
        print("Integrating generated autotests into 'autotests' project structure...")

        autotests_root = "autotests"

        # Recreate autotests project directory to ensure a clean state
        FilesUtil.delete_dir_if_exists(autotests_root)
        FilesUtil.create_dir_if_not_exists(autotests_root)

        # Parse project structure and file contents from LLM output
        all_paths = PipelineMain._parse_project_structure(autotests_llm_text, root_dir=autotests_root)
        print(f"--- Parsed Project Structure Paths ---\n{all_paths}\n--------------------------------------")
        file_contents_map = PipelineMain._parse_file_contents(autotests_llm_text, root_dir=autotests_root)

        # Create all directories that are part of the structure but are not files
        for path in all_paths:
            if path not in file_contents_map:
                FilesUtil.create_dir_if_not_exists(path)
                print(f"Created directory: {path}")

        # Write all files
        for file_path, content in file_contents_map.items():
            FilesUtil.write(file_path, content)
            print(f"Saved file: {file_path}")

        print("Autotests generated and integrated into 'autotests' project.")
        print("=== AI QA PIPELINE FINISHED ===")


if __name__ == "__main__":
    PipelineMain.main()
