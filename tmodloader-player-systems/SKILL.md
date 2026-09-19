---
name: tmodloader-player-systems
description: Design and implement tModLoader ModPlayer, GlobalItem/GlobalNPC/GlobalProjectile, ModSystem, configs, commands, recipes, and persistent player/world state.
---

# Players and systems

## When to use

Use this skill when behavior is shared across content or belongs to a player,
world, or mod lifecycle: `ModPlayer`, global types, `ModSystem`, configs,
commands, conditions, recipes, cross-mod integration, saved data, and world or
player progression flags.

Use `tmodloader-items-projectiles`, `tmodloader-npcs-buffs`, or
`tmodloader-world-tiles` for a content-first change, but consult this skill
when that content needs persistent/shared state. Use `tmodloader-networking`
for packet protocol details.

## Workflow

1. Decide the owner and lifetime of each value: item instance, projectile/NPC
   instance, player, world, mod process, or configuration.
2. Prefer the narrowest type. Use `ModPlayer` for per-player state and player
   hooks, `ModSystem` for world/mod lifecycle and shared systems, and
   `Global*` types only when the behavior really applies to many existing
   vanilla or modded instances.
3. Define initialization and reset paths before writing update hooks. A save
   tag may be absent for a new entity/world, and the same process may load
   multiple worlds or characters.
4. Separate saved state from network state. Choose `SaveData`/`LoadData` or
   `SaveWorldData`/`LoadWorldData` for persistence; choose the appropriate
   player/entity/world sync mechanism for replication.
5. Keep per-tick hooks cheap. Avoid repeated allocations, full-world scans,
   asset requests, and global mutable static state unless the API explicitly
   requires them.
6. Validate a fresh world/character, existing save data, multiplayer join,
   unload/reload, config changes, and command permission/error paths.

## Non-obvious invariants

- `ModSystem` replaces many old world/global responsibilities from legacy
  tModLoader, but the correct hook still depends on the target lane.
- `LoadData` may not run when no data was saved. Initialize defaults in the
  normal lifecycle (`Initialize`, `OnWorldLoad`, `ClearWorld`, or the lane's
  equivalent) as appropriate.
- Do not retain a `TagCompound` object beyond the save/load call. Persist the
  values, not the transient container.
- Save only non-default data where possible, especially in `GlobalItem`, or
  player/world files can grow rapidly.
- A `Global*` class may be shared or cloned per entity depending on its API
  contract. Check the current documentation before storing mutable fields.
- Configuration is not a substitute for authoritative gameplay state. A
  client-accepted setting may need server validation and a distinct sync path.
- A command should validate sender, arguments, side, and permissions before
  mutating player/world state.

## References

- Read [ownership-lifecycle.md](references/ownership-lifecycle.md) for choosing
  `ModPlayer`, `ModSystem`, and global types.
- Read [persistence.md](references/persistence.md) for `TagCompound`, reset,
  compatibility, and saved-state checks.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for API and ExampleMod links.
