---
name: tmodloader-world-tiles
description: Create and debug tModLoader tiles, walls, multitiles, tile entities, biomes, world generation, world data, and tile-related networking.
---

# World and tiles

## When to use

Use this skill for `ModTile`, `ModWall`, `ModTileEntity`, furniture,
multitiles, chests, wiring, tile interaction, biome detection, world
generation passes, post-generation edits, world flags, and tile synchronization.

Use `tmodloader-player-systems` for durable world flags and lifecycle ownership,
`tmodloader-ui-client` for a custom inventory/interaction UI, and
`tmodloader-networking` when the main issue is a custom packet or desync.

## Workflow

1. Identify whether the feature is a tile type, wall, multitile, tile entity,
   world-generation pass, biome query, or world state. These are related but
   have different lifecycles.
2. Inspect current [ModTile](https://docs.tmodloader.net/docs/stable/class_mod_tile.html),
   [ModTileEntity](https://docs.tmodloader.net/docs/stable/class_mod_tile_entity.html),
   and matching ExampleMod furniture/world examples before selecting hooks.
3. Define tile dimensions, frames, anchoring, collision, slopes, map entry,
   dust/sound, drop/item link, placement/removal, wiring, and multiplayer
   update behavior. For multitiles, verify the top-left coordinate and
   placement hook rather than guessing from the visible sprite.
4. For a tile entity, separate tile validity from entity data, persistence,
   inventory/UI, update side, and `NetSend`/`NetReceive` behavior.
5. For world generation, find a stable insertion point by name and guard the
   pass against changed or missing vanilla passes. Make generation deterministic
   enough to test and avoid writing client-only code in a server generation
   hook.
6. Test placement, mining, drops, frames, wiring, liquids, slopes, reload,
   world save/load, new-world generation, and multiplayer tile/entity state.

## Non-obvious invariants

- World-generation code runs before normal gameplay. It is not a replacement
  for an in-world update hook.
- `ModifyWorldGenTasks` changes the generation pass list; do not insert by a
  fragile integer index without checking the current pass names/order.
- `ModTileEntity.Hook_AfterPlacement` is a convenience pattern and is not
  automatically called by tModLoader; the placement hook must call the intended
  helper according to the current API.
- A tile entity's `Update` is server/single-player simulation, not a client
  render loop. Client visual/UI code needs a separate path.
- Tile changes and tile-entity data have distinct synchronization mechanisms.
  Sync the tile square/frames and entity data as required; one does not imply
  the other.
- Never assume a multitile coordinate is the clicked coordinate. Resolve the
  top-left tile and validate tile type/frame before reading entity state.

## References

- Read [tiles-and-entities.md](references/tiles-and-entities.md) for tile,
  multitile, wall, and tile-entity implementation.
- Read [world-generation.md](references/world-generation.md) for generation,
  biome, and world-state checks.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for API and wiki links.
