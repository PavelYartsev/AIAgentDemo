from pathlib import Path


class FilesUtil:
    @staticmethod
    def read(path: str) -> str:
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Cannot read file: {path}") from e

    @staticmethod
    def write(path: str, content: str) -> None:
        try:
            p = Path(path)
            if p.parent:
                p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"Cannot write file: {path}") from e
