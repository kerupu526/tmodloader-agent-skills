# Routing matrix

Use the first column that explains the user's requested behavior. A feature
can have more than one owner; the router should keep a small handoff note in
the implementation plan so that persistence, network, and client concerns are
not lost when the main content class is obvious.

| User intent or file family | Primary skill | Also inspect |
| --- | --- | --- |
| `ModItem`, weapon, accessory, ammo, prefix, recipe | `tmodloader-items-projectiles` | localization, networking if spawned state is custom |
| `ModProjectile`, AI, hitbox, owner, drawing, projectile spawn | `tmodloader-items-projectiles` | networking, UI/client for custom drawing |
| `ModNPC`, boss, town NPC, spawn chance, loot, buff immunity | `tmodloader-npcs-buffs` | networking, player-systems for world flags |
| `ModBuff`, `GlobalBuff`, player effects | `tmodloader-npcs-buffs` | player-systems, localization |
| `ModPlayer`, `GlobalItem`, `GlobalNPC`, `GlobalProjectile`, `ModSystem` | `tmodloader-player-systems` | networking, versioning |
| `SaveData`, `LoadData`, `SaveWorldData`, `LoadWorldData`, `TagCompound` | `tmodloader-player-systems` | networking for replicated state |
| world flags, world generation pass, biome, tile count | `tmodloader-world-tiles` | player-systems, networking |
| `ModTile`, `ModWall`, `ModTileEntity`, multitile, chest, wiring | `tmodloader-world-tiles` | UI/client, networking |
| `UIState`, `UIElement`, `UserInterface`, interface layers, hotkeys | `tmodloader-ui-client` | networking only if UI sends commands |
| textures, sounds, shaders, draw layers, `Main.dedServ` | `tmodloader-ui-client` | assets in ExampleMod, versioning |
| `ModPacket`, `NetSend`, `NetReceive`, `SyncPlayer`, desync | `tmodloader-networking` | owning content skill |
| `.hjson`, `DisplayName`, `Tooltip`, language files | `tmodloader-localization` | owning content skill |
| build/reload errors, missing asset, load/unload, stack trace | `tmodloader-debug-build-qa` | versioning first if signature-related |
| porting a 1.3/1.4.3/1.4.4 mod or preview branch | `tmodloader-versioning` | affected specialist |

## Cross-cutting handoff template

When a change crosses skills, record:

```text
Feature:
Version lane and evidence:
Primary content owner:
State that is saved:
State that is networked:
Client-only work:
Localization/assets:
Build/runtime checks:
```

This is a planning aid, not a requirement to create a separate document in the
user's mod.
