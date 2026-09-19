---
name: tmodloader-debug-build-qa
description: Build, reload, debug, inspect logs, reproduce, and QA Terraria tModLoader mods across single-player, dedicated-server, and multiplayer scenarios.
---

# Build, debugging, and QA

## When to use

Use this skill for compile/build failures, Build + Reload failures, missing
assets/localization, stack traces, JIT exceptions, load/unload bugs, runtime
regressions, dedicated-server failures, multiplayer reproduction, and release
readiness.

Use `tmodloader-versioning` first when the failure may be a lane mismatch. Use
the owning specialist when the cause is known and the user wants a feature fix.

## Workflow

1. Reproduce the failure with the smallest enabled mod set and capture the
   first relevant error, not only the final cascade. Record loader lane, mod
   commit, platform, world/character, and single-player/server context.
2. Classify the failure as source/compiler, content/autoload, asset/
   localization, runtime lifecycle, side/authority, save compatibility, or
   environment/tooling. Read the relevant official guide before changing code.
3. Use a clean baseline: build/reload the untouched or last-known-good source,
   then make one coherent change at a time. Preserve the log and diff.
4. For a compiler error, inspect the exact version-matched API signature and
   project target framework before changing names or adding casts.
5. For runtime/load failures, inspect the earliest stack frame owned by the
   mod, static initializers, autoload paths, asset case, localization parse,
   dedicated-server graphics references, and unload/reset lifecycle.
6. For multiplayer failures, run the authority/packet checklist and reproduce
   with a dedicated server and at least two clients when possible.
7. Finish with proportional checks: build, reload, targeted in-game behavior,
   server load, old save/load, and regression scenarios. Report evidence and
   remaining unverified cases.

## Non-obvious invariants

- “Build succeeded” proves compilation/package generation, not content
  loading, localization, save compatibility, or multiplayer correctness.
- “Works in single-player” does not test server authority or packet relay.
- A load error may be caused by a type initializer or asset reference before
  the method named in the stack trace is reached.
- Build + Reload is a tModLoader content lifecycle; IDE compile/debug and
  in-game reload exercise different paths.
- Unload bugs often show up only on the second reload. Test two cycles when the
  mod uses static events, UI, hooks, assets, or custom detours.
- Never suppress an exception or add a null guard solely to hide the symptom;
  identify the invalid lifecycle/side/asset assumption first.

## References

- Read [build-debug.md](references/build-debug.md) for build, logs, and debugger
  routing.
- Read [qa-matrix.md](references/qa-matrix.md) for proportional regression and
  release checks.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for official debugging and
  pipeline links.
