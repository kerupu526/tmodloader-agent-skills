---
name: tmodloader-modding
description: Route and perform cross-cutting Terraria tModLoader mod development, review, and troubleshooting when the request spans multiple systems or no narrower tModLoader skill is sufficient.
---

# tModLoader modding router

## When to use

Use this skill for a Terraria mod made with tModLoader when the request covers
project triage, several content systems, architecture, code review, or a task
whose exact specialist is not yet clear. It is also the entry point for
deciding which focused skill should own a change.

Do not use it for vanilla Terraria modding without tModLoader, Terraria server
administration without mod code, or a pure C# question with no tModLoader
behavior. Those tasks should stay in their more appropriate skill.

## Operating contract

1. Inspect the project before proposing code. Identify whether it is a
   generated `ModSources/<ModName>` source tree, a repository containing one,
   or the tModLoader source repository itself.
2. Detect the version lane before reading examples. Use the project metadata,
   branch, `.csproj`, `build.txt`, installed target framework, and any explicit
   user constraint together. Never mix 1.3, 1.4.3, 1.4.4 stable, and preview
   signatures just because their class names look similar.
3. Prefer the project's existing conventions and the matching official API
   page. Then consult the matching ExampleMod branch, official wiki, and only
   then a community example. The [source hierarchy](references/source-hierarchy.md)
   defines how to resolve disagreements.
4. Keep physical-client code, logical-client code, server simulation, and
   shared code distinct. Any change that can affect gameplay, saved state, or
   another player needs an explicit side and synchronization review.
5. Make the smallest coherent change. Add the source, asset, localization,
   persistence, and multiplayer pieces that the feature actually requires;
   do not create speculative framework code.
6. Validate with the strongest checks available: build/reload, targeted
   single-player behavior, dedicated-server behavior, and multiplayer behavior
   when networking or authority is involved. For a review-only request, report
   missing evidence rather than claiming runtime confidence.

## Specialist routing

Use the following focused skill when the request is mostly in one area. If the
task crosses boundaries, keep this router as the coordinator and apply each
specialist's checklist to the files it owns.

- Version detection, branches, 1.3/1.4.3/1.4.4/preview migration:
  `tmodloader-versioning`
- Items, weapons, ammo, recipes, prefixes, and projectiles:
  `tmodloader-items-projectiles`
- NPCs, bosses, spawning, drops, buffs, and debuffs:
  `tmodloader-npcs-buffs`
- ModPlayer, Global types, ModSystem, configs, commands, and saved state:
  `tmodloader-player-systems`
- Tiles, walls, tile entities, biomes, and world generation:
  `tmodloader-world-tiles`
- UI, interface layers, input, draw layers, assets, sounds, and client-only
  behavior: `tmodloader-ui-client`
- Netcode, packets, authority, entity sync, and multiplayer desync:
  `tmodloader-networking`
- HJSON, generated localization entries, language files, and translation QA:
  `tmodloader-localization`
- Build failures, debugging, logs, unload issues, regression checks, and QA:
  `tmodloader-debug-build-qa`

Read only the specialist reference files relevant to the current request. Do
not preload every reference in the suite.

## Shared invariants

- `Type` identifies a kind of content; `whoAmI`/an array index identifies an
  active instance. Never use one in place of the other.
- Content classes are normally autoloaded from their namespace and file/asset
  layout. Confirm the exact autoload convention for the lane before manually
  registering or loading something.
- A hook's return value and call side are part of its contract. Check the API
  documentation for whether it runs on the local client, remote clients,
  server, or all sides before adding side effects.
- `SetDefaults`/`SetStaticDefaults` are not interchangeable. Static ID sets,
  frame counts, and other type-wide metadata belong in the static phase; per
  instance gameplay values belong in defaults or the relevant runtime hook.
- Save data, network data, localization, and visual assets have different
  lifecycles. Do not use one as a substitute for another.
- When adapting vanilla behavior, find the current vanilla implementation and
  current ExampleMod analogue first. A copied 1.3 snippet is not evidence for
  current 1.4.x behavior.

## References

- Read [routing.md](references/routing.md) when the task spans two or more
  specialist areas or the ownership of a hook is unclear.
- Read [source-hierarchy.md](references/source-hierarchy.md) whenever a wiki,
  ExampleMod branch, API page, and community snippet disagree.
- The suite-wide provenance map is at `../SOURCE-MAP.md`.
