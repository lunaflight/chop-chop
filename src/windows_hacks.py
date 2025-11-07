import io
import os
import sys

AM_WINDOWS = os.name == "nt"


# This is required to align behaviour to be similar to
# Linux for program reliability
def set_stdin_stdout_encoding_if_windows() -> None:
    if AM_WINDOWS:
        sys.stdin = io.TextIOWrapper(
            sys.stdin.buffer, encoding="utf-8", errors="replace"
        )
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
