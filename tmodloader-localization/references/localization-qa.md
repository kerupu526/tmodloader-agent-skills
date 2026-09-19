# Localization QA

## Structural checks

For each language file:

- UTF-8 decoding succeeds;
- the HJSON file is parseable by an HJSON-aware parser when one is available;
- the English/default key set remains complete;
- translated files do not introduce accidental unrelated top-level namespaces;
- format placeholders match the English/source value;
- icon, item, color, and custom markup tags are balanced enough to render;
- no key is duplicated through two conflicting nesting paths.

The bundled checker performs conservative key and placeholder checks without
pretending to be a full HJSON parser. Use the game/build to validate semantics.

## Runtime checks

Switch through every language supported by the mod and inspect:

- item names/tooltips and recipe text;
- NPC names, dialogue, spawn/bestiary text, and loot messages;
- buffs/debuffs and system notifications;
- config labels/descriptions;
- custom UI at normal and small widths;
- chat/command errors and multiplayer messages.

Check long German/Russian/Portuguese/Japanese/Korean-style expansion and
missing-glyph fallback if those languages are supported. Never assume English
width or word boundaries.

## Review language changes

Separate generated key additions, translation changes, and code key changes in
the review. Record whether a missing translation is intentionally falling back
to English or is a release blocker.
