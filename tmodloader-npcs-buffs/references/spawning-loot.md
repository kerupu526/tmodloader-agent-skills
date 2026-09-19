# Spawning and loot checklist

## Natural spawning

Read the current [Basic NPC Spawning guide](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC-Spawning)
and [ModNPC API](https://docs.tmodloader.net/docs/stable/class_mod_n_p_c.html).
For each spawn rule, verify:

- neutral return value outside the desired condition;
- player biome/depth/position and tile context;
- day/night, events, invasions, hardmode, and progression flags;
- town NPC, statue, water, and other vanilla exclusions;
- spawn cap and competing spawn rules;
- whether a custom biome is queried via a stable helper rather than duplicated
  tile scans.

Do not make a spawn rule return a positive chance merely because a condition is
true; preserve the normal chance scale expected by the hook.

## Loot

Use the current [1.4 NPC drops and loot guide](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC-Drops-and-Loot-1.4).
Before editing a drop, identify its owner and mode:

```text
ModNPC.ModifyNPCLoot      -> this NPC's drops
GlobalNPC.ModifyNPCLoot   -> a matching NPC's drops
GlobalNPC.ModifyGlobalLoot -> global drops across NPCs
boss bag / expert / master -> separate rule path when appropriate
```

Check denominator/numerator semantics, luck, drop conditions, per-player
instancing, boss bags, and stack ranges. Test a representative number of
kills rather than relying only on a compile check.

## Multiplayer evidence

Manually spawn the NPC on a dedicated server and watch whether it remains
active, chooses a valid target, spawns children once, drops loot once, and
despawns consistently for all clients. If state differs, hand the packet and
authority analysis to `tmodloader-networking`.
