---
name: tmodloader-localization
description: Author, migrate, and QA tModLoader HJSON localization, generated content keys, tooltips, UI text, and translations across supported languages.
---

# tModLoader localization

## When to use

Use this skill for `.hjson` files, `DisplayName`, `Tooltip`, UI/dialogue text,
generated localization entries, translation files, language fallback, and
localization regressions in a tModLoader mod.

Use the owning content skill for gameplay code and `tmodloader-ui-client` for
layout/drawing. Localization is a cross-cutting completion pass whenever new
content or visible UI is added.

## Workflow

1. Confirm the version lane and inspect the mod's existing localization layout.
   Do not impose a new file naming convention on a working mod without a
   migration reason.
2. Build/reload or inspect the generated English entries for the target lane so
   the exact key shape is known. Use explicit keys for custom text and stable
   references for shared/common strings.
3. Keep the English/default file complete and UTF-8 encoded. Add or update
   translated files using the loader's current fallback/autopopulation behavior.
4. Preserve HJSON structure, quoting, multiline delimiters, placeholders, and
   inline item/tooltip tags. Do not “fix” a translator's punctuation by
   changing a key or placeholder.
5. Review copy for gender/plural/grammar context, text expansion, UI width,
   accessibility, and language fallback. Run the [localization QA script]
   when checking a directory of HJSON files; it is intentionally a lightweight
   structural check, not a full HJSON parser.
6. Switch languages in-game and build/reload. Verify item names, tooltips,
   bestiary/spawn text, NPC dialogue, config labels, UI, chat, and error paths.

## Non-obvious invariants

- The generated entry is evidence of the current key shape; a guessed key that
  looks plausible can silently fall back to the key or English.
- Localization data and gameplay data are separate. Never parse localized text
  to drive game logic.
- Keep format placeholders exactly aligned with the code that supplies them.
- HJSON is not ordinary JSON: comments, unquoted values, multiline strings,
  and nested keys require HJSON-aware handling.
- A language file that contains a key but an empty/incorrect value can mask the
  English fallback, so review visible output rather than only key presence.
- Generated localization files may be updated on build/reload. Separate those
  changes from intentional copy edits in reviews.

## References

- Read [hjson-workflow.md](references/hjson-workflow.md) for key layout,
  placeholders, and generated-file handling.
- Read [localization-qa.md](references/localization-qa.md) for checks and
  fallback/visual testing.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for the official wiki and
  ExampleMod links.

[localization QA script]: ../../scripts/check_localization_keys.py
