# Source hierarchy and disagreement handling

Use this order when deciding whether an API or pattern is safe to use:

1. The current project's compiling code and established conventions.
2. The version-matching official generated API reference.
3. The same-branch official ExampleMod source.
4. The official tModLoader wiki page, including migration notes.
5. tModLoader source, patches, and tests for behavior that the API summary
   does not explain.
6. A reputable open-source mod or community discussion, only as a lead to
   verify against the sources above.

The current project wins for local conventions but not for an obvious bug or a
stale workaround. If it uses an older API, state the mismatch and keep the
change consistent with the requested lane.

## How to resolve common conflicts

- If a method exists in one branch but not another, identify the branch and
  do not invent a compatibility shim until the user asks for multi-version
  support.
- If a wiki example and API signature differ, trust the signature for the
  selected branch and search the same-branch ExampleMod for the call site.
- If ExampleMod's default branch is ahead of the released build, switch to
  `stable` before copying code. Its README explicitly warns that the default
  source can contain upcoming-version changes.
- If a community snippet fixes a desync, verify the owner/authority rule and
  packet direction with the official netcode guide. Do not copy packet IDs or
  magic integers without identifying their meaning.
- If a porting note says something was removed or renamed, search the current
  API and current ExampleMod before assuming the replacement.

## Evidence language

Use precise confidence language in reports:

- **Confirmed** — directly supported by the selected branch/API or observed in
  a successful build/test.
- **Project convention** — works in this mod and is not being claimed as a
  universal tModLoader rule.
- **Likely** — supported by a current example but not exercised here.
- **Unverified** — needs a build, reload, dedicated server, or multiplayer
  reproduction.
