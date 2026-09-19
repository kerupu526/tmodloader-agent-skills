# Build and debug routing

Read the official [development pipeline](https://github.com/tModLoader/tModLoader/wiki/The-tModLoader-development-pipeline),
[Learn How To Debug](https://github.com/tModLoader/tModLoader/wiki/Learn-How-To-Debug),
[JIT Exception](https://github.com/tModLoader/tModLoader/wiki/JIT-Exception),
[Logging](https://github.com/tModLoader/tModLoader/wiki/Logging), and the
target lane's project setup.

## Build layers

Use the strongest available layer in order:

1. tModLoader's in-game `Build + Reload` for source/autoload/content packaging;
2. IDE/`dotnet` build for compiler diagnostics and debugger symbols;
3. dedicated-server launch/load for server-side assembly and side safety;
4. in-game reproduction for runtime behavior and asset/localization use.

Do not report an IDE build as proof that tModLoader can load the mod. Conversely,
do not discard a useful compiler error because the in-game log is shorter.

## First-failure method

- Save the complete log and the exact source diff.
- Find the first error/exception and its first mod-owned frame.
- Separate warnings from the failure that stops loading.
- Check version/lane before changing an API call.
- Rebuild after one conceptual fix and compare the new first failure.

## Debugger

Use the generated `.csproj`/launch settings and the current IDE guide for
breakpoints. Set breakpoints in the owning hook and in the state transition,
not only in the final draw or packet receiver. Inspect:

- side (`Main.dedServ`, `Main.netMode`, local player index);
- content type and active instance index;
- owner/target validity;
- timer/state values and `timeLeft`;
- saved-data key/defaults;
- packet discriminator and sender when networking is involved.

## Error classes

- **No suitable method/override**: likely wrong lane/signature; compare the
  current class API and migration notes.
- **Content not found/texture missing**: inspect namespace, asset path/case,
  autoload convention, and generated source layout.
- **JIT/server load exception**: inspect client-only types in fields/static
  initializers and side guards.
- **Null entity/invalid index**: validate active/type/coordinate and lifecycle.
- **Second reload fails**: inspect static events, hooks, UI, detours, cached
  assets, and unload cleanup.
- **Multiplayer-only**: use `tmodloader-networking`; do not “fix” by adding
  arbitrary delays.
