# tModLoader Agent Skills

An open Codex Agent Skill collection for developing Terraria mods with
[tModLoader](https://github.com/tModLoader/tModLoader).

This project is intentionally not one enormous skill. It uses a small router
skill plus focused specialist skills, so a task about projectile ownership does
not need to load every world-generation, UI, and localization procedure.

## What it supports

- Terraria/tModLoader project and version-lane detection
- item, weapon, ammo, accessory, prefix, recipe, and projectile work
- NPCs, bosses, town NPCs, spawning, drops, buffs, and debuffs
- `ModPlayer`, global types, `ModSystem`, configs, commands, and persistence
- tiles, walls, multitiles, tile entities, biomes, and world generation
- client UI, interface layers, keybinds, assets, sounds, shaders, and draw code
- multiplayer authority, `ModPacket`, entity sync, and desync investigation
- HJSON localization, generated keys, translations, and localization QA
- Build + Reload, IDE debugging, logs, dedicated-server checks, and regression QA

## Skill map

| Skill | Role |
| --- | --- |
| `tmodloader-modding` | Cross-cutting router, source hierarchy, side/lifecycle invariants, and specialist routing. |
| `tmodloader-versioning` | Stable/preview/legacy detection, porting, migration, and compatibility passes. |
| `tmodloader-items-projectiles` | `ModItem`, weapons, ammo, accessories, recipes, prefixes, `ModProjectile`, AI, collision, and ownership. |
| `tmodloader-npcs-buffs` | `ModNPC`, bosses, spawning, loot, `ModBuff`, debuffs, and global NPC behavior. |
| `tmodloader-player-systems` | `ModPlayer`, global types, `ModSystem`, configs, commands, save data, and lifecycle ownership. |
| `tmodloader-world-tiles` | `ModTile`, walls, multitiles, tile entities, biomes, world generation, and tile state. |
| `tmodloader-ui-client` | `UIState`, `UIElement`, interface layers, input, draw layers, and client-only assets. |
| `tmodloader-networking` | Authority, packet formats, player/world/entity synchronization, and multiplayer QA. |
| `tmodloader-localization` | HJSON structure, generated entries, placeholders, language fallback, and translation QA. |
| `tmodloader-debug-build-qa` | Build failures, runtime diagnostics, unload issues, server testing, and release evidence. |

Several skills can apply to one task. For example, a custom tile machine with a
screen may use `tmodloader-world-tiles`, `tmodloader-ui-client`,
`tmodloader-networking`, `tmodloader-localization`, and
`tmodloader-debug-build-qa` together. The router keeps the handoff between
those concerns explicit.

## Installation

Codex discovers user-level skills as sibling directories beneath
`~/.agents/skills/`. Copy the individual `tmodloader-*` directories there;
do not copy the outer repository directory as an additional nesting level.
Also copy the suite's shared `SOURCE-MAP.md` directly into the same skills
root. It is a companion provenance file, not an eleventh Skill.

Expected user-level layout:

```text
~/.agents/skills/
├── SOURCE-MAP.md
├── tmodloader-modding/
├── tmodloader-versioning/
├── tmodloader-items-projectiles/
├── tmodloader-npcs-buffs/
├── tmodloader-player-systems/
├── tmodloader-world-tiles/
├── tmodloader-ui-client/
├── tmodloader-networking/
├── tmodloader-localization/
└── tmodloader-debug-build-qa/
```

Each directory must contain `SKILL.md` directly beneath it.

### Windows PowerShell

From a clone or an extracted copy of this repository:

```powershell
$source = (Resolve-Path '.').Path
$destination = Join-Path $env:USERPROFILE '.agents\skills'
New-Item -ItemType Directory -Force $destination | Out-Null

$sourceMap = Join-Path $source 'SOURCE-MAP.md'
$sourceMapTarget = Join-Path $destination 'SOURCE-MAP.md'
if (Test-Path -LiteralPath $sourceMapTarget) {
  throw "Shared source map already exists: $sourceMapTarget. Compare it before replacing it."
}
Copy-Item -LiteralPath $sourceMap -Destination $sourceMapTarget

Get-ChildItem -LiteralPath $source -Directory |
  Where-Object { $_.Name -like 'tmodloader-*' } |
  ForEach-Object {
    $target = Join-Path $destination $_.Name
    if (Test-Path -LiteralPath $target) {
      throw "Skill already exists: $target. Compare it before replacing it."
    }
    Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse
  }
```

If a same-name directory already exists, compare its `SKILL.md` and
`references/` before deciding whether to merge, update, or keep the existing
version. The installation snippet deliberately stops instead of overwriting a
Skill silently.

### Project-specific installation

For a single mod repository, copy the same sibling directories under that
project's `.agents/skills/` directory. Project-local skills are useful when a
mod has conventions or APIs that should not affect unrelated projects.

User-level installation applies across projects. Project-local installation is
scoped to the project and can override or extend the context used for that
project. Keep the suite's folder names unchanged so automatic discovery remains
predictable.

## Example prompts

```text
Add a channelled spear to this 1.4.4 tModLoader mod. Inspect the current
project lane first, then implement the ModItem and ModProjectile with correct
owner checks, localization, and a two-client multiplayer test plan.
```

```text
Port this old ModWorld-based mod to the target tModLoader lane. Establish a
clean baseline, consult the matching migration guide, preserve world save
data, and report every unverified multiplayer or legacy-save case.
```

```text
Debug why this custom tile machine works in single-player but duplicates its
inventory in multiplayer. Trace tile-entity ownership, packet validation,
server relay, UI requests, and late-join behavior.
```

## Version awareness

The suite detects the version lane from project evidence instead of assuming a
permanent API version. Inspect the user's branch/commit, `build.txt`, `.csproj`,
launch settings, folder layout, installed runtime, and exact compiler/log
message before copying an example.

Keep stable, preview, and legacy API examples separate. Do not mix a preview or
`1.4.5` development signature into a stable project, and do not use 1.3 or
1.4.3 examples to justify a current 1.4.x implementation. The project may
choose a different lane than the current release, so the selected lane and its
evidence should be stated in the work.

## Sources of truth

The priority order is:

1. the current project's compiling code and conventions;
2. the version-matching official tModLoader API reference;
3. the same-branch official ExampleMod source;
4. the official tModLoader wiki and migration material;
5. tModLoader source, patches, and tests;
6. community examples as leads that must be verified against the sources above.

The complete source map, version snapshot, and links are maintained in
[`SOURCE-MAP.md`](SOURCE-MAP.md).

## Multiplayer and netcode principles

- Identify the authoritative side before spawning or mutating state.
- Treat client packets as requests, not proof of permission.
- Validate sender, entity type/index, coordinates, ranges, enum values, and
  current world/player state on the server.
- Keep packet read/write order stable and use an explicit discriminator/version
  for custom protocols.
- Distinguish persistence from replication: save hooks do not automatically
  synchronize live multiplayer state.
- Test a dedicated server, two clients, late join, owner disconnect, and
  repeated requests when the feature has shared state.

## Localization

Visible content should include the English/default HJSON entries, translated
files where supported, exact format placeholders, and UI-width checks. HJSON
is not ordinary JSON: preserve multiline syntax, comments, nested keys, tags,
and UTF-8 encoding. Use the localization specialist for key and fallback work.

## Validation

Run from the repository root:

```powershell
python scripts/validate_suite.py .
python -m py_compile scripts/validate_suite.py scripts/check_localization_keys.py
```

The suite validator checks frontmatter, naming, required sections, linked
references, and unfinished scaffold text. The localization checker performs a
conservative UTF-8/key/placeholder check; use an HJSON-aware parser and an
actual tModLoader Build + Reload for authoritative syntax and runtime
validation.

## Contributing

Keep specialist boundaries narrow and prefer progressive disclosure: shared
routing belongs in `tmodloader-modding`, version rules belong in
`tmodloader-versioning`, and mode-specific detail belongs in the relevant
`references/` file. When changing a source claim, update `SOURCE-MAP.md` or the
relevant reference link. Run the validation commands before opening a pull
request, and explain any runtime or version lane that was not tested.

## License

This collection is released under the MIT License. The repository contains
original Skill instructions, summaries, checklists, and links; it does not
redistribute a verbatim copy of tModLoader documentation or ExampleMod source.
