"""Validate the on-disk structure of the tModLoader skill suite.

This intentionally checks observable invariants rather than trying to prove
that prose is correct. It uses only the Python standard library so it can run
in a fresh Codex environment.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDERS = ("TODO", "<your", "{your", "lorem ipsum")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: frontmatter must start with ---")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path}: frontmatter must close with ---")
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match or not description_match:
        fail(f"{path}: frontmatter needs name and description")
    name = name_match.group(1).strip().strip('"\'')
    description = description_match.group(1).strip().strip('"\'')
    if not NAME_RE.fullmatch(name):
        fail(f"{path}: invalid skill name {name!r}")
    if not description:
        fail(f"{path}: empty description")
    if any(token.lower() in text.lower() for token in PLACEHOLDERS):
        fail(f"{path}: unfinished placeholder text found")
    return name, text


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        fail(f"suite directory does not exist: {root}")

    skill_files = sorted(root.glob("*/SKILL.md"))
    if len(skill_files) < 2:
        fail("expected a router plus at least one specialist SKILL.md")

    names: set[str] = set()
    for skill_file in skill_files:
        folder_name = skill_file.parent.name
        if not NAME_RE.fullmatch(folder_name):
            fail(f"invalid skill folder name: {folder_name}")
        skill_name, text = parse_frontmatter(skill_file)
        if skill_name != folder_name:
            fail(f"{skill_file}: frontmatter name {skill_name!r} != folder {folder_name!r}")
        if skill_name in names:
            fail(f"duplicate skill name: {skill_name}")
        names.add(skill_name)

        for reference in re.findall(r"\]\((references/[^)]+)\)", text):
            target = skill_file.parent / reference
            if not target.is_file():
                fail(f"{skill_file}: missing linked reference {reference}")

        if "## When to use" not in text:
            fail(f"{skill_file}: missing a When to use section")

    if not (root / "SOURCE-MAP.md").is_file():
        fail("missing SOURCE-MAP.md")
    if not (root / "scripts" / "validate_suite.py").is_file():
        fail("missing validator script")

    print(f"OK: {len(skill_files)} skills validated under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
