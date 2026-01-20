from typing import Self

from bs4 import BeautifulSoup, NavigableString, Tag


class Paragraphs:
    def __init__(self, paragraphs: list[str]) -> None:
        self.paragraphs = paragraphs

    @classmethod
    def create_with_title(cls, title: str) -> Self:
        return cls([title, ""])

    @classmethod
    def create_without_title(cls) -> Self:
        return cls([""])

    def add_br(self) -> None:
        if self.paragraphs[-1] != "":
            self.paragraphs.append("")

    def add_text(self, text: str) -> None:
        # This is required since Reddit likes to use \n for line breaks.
        text_chunk = text.split("\n")
        for i, line in enumerate(text_chunk):
            # An extra space may need to be added before appending more text
            if (
                line != ""
                and self.paragraphs[-1] != ""
                and not self.paragraphs[-1].endswith(" ")
            ):
                self.paragraphs[-1] += " "
            self.paragraphs[-1] += line
            if i < len(text_chunk) - 1:
                self.add_br()

    def to_string(self) -> str:
        paragraphs = [p.strip() for p in self.paragraphs if p.strip()]
        return "<br>".join(paragraphs)


def create(
    title: str,
    body_with_children: Tag | BeautifulSoup | None,
    *,
    is_reply: bool,
    only_use_br_as_line_break: bool,
) -> str:
    if body_with_children is None:
        return title

    if not is_reply:
        paragraphs = Paragraphs.create_with_title(title)
    else:
        paragraphs = Paragraphs.create_without_title()

    for element in body_with_children.children:
        assert isinstance(element, Tag | NavigableString)
        # "user said:" blockquotes are bloat information that are not
        # attributed to this author
        if hasattr(element, "name") and element.name == "blockquote":
            continue
        # every logical paragraph is separated by <br> in HardwareZone
        if hasattr(element, "name") and element.name == "br":
            paragraphs.add_br()
            continue
        if hasattr(element, "name") and element.name == "ul":
            for li in element.find_all("li"):
                paragraphs.add_text(f"- {li.get_text()}")
                paragraphs.add_br()
        elif hasattr(element, "get_text"):
            paragraphs.add_text(element.get_text())
        else:
            paragraphs.add_text(str(element))

        # Some sites solely rely on a br tag to separate logical chunks,
        # others treat a single <p> element, for instance, as a logical chunk
        if not only_use_br_as_line_break:
            paragraphs.add_br()

    return paragraphs.to_string()
