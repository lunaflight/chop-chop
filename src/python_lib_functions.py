from typing import TypeVar

T = TypeVar("T")


def find_duplicate(input_list: list[T]) -> T | None:
    seen = set()
    for item in input_list:
        if item in seen:
            return item
        seen.add(item)
    return None
