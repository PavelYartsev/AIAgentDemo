import json
import os

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
        structure_start_match = re.search(r"Project Structure\n", text)
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
        file_contents = {}

        # Находим начало секции "### Project Code"
        file_contents_start_match = re.search(r"^### Project Code\n", text, re.MULTILINE)
        if not file_contents_start_match:
            print("Warning: '### Project Code' section not found in the description text. No files will be parsed.")
            return file_contents

        text_to_parse = text[file_contents_start_match.end():]
        lines = text_to_parse.splitlines()

        # Pattern for file headers: "autotests/path/to/file.py" at the start of a line
        file_header_pattern = re.compile(r"^autotests\/([a-zA-Z0-9_\-.\/]+)") 
        code_block_pattern = re.compile(r"```(?:[a-zA-Z0-9]+)?\n(.*?)\n```", re.DOTALL)

        current_file_path = None
        current_file_content_lines = []
        is_in_code_block_mode = False # To handle content that is not in ``` ``` blocks

        for line in lines:
            header_match = file_header_pattern.match(line.strip())
            
            if header_match:
                # If we were collecting content for a previous file, save it
                if current_file_path:
                    full_content = "\n".join(current_file_content_lines).strip()
                    code_match = code_block_pattern.search(full_content)
                    
                    content_to_save = code_match.group(1).strip() if code_match else full_content
                    file_contents[os.path.join(root_dir, current_file_path)] = content_to_save

                # Start collecting content for the new file
                file_path_raw = header_match.group(1).strip() # Capture without "autotests/" prefix
                current_file_path = file_path_raw
                current_file_content_lines = []
                is_in_code_block_mode = False # Reset for new file
            elif current_file_path:
                # Only accumulate if we have a current file being processed
                current_file_content_lines.append(line)

        # Process the last file after the loop finishes
        if current_file_path:
            full_content = "\n".join(current_file_content_lines).strip()
            code_match = code_block_pattern.search(full_content)
            content_to_save = code_match.group(1).strip() if code_match else full_content
            file_contents[os.path.join(root_dir, current_file_path)] = content_to_save
        
        return file_contents



    @staticmethod
    def _generate_tree_string(paths: list[str], root_dir: str) -> str:
        # Create a nested dict from paths
        tree = {}
        for path in sorted(paths):
            # remove root_dir prefix
            parts = path.replace(f"{root_dir}/", "", 1).split('/')
            node = tree
            for part in parts:
                node = node.setdefault(part, {})

        # Recursively build the string
        def build_string(node, indent=""):
            lines = []
            sorted_items = sorted(node.items())
            for i, (name, children) in enumerate(sorted_items):
                is_last = i == (len(sorted_items) - 1)
                connector = "└── " if is_last else "├── "
                lines.append(f"{indent}{connector}{name}")
                if children:
                    child_indent = "    " if is_last else "│   "
                    lines.extend(build_string(children, indent + child_indent))
            return lines

        tree_lines = build_string(tree)
        return f"{root_dir}/\n" + "\n".join(tree_lines)

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

        # Integrate generated autotests into project structure
        print("Integrating generated autotests into 'autotests' project structure...")

        autotests_root = "autotests"

        # Recreate autotests project directory to ensure a clean state
        FilesUtil.delete_dir_if_exists(autotests_root)
        FilesUtil.create_dir_if_not_exists(autotests_root)

        # Parse file contents from LLM output. This is now the single source of truth.
        file_contents_map = PipelineMain._parse_file_contents(autotests_llm_text, root_dir=autotests_root)

        if not file_contents_map:
            print("Warning: No file contents were parsed from the LLM output. The 'autotests' directory will be empty.")

        # Generate a clean project structure tree string and inject it into README.md
        if file_contents_map:
            clean_tree_str = PipelineMain._generate_tree_string(
                list(file_contents_map.keys()), autotests_root
            )
            print("--- Generated Clean Project Structure ---")
            print(clean_tree_str)
            print("---------------------------------------")

            readme_key = f"{autotests_root}/README.md"
            if readme_key in file_contents_map:
                print(f"Injecting clean structure into {readme_key}...")
                readme_content = file_contents_map[readme_key]

                # This regex finds "## Project Structure" and makes the code block after it optional
                pattern = re.compile(
                    r"(#{2,3}\s+### Project Structure\s*\n+)(?:```.*?```)?",
                    re.DOTALL | re.IGNORECASE
                )

                replacement = r"\1" + f"```\n{clean_tree_str.replace('\\', '\\\\')}\n```"
                new_readme_content, num_replacements = pattern.subn(replacement, readme_content)

                if num_replacements > 0:
                    file_contents_map[readme_key] = new_readme_content
                    print("Injection successful.")
                else:
                    print("Warning: Could not find a 'Project Structure' section to replace in README.md.")

        # Write all files. Parent directories are created automatically by FilesUtil.write.
        for file_path, content in file_contents_map.items():
            FilesUtil.write(file_path, content)
            print(f"Saved file: {file_path}")

        print("Autotests generated and integrated into 'autotests' project.")

        # STAGE 6. AI CODE REVIEW
        print("STAGE 6: AI code review...")
        generated_test = FilesUtil.read("generated/autotests.txt")
        review_prompt = FilesUtil.read("prompts/04_code_review.txt").replace("{{CODE}}", generated_test)
        FilesUtil.write("generated/code_review_prompt.txt", review_prompt)

        raw_review = MistralClient.MistralClient.call(review_prompt)
        FilesUtil.write("generated/code_review_raw.json", raw_review)

        review = PipelineMain.extract_assistant_content(raw_review)
        FilesUtil.write("generated/code_review.txt", review)

        print("AI code review saved: generated/code_review.txt")

        # STAGE 7. AI BUG REPORT (DESIGN-TIME)
        print("STAGE 7: Generating AI bug report...")
        checklist = FilesUtil.read("checklist_submitForm.txt")
        testcases = FilesUtil.read("generated/testcases.json")
        code_review = FilesUtil.read("generated/code_review.txt")

        bug_prompt = (
            FilesUtil.read("prompts/05_bug_report.txt")
            .replace("{{CHECKLIST}}", checklist)
            .replace("{{TESTCASES}}", testcases)
            .replace("{{REVIEW}}", code_review)
        )

        FilesUtil.write("generated/bug_report_prompt.txt", bug_prompt)

        raw_bug = MistralClient.MistralClient.call(bug_prompt)
        FilesUtil.write("generated/bug_report_raw.json", raw_bug)

        bug_text = PipelineMain.extract_assistant_content(raw_bug)
        FilesUtil.write("generated/bug_report_llm.txt", bug_text)

        pure_bug_json = JsonExtractor.JsonExtractor.extract_json(bug_text)
        FilesUtil.write("generated/bug_report.json", pure_bug_json)

        print("Bug report saved: generated/bug_report.json")
        print("=== AI QA PIPELINE FINISHED ===")


if __name__ == "__main__":
    PipelineMain.main()
