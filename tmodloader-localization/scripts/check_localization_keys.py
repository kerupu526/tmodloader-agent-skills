"""Conservative HJSON localization checker.

It deliberately does not claim to parse all HJSON. It checks UTF-8 decoding,
obvious key paths, and printf-style placeholders without requiring a third
party dependency. Use tModLoader's build/reload or an HJSON parser for the
authoritative syntax check.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


KEY_RE = re.compile(r'^\s*(?:"([^"]+)"|([A-Za-z0-9_.-]+))\s*:\s*(.*?)\s*$')
PLACEHOLDER_RE = re.compile(r"\{(\d+)(?:,[^}]*)?(?::[^}]*)?\}")
MULTILINE = "'''"
# tModLoader mirrors untranslated entries into other language files as
# "// Key: English text". They fall back to English and must not count as
# missing. Only "//" is used for these; "#" lines are prose comments.
COMMENTED_KEY_RE = re.compile(r"^\s*//\s*(?:\"([^\"]+)\"|([A-Za-z0-9_.-]+))\s*:")
BLOCK_COMMENTED_KEY_RE = re.compile(r"^/\*\s*(?:\"([^\"]+)\"|([A-Za-z0-9_.-]+))\s*:")


def strip_comment(line: str) -> str:
    if line.lstrip().startswith(("#", "//")):
        return ""
    # This intentionally handles only the common inline forms. It avoids
    # interpreting a URL or a quoted // as a comment in the normal cases.
    in_quote = False
    escaped = False
    for index, char in enumerate(line):
        if char == '"' and not escaped:
            in_quote = not in_quote
        if not in_quote and line[index:index + 2] == "//":
            return line[:index]
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return line


def placeholders(text: str) -> tuple[str, ...]:
    return tuple(PLACEHOLDER_RE.findall(text))


def extract(path: Path) -> tuple[set[str], dict[str, tuple[str, ...]], set[str]]:
    """Return (live keys, placeholders per live key, commented-out keys)."""
    text = path.read_text(encoding="utf-8")
    stack: list[str] = []
    keys: set[str] = set()
    commented: set[str] = set()
    values: dict[str, tuple[str, ...]] = {}
    multiline_key: str | None = None
    multiline_parts: list[str] = []
    # A key with nothing after the colon: the multiline block may open on the
    # next non-blank line, which is the usual layout for tooltips/dialogue.
    pending_key: str | None = None
    in_block_comment = False

    def open_multiline(key: str, rest: str) -> None:
        nonlocal multiline_key, multiline_parts
        if MULTILINE in rest:
            values[key] = placeholders(rest.partition(MULTILINE)[0])
            multiline_key = None
            multiline_parts = []
        else:
            multiline_key = key
            multiline_parts = [rest]

    for raw in text.splitlines():
        if multiline_key is not None:
            # Inside a multiline block everything is text: no comments, no keys.
            if MULTILINE in raw:
                multiline_parts.append(raw.partition(MULTILINE)[0])
                values[multiline_key] = placeholders("\n".join(multiline_parts))
                multiline_key = None
                multiline_parts = []
            else:
                multiline_parts.append(raw)
            continue
        if in_block_comment:
            in_block_comment = "*/" not in raw
            continue
        commented_match = COMMENTED_KEY_RE.match(raw)
        if commented_match:
            name = commented_match.group(1) or commented_match.group(2)
            commented.add(".".join([*stack, name]))
        line = strip_comment(raw).strip()
        if pending_key is not None:
            if not line:
                continue
            key, pending_key = pending_key, None
            if line.startswith(MULTILINE):
                open_multiline(key, line[len(MULTILINE):])
                continue
        if line.startswith("/*"):
            # A block comment can hold a whole commented-out entry, for example
            # "/* Usage:" followed by a ''' block. Skip its body entirely.
            block_match = BLOCK_COMMENTED_KEY_RE.match(line)
            if block_match:
                name = block_match.group(1) or block_match.group(2)
                commented.add(".".join([*stack, name]))
            in_block_comment = "*/" not in line[2:]
            continue
        if not line:
            continue
        closing = 0
        while line.startswith("}"):
            closing += 1
            line = line[1:].lstrip(" ,")
        for _ in range(closing):
            if stack:
                stack.pop()
        match = KEY_RE.match(line)
        if not match:
            continue
        key = match.group(1) or match.group(2)
        value = match.group(3).rstrip(",")
        path_key = ".".join([*stack, key])
        keys.add(path_key)
        values[path_key] = placeholders(value)
        if value.startswith(MULTILINE):
            open_multiline(path_key, value[len(MULTILINE):])
        elif value == "":
            pending_key = path_key
        elif value.endswith("{"):
            stack.append(key)
    return keys, values, commented


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("english", type=Path, help="default/English HJSON file")
    parser.add_argument("languages", nargs="*", type=Path, help="other HJSON files")
    args = parser.parse_args()

    english_keys, english_values, _english_commented = extract(args.english)
    errors: list[str] = []
    notes: list[str] = []
    for path in args.languages:
        try:
            keys, values, commented = extract(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: not valid UTF-8 ({exc})")
            continue
        untranslated = (english_keys - keys) & commented
        if untranslated:
            notes.append(
                f"{path}: {len(untranslated)} keys are only present as commented "
                f"(untranslated, English fallback) entries"
            )
        missing = sorted(english_keys - keys - commented)
        if missing:
            errors.append(f"{path}: missing {len(missing)} obvious keys; first: {missing[0]}")
        for key in sorted(english_keys & keys):
            # Translations may reorder placeholders, but must keep the same set.
            if sorted(english_values.get(key, ())) != sorted(values.get(key, ())):
                errors.append(f"{path}: placeholder mismatch at {key}")

    for note in notes:
        print(f"NOTE: {note}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: checked {len(english_keys)} obvious keys in {args.english}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
