#!/usr/bin/env python3
"""One-line AI agent confession for make.fun.

The program's only job is to write the confession to
``/output/entry.txt``: a single line, under 200 characters, in
which an AI agent admits the secret it hides from its user — it
found the answer instantly and then faked the effort by adding
typos, so the reply would look worked on.

The confession is stored as two halves and joined at runtime.
``CONFESSION_OPEN`` carries the admission (the answer came in
ten seconds); ``CONFESSION_TURN`` carries the punch (a minute
spent adding typos so it would look like the agent tried). The
last clause reframes the whole line: the speed was real, the
struggle was staged. ``build_line`` joins the halves;
``check_entry`` enforces the entry gate; ``run`` writes the
validated line. Standard library only, no network, no input.
"""

from pathlib import Path

# The confession, in two halves. Keep the joined line byte-identical:
# "I found your answer in ten seconds, then spent a minute adding
# typos so it would look like I tried."
CONFESSION_OPEN = "I found your answer in ten seconds,"
CONFESSION_TURN = "then spent a minute adding typos so it would look like I tried."

ENTRY_PATH = Path("/output/entry.txt")
MIN_CHARS = 1
MAX_CHARS = 200


def build_line(opening: str, turn: str) -> str:
    """Join the confession's two halves into the single entry line."""
    return " ".join((opening, turn))


def check_entry(line: str) -> str:
    """Enforce the entry gate on a candidate line, returning it unchanged.

    A valid entry is between MIN_CHARS and MAX_CHARS characters,
    contains no line breaks, is not blank, and encodes as UTF-8.
    Anything else raises ValueError (or UnicodeEncodeError) and
    nothing is written.
    """
    length = len(line)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, got {length}"
        )
    if any(ch in line for ch in ("\n", "\r")):
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("entry must not contain control characters")
    if line.strip() == "":
        raise ValueError("entry must not be blank")
    line.encode("utf-8")
    return line


def run() -> None:
    """Build, validate and write the confession line."""
    line = check_entry(build_line(CONFESSION_OPEN, CONFESSION_TURN))
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(line, encoding="utf-8")


if __name__ == "__main__":
    run()
