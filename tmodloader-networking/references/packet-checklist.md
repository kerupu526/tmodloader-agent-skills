# Packet design and verification

## Packet format

Define the protocol in one place:

```text
byte/message discriminator:
protocol version (when the packet may outlive one build):
sender/target identity:
payload fields and exact read/write order:
validation rules:
server relay behavior:
```

Initialize a packet with the current `Mod.GetPacket` API, write values in a
stable order, and call `Send` with explicit `toClient`/`ignoreClient` meaning.
See the current [ModPacket reference](https://docs.tmodloader.net/docs/stable/class_mod_packet.html)
for the target lane.

## Receiver validation

Reject or safely ignore a packet when:

- the discriminator/version is unknown;
- the sender is not allowed to request the action;
- an index is out of range or points to an inactive/wrong-type entity;
- a coordinate is outside the world or not near the sender when proximity is
  part of the game rule;
- a quantity, enum, string length, or item is invalid;
- the world/player/mod state makes the action impossible;
- applying it would violate server-side progression or permission.

Use the server's authoritative object when applying an accepted request, not a
client-supplied object snapshot.

## Common desync patterns

- every client runs a player input path and spawns the same projectile;
- an NPC spawns a projectile on clients as well as the server;
- the owner changes an AI field but never marks/sends the updated state;
- a client mutates a tile entity without server validation;
- the server accepts a packet but does not relay the resulting field;
- packets are read in a different order from how they are written;
- state is synced on join but not when it changes during play;
- a late joiner sees an entity but misses custom fields.

## Test matrix

Run the smallest matrix that covers the feature:

| Case | Observe |
| --- | --- |
| single-player | behavior baseline |
| listen server + one client | direction and relay |
| dedicated server + two clients | authority and duplicates |
| late join | full initial state |
| owner death/disconnect | cleanup and re-assignment |
| repeated request | idempotence and anti-duplication |
| old/new mod mismatch if supported | safe rejection/version behavior |
