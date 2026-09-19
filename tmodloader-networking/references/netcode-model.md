# Multiplayer state model

Read the official [Basic Netcode](https://github.com/tModLoader/tModLoader/wiki/Basic-Netcode),
[Intermediate netcode](https://github.com/tModLoader/tModLoader/wiki/Intermediate-netcode),
and [ModPacket API](https://docs.tmodloader.net/docs/stable/class_mod_packet.html).

## Classify each value

| Value | Typical authority | Typical mechanism |
| --- | --- | --- |
| local input, mouse, keybind | local client | request packet if it changes shared state |
| player state at join | server/client handshake | `ModPlayer.SyncPlayer` |
| changed local player field | owning client to server | `CopyClientState` + `SendClientChanges` or explicit packet |
| NPC AI/progression | server | vanilla/entity sync plus explicit custom sync |
| player-owned projectile movement | owning client | projectile owner and `netUpdate`/entity sync as needed |
| NPC-owned projectile movement | server | server spawn/AI and entity sync |
| world progression flag | server/world | `ModSystem.NetSend`/`NetReceive` or explicit packet |
| tile type/frame | server/vanilla tile sync | tile network message/helpers |
| tile entity fields | server | tile entity `NetSend`/`NetReceive` |
| UI visibility | local client | local state only unless it represents shared state |

These are starting points, not substitutes for the selected API documentation.
Some vanilla hooks already synchronize fields; do not send duplicate packets
without confirming the contract.

## Authority questions

For each mutation answer:

```text
Who can request it?
Who validates it?
Who commits it?
Who receives the result?
What happens if the sender is stale or disconnected?
Can the action be repeated safely?
```

If the server commits a mutation, send the result or rely on a documented
vanilla synchronization path. Never let a client-only visual change be mistaken
for a committed game-state change.

## Official API anchors

- [ModPlayer SyncPlayer](https://docs.tmodloader.net/docs/stable/class_mod_player.html)
- [ModPlayer CopyClientState](https://docs.tmodloader.net/docs/stable/class_mod_player.html)
- [ModSystem NetSend/NetReceive](https://docs.tmodloader.net/docs/stable/class_mod_system.html)
- [ModTileEntity NetSend/NetReceive](https://docs.tmodloader.net/docs/stable/class_mod_tile_entity.html)
- [Projectile API](https://docs.tmodloader.net/docs/stable/class_projectile.html)
