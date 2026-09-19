# Tiles, walls, and tile entities

## Tile checklist

Read [Basic Tile](https://github.com/tModLoader/tModLoader/wiki/Basic-Tile),
[Basic Tile Entity](https://github.com/tModLoader/tModLoader/wiki/Basic-Tile-Entity),
and the current [ModTile API](https://docs.tmodloader.net/docs/stable/class_mod_tile.html).
For a new tile, account for:

- source/texture and matching placeable item;
- static sets, map entry, dust, sound, mining, pickaxe/power, and drops;
- dimensions, `TileObjectData`, anchoring, frame important, slopes, collision,
  actuators, wires, liquids, and smart cursor if relevant;
- `NearbyEffects`, mouse interaction, right-click/use, and tile kill hooks;
- tile square/frame synchronization after server-side changes;
- localization for display name/map entry and any UI text.

For walls, use the current wall API and verify wall item/drop behavior, map
color, merge/frame rules, and the exact texture path.

## Multitiles

Treat a multitile as a coordinate transform problem:

1. Determine the tile's top-left coordinate from the frame data.
2. Verify the tile type and frame before using it.
3. Place/remove the complete object through the documented `TileObjectData`
   and placement hooks.
4. Store the entity at the intended anchor and use the same anchor in UI,
   persistence, and network code.
5. Break/kill the entity when the tile is removed and handle failed placement.

Use ExampleMod furniture/chest examples for the target branch. Do not copy a
1.3 `ModTile`/`TE` pattern into 1.4.x.

## Tile entities

The current [ModTileEntity API](https://docs.tmodloader.net/docs/stable/class_mod_tile_entity.html)
separates:

- `IsTileValidForEntity` — whether an entity may remain at coordinates;
- `SaveData`/`LoadData` — persistent data;
- `NetSend`/`NetReceive` — server-to-client entity state;
- update hooks — simulation, normally server/single-player;
- inventory/UI hooks — interaction and client presentation.

Initialize inventories and fields defensively. A received entity may be created
on a client before its final ID is assigned, so use position/type validation
and do not assume an ID is ready during `NetReceive`.

## Testing

Test a tile in a new world and an existing world, at all orientations/frames,
with tools, actuators, wires, liquids, multiplayer placement/removal, and a
server restart. Verify tile entity inventories are not duplicated or lost and
that a client cannot perform an unvalidated server mutation.
