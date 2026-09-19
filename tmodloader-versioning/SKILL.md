---
name: tmodloader-versioning
description: Identify a Terraria tModLoader version lane and port or update a mod across 1.3, 1.4.3, 1.4.4 stable, and preview branches using matching official migration evidence.
---

# tModLoader versioning and porting

## When to use

Use this skill before changing code when the user mentions porting, updating,
preview builds, an old mod, a compiler signature error, a branch, or a
version-specific API. It also applies when a project has no obvious version
metadata and copying an example could be risky.

Do not use it to guess a version from a class name alone. If the request is
clearly a feature implementation in an already identified lane, hand the
feature to the relevant specialist after this skill's short detection pass.

## Required workflow

1. Inspect the project and record evidence: repository branch/commit,
   `build.txt`, `.csproj` target framework and references, `Properties` files,
   folder layout, installed `ModSources` context, and the exact compiler/log
   message.
2. Classify the project into the [version lanes](references/version-detection.md).
   If evidence conflicts, stop assuming and report the conflict; use the
   explicit user target as the intended destination but preserve a backup or
   separate porting branch when possible.
3. Read the matching API tree and the official [Update Migration Guide]. Do
   not use preview or default-branch ExampleMod code for a stable build unless
   the project is explicitly targeting that preview lane.
4. Establish a clean baseline by building the untouched source if possible.
   Separate mechanical API changes from behavior changes. Fix one family of
   errors at a time and rebuild so later errors are not cascading noise.
5. For save data, networking, localization, and assets, perform a dedicated
   compatibility pass. A successful compile does not prove old worlds,
   players, multiplayer clients, or translations remain compatible.
6. Validate the migrated mod in the destination lane. Report exactly which
   lane and commit were tested, what could not be tested, and any remaining
   preview risk.

## Rules that prevent version drift

- Treat `stable`, `preview`, `1.4.4`, and `1.4.5` as different evidence
  sources. A branch name in a URL is part of the API context.
- Prefer a project's current code over an old internet snippet, but do not
  preserve a stale workaround merely because it compiles.
- Never silently convert a legacy `ModWorld`/old world hook design into a
  guessed `ModSystem` design. Consult the migration notes and current API,
  then preserve the intended world lifecycle and reset behavior.
- Do not use a compatibility abstraction to hide differences unless the user
  requested multiple target lanes. For one target, use that lane's native API.
- Keep migration commits or patches reviewable: one conceptual conversion per
  change, and keep generated/localization changes distinguishable from code.

## References

- Read [version-detection.md](references/version-detection.md) for the evidence
  table and stable/preview decision.
- Read [migration-workflow.md](references/migration-workflow.md) for the
  porting order and regression checklist.
- Use the suite-wide [SOURCE-MAP](../SOURCE-MAP.md) for live official links.

[Update Migration Guide]: https://github.com/tModLoader/tModLoader/wiki/Update-Migration-Guide
