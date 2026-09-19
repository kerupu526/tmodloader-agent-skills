# Porting and update workflow

## 1. Freeze the baseline

- Copy or branch the source before changing it.
- Record the old loader lane, mod version, save-data expectations, and the
  first clean build/log result.
- List the feature families present: content classes, global classes, world
  state, custom UI, packets, assets, localization, configs, and commands.

## 2. Apply the official migration map

Read the relevant sections of the official migration pages for the exact
source and destination. Typical 1.3-to-1.4 work includes moving world-global
behavior into `ModSystem`, adapting old loading/autoload patterns, updating
entity sources and hooks, and converting old loot/recipe/network patterns.
These are families of changes, not a license to replace every occurrence by
search-and-replace.

For each compiler error, record:

```text
old API or behavior:
destination API or behavior:
why the replacement preserves intent:
side/authority impact:
save/network/localization impact:
```

## 3. Convert in dependency order

1. Build metadata and generated source layout.
2. Namespaces, type names, using directives, and obvious signature changes.
3. Registration/autoload and content classes.
4. Recipes, loot, spawning, and cross-content references.
5. `ModSystem`, `ModPlayer`, global types, and lifecycle resets.
6. Network ownership, packet formats, `NetSend`/`NetReceive`, and entity
   synchronization.
7. UI, rendering, assets, and client-only guards.
8. Localization and generated language-file updates.
9. Save-data compatibility and release metadata.

Rebuild after each meaningful family. Do not fix ten unrelated errors at once
and then guess which change caused a runtime regression.

## 4. Compatibility passes

### Saved data

Compare `SaveData`/`LoadData` and `SaveWorldData`/`LoadWorldData` keys and
defaults. Reset world/player state in the correct lifecycle when no prior tag
exists. Preserve old keys or write an intentional migration when changing a
type or meaning.

### Multiplayer

Confirm who creates entities, who owns projectile AI, which side runs each
hook, and whether a changed field is sent to new and existing clients. Compile
success is irrelevant if clients disagree about state.

### Localization and assets

Keep the English HJSON source complete, update other language files according
to the current loader behavior, and verify asset paths/casing. Regenerated
localization output should be reviewed separately from handwritten changes.

### Runtime regression

Test a new world, an old representative world, a fresh character, an existing
character, single-player, and a dedicated-server session when the mod has
state or networking. Test content that was changed, not only that the title
screen loads.
