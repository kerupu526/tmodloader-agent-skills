# HJSON workflow

Read the official [Localization guide](https://github.com/tModLoader/tModLoader/wiki/Localization)
and inspect [ExampleMod localization](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod/Localization)
for the selected branch.

## Files and keys

- Follow the mod's current `Localization/` layout. Current ExampleMod keeps an
  English file plus language-specific files and separate config localization
  files.
- Keys are nested under the mod namespace, commonly beginning with `Mods` and
  the mod's internal name. Let tModLoader generate new content entries after a
  build/reload, then edit the generated values rather than guessing the path.
- Custom keys should be descriptive and stable. Use a shared/common section
  for repeated text and reference it through the documented localization
  syntax when appropriate.
- Keep key identity independent from prose. Renaming display text should not
  rename a key unless the code/API requires it.

## HJSON safety

- Preserve braces, indentation, comments, and nesting.
- Use quoted strings when punctuation, leading/trailing whitespace, or HJSON
  syntax could make an unquoted value ambiguous.
- Use the documented multiline delimiter for multi-line tooltips/dialogue;
  do not paste JSON escaping into an HJSON multiline value.
- Preserve `{0}`, `{1}`, and other format placeholders exactly. If the code
  changes the argument count, update every language with a translator note.
- Treat icon/item tags and color tags as syntax. Verify them in-game.
- Save as UTF-8 and avoid editor conversions that add a different encoding.

## Fallback and generated entries

The loader's current localization system can populate missing entries after a
build/reload. Non-English files may contain commented/untranslated entries that
fall back to English. Keep that behavior visible to translators; do not delete
generated keys merely because they are not yet translated.
