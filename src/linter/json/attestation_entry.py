from pydantic import BaseModel

from src.linter.json import specs


class T(BaseModel):
    eg: str
    src: str | None = None


def get_linked_words(t: T) -> list[str]:
    return specs.get_linked_words(t.eg)
