---
name: tmodloader-ui-client
description: Build and debug tModLoader client-side UI, interface layers, input, draw layers, textures, sounds, shaders, and other visual behavior.
---

# UI and client behavior

## When to use

Use this skill for `UIState`, `UIElement`, `UserInterface`, custom menus,
interface layers, inventory/UI interaction, keybinds, player draw layers,
custom drawing, assets, sounds, shader effects, and client-only behavior.

Use `tmodloader-world-tiles` for tile entities whose UI is only one part of
the feature, `tmodloader-networking` when the UI sends gameplay mutations, and
the owning content skill for gameplay state.

## Workflow

1. Identify the client lifecycle: loading, in-game interface, fullscreen menu,
   world/map layer, player/entity draw, or asset-only behavior.
2. Keep UI state and authoritative gameplay state separate. A button can ask
   the server to perform an action; it must not grant the action merely because
   the client clicked it.
3. Register/unregister `UserInterface` states and interface layers at the
   correct lifecycle. Remove references, hooks, keybinds, and draw layers on
   unload so reload does not duplicate UI.
4. Use the current UI element guide and ExampleMod for layout, mouse handling,
   focus, scaling, and layer insertion. Do not guess interface-layer names.
5. Load assets through the current asset API. Avoid requesting the same asset
   every frame; use immediate loading only when dimensions are required before
   layout and arrange asynchronous loading when possible.
6. Guard graphics/input code from dedicated-server execution. Test different
   UI scales, resolutions, fullscreen/windowed modes, mouse/gamepad input, and
   language lengths.

## Non-obvious invariants

- A server must be able to load the mod without constructing a texture,
  `SpriteBatch`, shader, or client-only UI type.
- `ModifyInterfaceLayers` is the preferred insertion point for custom interface
  drawing; obsolete post-draw shortcuts should not be copied without checking
  the current API.
- A `UIState` that reads texture dimensions before an asset is loaded can be
  laid out at the temporary 1x1 size. Load or defer layout deliberately.
- Drawing a local visual effect and changing gameplay state are separate
  operations; only the latter needs authority/network design.
- Keyboard/mouse input is local. Send a validated request for shared gameplay
  actions and update the UI from authoritative state.

## References

- Read [ui-lifecycle.md](references/ui-lifecycle.md) for UI state, layers,
  input, and unload patterns.
- Read [assets-client.md](references/assets-client.md) for texture/sound/shader
  loading and dedicated-server constraints.
- Use the suite [SOURCE-MAP](../SOURCE-MAP.md) for official UI and asset links.
