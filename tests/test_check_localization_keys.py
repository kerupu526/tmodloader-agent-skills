"""Regression tests for the localization checker.

Run from the repository root:  python -m unittest discover -s tests
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tmodloader-localization" / "scripts" / "check_localization_keys.py"

ENGLISH = """\
Mods: {
	MyMod: {
		Items: {
			Sword: {
				DisplayName: Cool Sword
				Tooltip:
					'''
					Deals {0} damage
					Warning: heals {1}
					'''
			}
			Bow: {
				DisplayName: "Bow // fancy"
				Tooltip: Shoots {0:N1} arrows, "range {1,5}"
			}
			Inline: {
				Tooltip: '''one line {0}'''
			}
		}
	}
}
"""

GOOD = """\
Mods: {
	MyMod: {
		Items: {
			Sword: {
				DisplayName: Sword
				Tooltip:
					'''
					{1} 회복
					경고: {0} 피해
					'''
			}
			Bow: {
				DisplayName: Bow
				Tooltip: range {1,5}, arrows {0:N1}
			}
			Inline: {
				Tooltip: '''한 줄 {0}'''
			}
		}
	}
}
"""


def run(english: str, *others: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        (base / "en.hjson").write_text(english, encoding="utf-8")
        names = []
        for index, text in enumerate(others):
            name = base / f"lang{index}.hjson"
            name.write_text(text, encoding="utf-8")
            names.append(str(name))
        return subprocess.run(
            [sys.executable, str(CHECKER), str(base / "en.hjson"), *names],
            capture_output=True,
            text=True,
        )


class LocalizationCheckerTests(unittest.TestCase):
    def test_matching_translation_passes(self) -> None:
        # Covers: multiline block opened on the next line, a "word:" inside the
        # block, reordered placeholders, and a same-line multiline value.
        result = run(ENGLISH, GOOD)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_placeholder_in_next_line_multiline_is_reported(self) -> None:
        bad = GOOD.replace("{1} 회복", "회복")
        result = run(ENGLISH, bad)
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder mismatch at Mods.MyMod.Items.Sword.Tooltip", result.stdout)

    def test_missing_placeholder_on_single_line_is_reported(self) -> None:
        bad = GOOD.replace("arrows {0:N1}", "arrows")
        result = run(ENGLISH, bad)
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder mismatch at Mods.MyMod.Items.Bow.Tooltip", result.stdout)

    def test_missing_key_is_reported(self) -> None:
        bad = GOOD.replace("DisplayName: Bow", "")
        result = run(ENGLISH, bad)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stdout)

    def test_colon_inside_multiline_text_is_not_a_key(self) -> None:
        result = run(ENGLISH, GOOD.replace("경고: ", "경고 "))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_commented_untranslated_entries_are_not_missing(self) -> None:
        # tModLoader mirrors untranslated entries as "// Key: text" and as a
        # "/* Key: ... */" block for multiline values; both fall back to English.
        english = (
            "Mods: {\n"
            "\tM: {\n"
            "\t\tA: Alpha {0}\n"
            "\t\tB: Beta\n"
            "\t\tCmd: {\n"
            "\t\t\tUsage:\n"
            "\t\t\t\t'''\n"
            "\t\t\t\t/cmd name: arg {0}\n"
            "\t\t\t\t'''\n"
            "\t\t}\n"
            "\t}\n"
            "}\n"
        )
        translated = (
            "Mods: {\n"
            "\tM: {\n"
            "\t\tA: 알파 {0}\n"
            "\t\t// B: Beta\n"
            "\t\tCmd: {\n"
            "\t\t\t/* Usage:\n"
            "\t\t\t\t'''\n"
            "\t\t\t\t/cmd name: arg {0}\n"
            "\t\t\t\t''' */\n"
            "\t\t}\n"
            "\t}\n"
            "}\n"
        )
        result = run(english, translated)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("NOTE:", result.stdout)

    def test_hash_prose_comment_does_not_hide_a_missing_key(self) -> None:
        english = "Mods: {\n\tM: {\n\t\tNote: Hello\n\t}\n}\n"
        translated = "Mods: {\n\tM: {\n\t\t# Note: translators read this\n\t}\n}\n"
        result = run(english, translated)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stdout)

    def test_repeated_placeholder_is_a_mismatch(self) -> None:
        english = "Mods: {\n\tM: {\n\t\tA: {0} and {0}\n\t}\n}\n"
        translated = "Mods: {\n\tM: {\n\t\tA: {0}\n\t}\n}\n"
        result = run(english, translated)
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
