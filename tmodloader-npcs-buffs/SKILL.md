---
name: tmodloader-npcs-buffs
description: Build, balance, review, and debug tModLoader NPCs, bosses, town NPCs, spawning, loot, buffs, debuffs, and global NPC behavior.
---

# NPCs and buffs

## When to use

Use this skill for `ModNPC`, `GlobalNPC`, boss AI, town NPCs, critters,
spawning, bestiary data, shops, drops/loot, `ModBuff`, `GlobalBuff`, debuffs,
immunity, and NPC/projectile/player combat interactions.

Use `tmodloader-items-projectiles` for a weapon/projectile-first task,
`tmodloader-world-tiles` for world generation or tile mechanics, and
`tmodloader-networking` when synchronization is the central problem.

## Workflow

1. Identify the version lane and find a current ExampleMod NPC or buff with a
   similar lifecycle. A boss, town NPC, spawn rule, and debuff have different
   responsibilities; do not start from a giant class template.
2. Separate static identity/setup, per-instance defaults, AI/state transitions,
   target selection, combat hooks, loot, spawning, visuals, and persistence.
3. For NPC AI, define a small state machine and timers. Make target changes,
   projectile spawns, and world-state transitions explicit about authority.
4. For spawn chances, return the correct neutral value for the context and
   check biome, depth, events, invasion, town/NPC exclusions, and player
   conditions without accidentally increasing unrelated spawn rates.
5. Use the current item-drop-rule API for loot. Separate normal, expert,
   master, boss-bag, per-player, and conditional drops deliberately.
6. For buffs/debuffs, decide whether the effect is player-owned, NPC-owned,
   global, visual, or gameplay state. Keep reset/expiration behavior explicit.
7. Test manually spawned and naturally spawned NPCs, target changes, death and
   loot, multiplayer authority, boss progression, and clean unload.

## Non-obvious invariants

- NPC `whoAmI` is an active instance index; `NPC.type` is the content kind.
- An NPC-spawned projectile is usually server-authoritative. A player-owned
  projectile spawned by an item follows a different ownership rule.
- A spawn hook's return value is not a generic “spawn now” flag. Confirm the
  expected chance/neutral value and context in the version-matched API.
- Per-NPC mutable values belong on the `ModNPC` instance or an appropriately
  cloned `GlobalNPC`; static fields are shared across all instances.
- A world progression flag such as “boss defeated” belongs in a world system,
  not in a single NPC instance. Coordinate with `tmodloader-player-systems`.
- Buff `Update` logic must be safe to run each tick and should reset or derive
  transient effects rather than accumulating them unintentionally.
- Dedicated servers must not load or execute rendering-only NPC/buff code.

## References

- Read [npcs-buffs.md](references/npcs-buffs.md) for NPC and buff lifecycle
  patterns.
- Read [spawning-loot.md](references/spawning-loot.md) for spawn and drop
  checklists.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for API and ExampleMod links.
