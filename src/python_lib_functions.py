from typing import TypeVar

T = TypeVar("T")


def find_duplicate(input_list: list[T]) -> T | None:
    """
    Find the first duplicate element in a list.

    Args:
        input_list: A list of hashable elements to search for duplicates.
            The element type ``T`` should not be ``None``. This cannot
            currently be enforced statically. See
            `python/typing#801 <https://github.com/python/typing/issues/801>`_.

    Returns:
        The first duplicate element found, or ``None`` if no duplicates exist.
        ``None`` does not indicate a duplicated ``None`` value due to the input
        constraint.

    Raises:
        TypeError: If any element in ``input_list`` is ``None``.

    """
    seen = set()
    for item in input_list:
        if item is None:
            raise TypeError("T should not be None")
        if item in seen:
            return item
        seen.add(item)
    return None
