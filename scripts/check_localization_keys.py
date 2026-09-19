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


def extract(path: Path) -> tuple[set[str], dict[str, tuple[str, ...]]]:
    text = path.read_text(encoding="utf-8")
    stack: list[str] = []
    keys: set[str] = set()
    values: dict[str, tuple[str, ...]] = {}
    multiline_key: str | None = None
    multiline_parts: list[str] = []
    for raw in text.splitlines():
        line = strip_comment(raw).strip()
        if multiline_key is not None:
            if "'''" in line:
                before, _separator, _after = line.partition("'''")
                multiline_parts.append(before)
                values[multiline_key] = tuple(
                    PLACEHOLDER_RE.findall("\n".join(multiline_parts))
                )
                multiline_key = None
                multiline_parts = []
            else:
                multiline_parts.append(line)
            continue
        if not line or line.startswith("/*"):
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
        values[path_key] = tuple(PLACEHOLDER_RE.findall(value))
        if value.startswith("'''"):
            multiline_key = path_key
            multiline_parts = [value[3:]]
            if "'''" in multiline_parts[0]:
                before, _separator, _after = multiline_parts[0].partition("'''")
                values[path_key] = tuple(PLACEHOLDER_RE.findall(before))
                multiline_key = None
                multiline_parts = []
            continue
        if value.endswith("{") or value == "{":
            stack.append(key)
    return keys, values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("english", type=Path, help="default/English HJSON file")
    parser.add_argument("languages", nargs="*", type=Path, help="other HJSON files")
    args = parser.parse_args()

    english_keys, english_values = extract(args.english)
    errors: list[str] = []
    for path in args.languages:
        try:
            keys, values = extract(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: not valid UTF-8 ({exc})")
            continue
        missing = sorted(english_keys - keys)
        if missing:
            errors.append(f"{path}: missing {len(missing)} obvious keys; first: {missing[0]}")
        for key in sorted(english_keys & keys):
            if english_values.get(key) != values.get(key):
                errors.append(f"{path}: placeholder mismatch at {key}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: checked {len(english_keys)} obvious keys in {args.english}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
