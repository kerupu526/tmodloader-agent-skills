# Terraria/tModLoader Skill Suite — source map

Research snapshot: 2026-09-20 (Asia/Seoul).

This package is a set of Codex skills, not a copy of the tModLoader manual. The
references below are deliberately links to maintained upstream material. Read
the version-matching page when a task depends on an exact signature; do not
treat this snapshot as a replacement for the live API reference.

## Version lanes observed

At the snapshot date, the official API site exposes separate `stable`,
`preview`, `1.4-stable`, and `1.3` documentation trees. The stable generated
API identifies itself as tModLoader `v2026.07`. The upstream repository exposes
`stable`, `preview`, `1.4.4`, and `1.4.5` branches. The skill suite therefore
uses these as lanes to detect, not as timeless guarantees:

| Lane | Use |
| --- | --- |
| `stable` / stable docs | Default for a normal released mod unless the project says otherwise. |
| `preview` / `1.4.5` | Preview or development work only after confirming the project branch/build. |
| `1.4.4` / `1.4-stable` | Explicit 1.4.4 maintenance or porting work. |
| `1.4.3-legacy` / `1.3` | Legacy support only; never mix its examples into current work. |

The repository heads observed during this research were `stable` at
`666f69962d3bdffde54fc14025f02634965b4e7c`, `preview` at
`2a633b0bcc8312737873350257074db8cce192d6`, `1.4.4` at
`cd937bbe458587ecfadd52b04092dd912c5bdacd`, and `1.4.5` at
`61e4750b6ce26387db427b1d7b7373941fab214d`. These hashes are a research
snapshot only; a future task must resolve the project's actual commit again.

## Primary sources

- [tModLoader API documentation selector](https://docs.tmodloader.net/)
- [Stable API class list](https://docs.tmodloader.net/docs/stable/annotated.html)
- [Preview API class list](https://docs.tmodloader.net/docs/preview/annotated.html)
- [1.4 stable API class list](https://docs.tmodloader.net/docs/1.4-stable/annotated.html)
- [tModLoader repository](https://github.com/tModLoader/tModLoader)
- [Stable ExampleMod README](https://github.com/tModLoader/tModLoader/blob/stable/ExampleMod/README.md)
- [Stable ExampleMod source tree](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod)
- [Basic tModLoader Modding Guide](https://github.com/tModLoader/tModLoader/wiki/Basic-tModLoader-Modding-Guide)
- [Update Migration Guide](https://github.com/tModLoader/tModLoader/wiki/Update-Migration-Guide)
- [Previous-version migration guide](https://github.com/tModLoader/tModLoader/wiki/Update-Migration-Guide-Previous-Versions)
- [Advanced Vanilla Code Adaption](https://github.com/tModLoader/tModLoader/wiki/Advanced-Vanilla-Code-Adaption)
- [tModLoader development pipeline](https://github.com/tModLoader/tModLoader/wiki/The-tModLoader-development-pipeline)
- [Basic prerequisites](https://github.com/tModLoader/tModLoader/wiki/Basic-Prerequisites)
- [Basic autoload](https://github.com/tModLoader/tModLoader/wiki/Basic-Autoload)
- [Assets](https://github.com/tModLoader/tModLoader/wiki/Assets)
- [Saving and loading with TagCompound](https://github.com/tModLoader/tModLoader/wiki/Saving-and-loading-using-TagCompound)

## API anchors used by the specialist skills

- [ModItem](https://docs.tmodloader.net/docs/stable/class_mod_item.html)
- [ModProjectile](https://docs.tmodloader.net/docs/stable/class_mod_projectile.html)
- [ModNPC](https://docs.tmodloader.net/docs/stable/class_mod_n_p_c.html)
- [ModPlayer](https://docs.tmodloader.net/docs/stable/class_mod_player.html)
- [ModSystem](https://docs.tmodloader.net/docs/stable/class_mod_system.html)
- [ModTile](https://docs.tmodloader.net/docs/stable/class_mod_tile.html)
- [ModTileEntity](https://docs.tmodloader.net/docs/stable/class_mod_tile_entity.html)
- [ModPacket](https://docs.tmodloader.net/docs/stable/class_mod_packet.html)
- [ModContent](https://docs.tmodloader.net/docs/stable/class_mod_content.html)
- [Item](https://docs.tmodloader.net/docs/stable/class_item.html)
- [Projectile](https://docs.tmodloader.net/docs/stable/class_projectile.html)
- [NPC](https://docs.tmodloader.net/docs/stable/class_n_p_c.html)

## Wiki pages routed by topic

### Content and gameplay

- [Basic Item](https://github.com/tModLoader/tModLoader/wiki/Basic-Item)
- [Basic Projectile](https://github.com/tModLoader/tModLoader/wiki/Basic-Projectile)
- [Basic NPC](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC)
- [Basic NPC Spawning](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC-Spawning)
- [Basic NPC Drops and Loot 1.4](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC-Drops-and-Loot-1.4)
- [Basic Recipes](https://github.com/tModLoader/tModLoader/wiki/Basic-Recipes)
- [ModPlayer](https://github.com/tModLoader/tModLoader/wiki/ModPlayer)
- [Basic Tile](https://github.com/tModLoader/tModLoader/wiki/Basic-Tile)
- [Basic Tile Entity](https://github.com/tModLoader/tModLoader/wiki/Basic-Tile-Entity)
- [World Generation](https://github.com/tModLoader/tModLoader/wiki/World-Generation)
- [Vanilla world generation steps](https://github.com/tModLoader/tModLoader/wiki/Vanilla-World-Generation-Steps)

### Client, UI, assets, and language

- [Basic UI Element](https://github.com/tModLoader/tModLoader/wiki/Basic-UI-Element)
- [Advanced guide to custom UI](https://github.com/tModLoader/tModLoader/wiki/Advanced-guide-to-custom-UI)
- [Vanilla interface layer values](https://github.com/tModLoader/tModLoader/wiki/Vanilla-Interface-layers-values)
- [Localization](https://github.com/tModLoader/tModLoader/wiki/Localization)
- [Contributing Localization](https://github.com/tModLoader/tModLoader/wiki/Contributing-Localization)
- [Spriting](https://github.com/tModLoader/tModLoader/wiki/Spriting)
- [Basic sounds](https://github.com/tModLoader/tModLoader/wiki/Basic-Sounds)

### Networking and persistence

- [Basic Netcode](https://github.com/tModLoader/tModLoader/wiki/Basic-Netcode)
- [Intermediate netcode](https://github.com/tModLoader/tModLoader/wiki/Intermediate-netcode)
- [NetMessage class documentation](https://github.com/tModLoader/tModLoader/wiki/NetMessage-Class-Documentation)
- [IEntitySource](https://github.com/tModLoader/tModLoader/wiki/IEntitySource)
- [Saving and loading with TagCompound](https://github.com/tModLoader/tModLoader/wiki/Saving-and-loading-using-TagCompound)

### Debugging, build, and release

- [Learn how to debug](https://github.com/tModLoader/tModLoader/wiki/Learn-How-To-Debug)
- [Debugging multiplayer usage issues](https://github.com/tModLoader/tModLoader/wiki/Debugging-Multiplayer-Usage-Issues)
- [JIT exception](https://github.com/tModLoader/tModLoader/wiki/JIT-Exception)
- [Logging](https://github.com/tModLoader/tModLoader/wiki/Logging)
- [Command line](https://github.com/tModLoader/tModLoader/wiki/Command-Line)
- [Workshop](https://github.com/tModLoader/tModLoader/wiki/Workshop)
- [Mod Browser](https://github.com/tModLoader/tModLoader/wiki/Mod-Browser)
- [Starting a modded server](https://github.com/tModLoader/tModLoader/wiki/Starting-a-modded-server)

## Community material policy

Community material is useful for recurring failure modes and practical
examples, but it is never allowed to override a version-matching API page,
the current ExampleMod branch, or the project's existing code. When a
community example is used, verify its branch/date and translate only the
concept that is still valid.
