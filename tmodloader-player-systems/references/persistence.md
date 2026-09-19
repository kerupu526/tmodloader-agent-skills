# Persistence and saved state

## TagCompound contract

The official [TagCompound guide](https://github.com/tModLoader/tModLoader/wiki/Saving-and-loading-using-TagCompound)
uses `TagCompound` for custom data in `ModSystem`, `ModPlayer`, `ModItem`,
`ModNPC`, global types, and tile entities. Treat it as a transient nested
key/value serialization boundary.

- Write in the save hook and read in the load hook; do not store the tag object
  in a field.
- Initialize defaults outside the load hook because there may be no tag for a
  new object/world.
- Use stable keys and defensive reads. A missing key should resolve to the
  intended old/default behavior.
- If a field's type or meaning changes, preserve the old key and migrate it or
  explicitly accept data loss. Do not make a silent incompatible type change.
- Prefer `nameof` for typo resistance, but remember that renaming the field can
  change the serialized key; preserve an explicit old key when compatibility
  matters.
- Save only non-default values where possible. This is especially important
  for global item data and large player/world files.
- For `Item` values, use the supported item serialization rather than saving an
  ID/name pair that cannot preserve modded or unloaded item data.

## World state

For a `ModSystem` world flag:

1. Reset it in the world-load/clear lifecycle.
2. Read it in `LoadWorldData` with a safe default.
3. Write it in `SaveWorldData` only when non-default.
4. If clients need it during play, sync it through the world-data hooks or a
   dedicated packet as appropriate; persistence and replication are separate.

## Player state

For a `ModPlayer` value:

1. Initialize it in the player lifecycle.
2. Reset transient effects every update cycle or in the documented reset hook.
3. Save only durable progression/configuration state.
4. Use the player sync hooks for join and changed-state replication. See
   `tmodloader-networking` for packet direction and authority.

## Compatibility tests

Keep a representative old world and character when a feature changes saved
state. Test missing keys, old values with the old type, unloaded content, and
loading multiple worlds/characters in one process. Inspect `.twld`/`.tplr`
data with an appropriate viewer only as a diagnostic aid; the mod's defensive
load behavior is the real compatibility boundary.
