# Projectile implementation guide

## Define the state model first

Identify whether the projectile is:

- a simple owner-fired projectile with vanilla movement;
- a held/channelled projectile that follows a player;
- an AI-driven projectile that reads owner input;
- an NPC/server-owned projectile;
- a minion/sentry, bobber, whip, flail, mount, or other specialized type;
- a visual-only projectile with no gameplay authority.

Use the current [ModProjectile API](https://docs.tmodloader.net/docs/stable/class_mod_projectile.html),
[Projectile API](https://docs.tmodloader.net/docs/stable/class_projectile.html),
and [ExampleMod projectiles](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod/Content/Projectiles)
for the exact hooks and signatures.

## Creation and ownership

- A player-owned projectile should normally be spawned only by the owning
  client. Guard a `Projectile.NewProjectile` call according to the source
  context so every client does not create a copy.
- A projectile spawned by an NPC or a non-player-owned simulation normally
  originates on the server. Do not blindly substitute `Main.myPlayer` for an
  NPC source.
- Use an `IEntitySource` that describes the real cause of the spawn. This
  improves attribution, vanilla behavior, and future compatibility.
- Pass the intended owner and initialize `ai[]` values deliberately. Record
  the meaning and units of each `ai` slot near the code.

## AI and synchronization

- Start with a timer/state machine rather than scattered magic frame counts.
- Use `Projectile.velocity`, `rotation`, `timeLeft`, `penetrate`, and collision
  fields consistently with the intended movement.
- `aiStyle`/`AIType` and cloning are useful for a prototype or a close vanilla
  adaptation. For custom behavior, locate the current vanilla implementation
  with the [Advanced Vanilla Code Adaption guide](https://github.com/tModLoader/tModLoader/wiki/Advanced-Vanilla-Code-Adaption)
  and adapt only the needed logic.
- Local mouse/input decisions must run on the owner. When authoritative state
  changes, update the projectile's network state as required by the target
  lane; do not rely on every client seeing the owner's mouse.
- If a projectile spawns children from `AI`, `OnKill`, or `OnTileCollide`,
  apply the source-specific authority guard and reduce damage/lifetime as
  intended. Test for duplicate children in a two-client session.

## Collision and drawing

- Decide separately whether the projectile is friendly/hostile, can hit NPCs
  or players, collides with tiles, and uses local or ID-based immunity.
- Keep hitbox dimensions and sprite offsets explicit. A visually correct
  sprite with an incorrect hitbox is a gameplay bug.
- Put dust, trails, sounds, shader work, and custom `PreDraw`/`PostDraw` code
  behind the correct client-side assumptions. Avoid per-frame asset requests.
- For animated textures, set the type-wide frame metadata and update the
  instance frame/timer together. Test animation on a dedicated server path to
  ensure no graphics class is loaded there.

## QA checklist

- normal spawn and despawn;
- tile collision and edge cases at world boundaries;
- friendly/hostile and PvP behavior if relevant;
- owner disconnect/death and channel release;
- multiple projectiles and penetration/immunity;
- two-client spawn, movement, hit, child-spawn, and visual behavior;
- reload/unload without stale static state.
