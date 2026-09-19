# NPC and buff implementation guide

## NPC responsibilities

Use the current [ModNPC API](https://docs.tmodloader.net/docs/stable/class_mod_n_p_c.html)
and [NPC API](https://docs.tmodloader.net/docs/stable/class_n_p_c.html) to
choose hooks. Keep these concerns separate:

- `SetStaticDefaults`: bestiary flags, frame metadata, sets, and type-wide data;
- `SetDefaults`: dimensions, life, defense, damage, value, sounds, and flags;
- AI/state: target selection, timers, movement, attacks, and transitions;
- hit hooks: modify/deny damage, immunity, and effects;
- spawn hooks: chance/eligibility and natural-spawn context;
- loot: `ModifyNPCLoot` and the current drop-rule conditions;
- shops/dialogue/happiness: town-NPC behavior and localization;
- drawing: client-only visual work;
- save/network: only if the NPC has state that must persist or replicate.

Compare with [ExampleMod NPCs](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod/Content/NPCs)
and `Common/GlobalNPCs` before inventing a global hook.

## AI design

Write states and transitions in terms of gameplay intent. For each state,
define the entry condition, timer reset, movement/attack behavior, exit
condition, and network-visible fields. Avoid using an unbounded random call in
every tick when a timed transition is intended.

For bosses, isolate phase selection from attack execution and test target
death, target switching, despawn distance, world progression, and multiplayer
late join. A boss that looks correct against a dummy can still fail when its
target is invalid or the world changes phase.

## Buffs and debuffs

Use the current [ModBuff and buff-related API](https://docs.tmodloader.net/docs/stable/class_mod_buff.html)
for static flags and per-tick update behavior. Check:

- whether the effect is a debuff and can be cured;
- whether NPCs, players, or both can receive it;
- immunity and reapplication rules;
- whether effects are reset every tick or derived from active buffs;
- whether visuals, dust, sound, or text are client-only;
- whether the effect must be synchronized or can be recalculated locally.

If a buff changes player stats, keep the authoritative value and reset logic
with the player/system design rather than hiding it in a visual hook.
