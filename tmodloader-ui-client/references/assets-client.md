# Assets and client-only work

Read [Assets](https://github.com/tModLoader/tModLoader/wiki/Assets),
[Spriting](https://github.com/tModLoader/tModLoader/wiki/Spriting), and the
current [ModContent API](https://docs.tmodloader.net/docs/stable/class_mod_content.html).

## Asset rules

- Use the mod's namespace/path conventions and preserve exact casing.
- Prefer the mod asset request API and cache the returned asset reference.
- Do not request textures, sounds, fonts, or effects every frame.
- Use asynchronous loading for ordinary assets. If UI layout needs dimensions
  before the first draw, load during the proper client lifecycle or use the
  documented immediate mode sparingly; do not hide a load stall in a hot hook.
- Keep shader/effect initialization client-only and dispose/clear custom state
  on unload.
- Match spritesheet frame counts, equipment texture suffixes, sound paths, and
  fallback behavior to the target branch's ExampleMod examples.

## Dedicated server boundary

Audit namespaces and static initializers, not only method bodies. A server can
fail while loading a type that references a graphics-only class even if its
draw method is never called. Use the target lane's client-side attributes or
side checks and keep shared model/state types free of graphics dependencies.

## Visual QA

Check normal and flipped sprites, animation frames, lighting, afterimages,
player draw ordering, UI scale, resolution, language text expansion, asset
reload, and a dedicated-server load. A feature is not complete if it only works
with the developer's default 1920x1080 UI scale and English language.
