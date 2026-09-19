# World generation and biome guidance

## Generation hooks

Read [World Generation](https://github.com/tModLoader/tModLoader/wiki/World-Generation),
[vanilla world-generation steps](https://github.com/tModLoader/tModLoader/wiki/Vanilla-World-Generation-Steps),
and the current [ModSystem API](https://docs.tmodloader.net/docs/stable/class_mod_system.html).

- Use `ModifyWorldGenTasks` to add, remove, disable, or wrap generation passes.
- Choose an insertion point by a current pass name and add defensive fallback
  behavior if the pass is absent in the selected lane.
- Use `PostWorldGen` for post-generation edits that do not need to be an
  interleaved generation pass.
- Keep generation deterministic enough to reproduce failures and avoid relying
  on a client-only asset or UI object.
- Do not assume the world is fully populated at every pass. Follow the vanilla
  generation order and check bounds/tiles before writing.

## World flags and synchronization

Put progression booleans, counters, and generated-location metadata in a
`ModSystem` with a clear reset/load/save path. If clients need to know a flag
during play, use the world-data sync hooks or a packet; saving the flag does not
replicate it immediately.

## Biomes

Use a dedicated biome type/helper when the project needs a reusable condition.
Keep tile-count and player-zone checks cheap and cache/update them through the
documented lifecycle rather than scanning the entire world every frame. Define
what happens near boundaries, underground, in liquids, and when the relevant
tiles are actuated or replaced.

## Generation QA

- generate small/medium/large worlds;
- generate each evil/seed mode relevant to the feature;
- generate with the mod alone and with the project's supported mod set;
- verify pass insertion still works if a vanilla pass is renamed/missing;
- inspect generated structures, chests, tiles, walls, and loot;
- load the generated world in single-player and dedicated multiplayer;
- confirm world flags are reset between two worlds in one process.
