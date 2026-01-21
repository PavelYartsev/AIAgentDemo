from FilesUtil import FilesUtil


class PromptEngine:
    @staticmethod
    def build_prompt(prompt_template_path: str, checklist_path: str) -> str:
        template = FilesUtil.read(prompt_template_path)
        checklist = FilesUtil.read(checklist_path)
        return template.replace("{{CHECKLIST}}", checklist)
