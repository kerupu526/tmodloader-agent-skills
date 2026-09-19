# Ownership and lifecycle

## Choose the owner

| State | Preferred owner | Why |
| --- | --- | --- |
| A value belongs to one player across items | `ModPlayer` | One instance per player; easy to reset, save, and sync. |
| A value belongs to one item/NPC/projectile instance | its `Mod*` or appropriately scoped `Global*` | Keeps instances independent. |
| A rule modifies many existing items/NPCs/projectiles | matching `Global*` | Avoids editing every content class. Keep it narrow. |
| A world progression flag or world lifecycle task | `ModSystem` | World load/save and world-wide hooks live here in current 1.4.x. |
| A mod-wide service or integration | `ModSystem` or the mod class as documented | Avoid hidden static state and unload leaks. |
| User-tunable settings | `ModConfig` | Configuration lifecycle and UI are separate from game state. |
| A player command or server action | `ModCommand`/current command API | Validate caller and inputs before mutation. |

Use the current [ModPlayer API](https://docs.tmodloader.net/docs/stable/class_mod_player.html),
[ModSystem API](https://docs.tmodloader.net/docs/stable/class_mod_system.html),
and [ExampleMod Common](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod/Common)
for exact hook names.

## Lifecycle questions

For each field, answer:

```text
When is it initialized?
When is it reset after death/respawn/world change/unload?
Is it saved?
Is it networked?
Who may mutate it?
Can a client request a mutation?
What happens when the content that created it is unloaded?
```

Use reset hooks rather than relying on `LoadData` to run every time. Keep
`PostUpdate`, draw, and UI hooks derived from authoritative state whenever
possible.

## Global types

Before adding a `GlobalItem`, `GlobalNPC`, or `GlobalProjectile`, check whether
a local `Mod*` class or a `ModPlayer` is a better owner. If the global type
stores mutable data, verify whether it is instance-per-entity, whether cloning
is needed, and how the field is saved. A global hook that changes every vanilla
object is a large compatibility surface and should carry explicit conditions.
