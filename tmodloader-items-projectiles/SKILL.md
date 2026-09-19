---
name: tmodloader-items-projectiles
description: Create, modify, review, or debug tModLoader items, weapons, ammo, accessories, prefixes, recipes, and projectiles in a version-matched Terraria mod.
---

# Items and projectiles

## When to use

Use this skill for `ModItem`, `GlobalItem`, weapons, tools, armor, accessories,
ammo, prefixes, recipes, `ModProjectile`, projectile AI, hitboxes, spawning,
ownership, projectile drawing, and item/projectile interactions.

Use `tmodloader-npcs-buffs` for NPCs or buffs, `tmodloader-world-tiles` for
tiles/world generation, and `tmodloader-networking` when the main problem is a
packet protocol or multiplayer desync. Bring in `tmodloader-localization` when
the change includes language files.

## Workflow

1. Identify the version lane and inspect adjacent ExampleMod content in the
   same branch.
2. Decide whether the behavior belongs to the item, its projectile, a player
   effect, or a global type. Keep item use configuration separate from
   projectile runtime state.
3. Implement the smallest content class and its required asset, localization,
   recipe/loot, and ownership pieces. Use `ModContent.*Type<T>()` or the
   current documented lookup for modded content; do not hard-code modded IDs.
4. For a projectile, specify the hitbox, friendly/hostile state, damage type,
   collision, lifetime, owner, and authority model before writing AI. Use
   vanilla AI/clone patterns as a prototype, then write or adapt current
   behavior when the projectile needs custom logic.
5. Check every spawn path for duplicate creation in multiplayer. Player-owned
   spawns normally originate on the owning client; NPC/server-owned spawns
   normally originate on the server. Confirm the exact hook and side in the
   API before applying a guard.
6. Test item use, cooldown/animation, ammo consumption, projectile collision,
   tile collision, item/projectile visuals, and single-player plus multiplayer
   when state is not purely local.

## Non-obvious invariants

- `CanUseItem` is a permission query; do not consume resources or mutate
  gameplay state there because the item may not actually be used.
- A `Type` is a content kind; a `whoAmI` or array slot is an active instance.
- `Main.myPlayer` is the local player index, not an NPC or projectile owner in
  every context. Use the actual owner/entity rules for the spawn source.
- A projectile that reads local mouse input or changes its velocity must be
  authoritative for its owner and mark the relevant state for synchronization.
- `SetStaticDefaults` is for type-wide metadata such as frames/sets; per-item
  and per-projectile gameplay defaults belong in the proper defaults phase.
- `Item.CloneDefaults`/`Projectile.CloneDefaults` copy a vanilla starting
  point, not a promise that all current behavior is preserved. Recheck fields,
  hooks, damage type, and ownership after cloning.
- Draw hooks are client-side concerns. Avoid loading textures or accessing
  graphics state on a dedicated server.

## References

- Read [items.md](references/items.md) for the item/weapon/recipe checklist.
- Read [projectiles.md](references/projectiles.md) for AI, ownership, collision,
  spawning, and drawing guidance.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for versioned API and ExampleMod
  links.
