# Version detection

Use multiple signals. No single filename is a reliable version detector.

| Evidence | What it can establish | Caution |
| --- | --- | --- |
| Explicit user target or release/branch | Intended destination | Still verify the API branch and installed build. |
| Git branch/tag and commit | Which source lane the project follows | A local branch can be renamed or based on a fork. |
| API docs URL used by the project | Intended API family | Links in old comments may be stale. |
| `ModSources/<ModName>` generated tree | It is likely a source mod rather than a compiled `.tmod` | It does not identify 1.4.4 vs preview by itself. |
| `build.txt`, `description.txt`, localization folder | Mod metadata and generated layout | These files are not a complete loader version manifest. |
| `.csproj` target framework, references, launch settings | Build/runtime setup | A hand-edited project may retain old values. |
| Compiler error and missing/renamed hook | A clue about the API lane | Confirm with the matching migration guide before changing code. |
| tModLoader installation or Steam beta selection | Runtime lane | Ask the user or inspect configured paths; do not infer from Terraria alone. |

## Lane decision

- If the project clearly targets the normal released installation and no
  preview switch/branch is present, start with the stable API tree.
- If it explicitly targets preview or the `1.4.5` branch, use preview/1.4.5
  documentation and state that the API may move.
- If it names `1.4.4`, use the 1.4.4/stable lane even if a newer preview exists.
- If it names 1.4.3 or 1.3, use the legacy API tree and the historical
  migration notes; do not “modernize” unrelated code during a compatibility
  fix.
- If the evidence is insufficient, ask for the target only when changing the
  target would materially change the implementation. Otherwise inspect the
  API candidates and clearly mark the chosen assumption.

## Useful checks

```text
git branch --show-current
git log -1 --format=%H
find . -name '*.csproj' -o -name 'build.txt' -o -name 'launchSettings.json'
```

On Windows, use the equivalent file and Git inspection commands. These are
diagnostic examples; preserve the user's shell and repository conventions.

## Current-source reminder

The official docs selector currently exposes stable, preview, 1.4-stable, and
1.3 trees. The repository also carries separate `stable`, `preview`, `1.4.4`,
and `1.4.5` branches. Re-check these links at task time because release status
and branch history can change.
