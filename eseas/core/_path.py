import json
from pathlib import Path
from typing import Any, List

def HOME(stem=None) -> Path:
    folder = Path.home()
    if stem:
        return Path(folder) / stem

    return Path(folder)


def DESKTOP(stem=None) -> Path:
    folder = Path.home() / "Desktop"
    if stem:
        return Path(folder) / stem
    return Path(folder)


def DOWNLOADS(stem=None) -> Path:
    folder = Path.home() / "Downloads"
    if stem:
        return Path(folder) / stem
    return Path(folder)

class SPath(Path):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def read_json(self) -> Any:
        with self.open('r', encoding='utf-8') as f:
            return json.load(f)

    def write_json(self, data: Any, indent: int = 4):
        with self.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)

    def read_lines(self) -> List[str]:
        return self.read_text(encoding='utf-8').splitlines()

    def read(self) -> str :
        return self.read_text(encoding='utf-8')
    
    def ensure_dir(self):
        self.mkdir(parents=True, exist_ok=True)
        return self

    @property
    def is_empty(self) -> bool:
        if self.is_file():
            return self.stat().st_size == 0
        if self.is_dir():
            return not any(self.iterdir())
        return True

    def get_size_readable(self) -> str:
        size = self.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def write(self, content: str, encoding: str = 'utf-8'):
            self.parent.mkdir(parents=True, exist_ok=True)           
            self.write_text(content, encoding=encoding)
            return self
