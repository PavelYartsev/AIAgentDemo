from pathlib import Path
import shutil


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

    @staticmethod
    def create_dir_if_not_exists(path: str) -> None:
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Cannot create directory: {path}") from e

    @staticmethod
    def clear_directory_contents(path: str) -> None:
        try:
            p = Path(path)
            if p.is_dir():
                for item in p.iterdir():
                    if item.is_file():
                        item.unlink()
            else:
                raise ValueError(f"Path is not a directory: {path}")
        except Exception as e:
            raise RuntimeError(f"Cannot clear directory contents: {path}") from e

    @staticmethod
    def delete_dir_if_exists(path: str) -> None:
        try:
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(p)
        except Exception as e:
            raise RuntimeError(f"Cannot delete directory: {path}") from e
