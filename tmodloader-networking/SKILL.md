---
name: tmodloader-networking
description: Design and debug tModLoader multiplayer synchronization, ModPacket protocols, entity ownership, player/world sync, and server-authoritative behavior.
---

# tModLoader networking

## When to use

Use this skill when a feature has packets, multiplayer state, owner/client
authority, `ModPacket`, `SyncPlayer`, `NetSend`/`NetReceive`, `netUpdate`, tile
entity sync, late join, duplicate spawns, or desync.

Use the owning specialist for the content implementation, but make this skill
the lead when the failure is “works in single-player, breaks in multiplayer”
or when a new protocol is required.

## Workflow

1. Draw the state flow before writing code:

   ```text
   state -> authoritative owner -> message/vanilla sync -> receiver -> local view
   ```

   Mark each field as local-only, persistent, server-authoritative,
   owner-authoritative, or derived.
2. Identify the source entity and side. A player input, NPC AI, projectile AI,
   world flag, tile change, and UI click do not share one authority rule.
3. Prefer built-in entity/world/player sync when it expresses the state. Use a
   `ModPacket` for arbitrary mod state, requests, or cross-object messages.
4. Give every custom packet an explicit discriminator/version and validate
   sender, target, enum/range, entity index/type, and world/context before
   applying it. A client packet is a request, not proof of permission.
5. Relay accepted client changes from the server to other clients when needed.
   Avoid echo loops and make repeated packets idempotent where possible.
6. Test single-player, listen server, dedicated server, two clients, late join,
   reconnect, owner death/disconnect, world transition, and mod reload. Log
   packet direction and key state transitions at debug level, not every frame.

## Non-obvious invariants

- `Main.myPlayer` identifies the local player; it is not a universal authority
  check. Use `Main.netMode`, entity owner, and source context together.
- A client should not independently simulate an authoritative state merely
  because it can render it. Derive presentation from synced data.
- `ModPacket` inherits binary-writer behavior. Define and preserve read/write
  order; adding a field without a version/discriminator can corrupt the rest of
  the stream.
- `SyncPlayer` handles join/full player synchronization; changed local player
  state commonly uses `CopyClientState`/`SendClientChanges` plus an accepted
  packet or documented sync path.
- `ModSystem.NetSend`/`NetReceive` and tile-entity `NetSend`/`NetReceive` have
  different lifecycle meanings. Do not use one for arbitrary per-tick traffic.
- A spawn guard prevents duplicate entities; it does not automatically sync
  later custom AI fields.

## References

- Read [netcode-model.md](references/netcode-model.md) for authority and state
  classification.
- Read [packet-checklist.md](references/packet-checklist.md) for safe packet
  design and test cases.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for current API and wiki links.
