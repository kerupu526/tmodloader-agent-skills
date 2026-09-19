# UI lifecycle and interaction

Read [Basic UI Element](https://github.com/tModLoader/tModLoader/wiki/Basic-UI-Element),
[the advanced custom UI guide](https://github.com/tModLoader/tModLoader/wiki/Advanced-guide-to-custom-UI),
and the current [ModSystem API](https://docs.tmodloader.net/docs/stable/class_mod_system.html).

## A safe shape

Keep these pieces distinct:

- a `UIState` that owns a screen/panel;
- child `UIElement`s that render and handle local input;
- a system that owns the `UserInterface`, activation, update, and draw;
- a gameplay/system owner that supplies authoritative data;
- a packet/request path if a click mutates shared state.

Use `ModifyInterfaceLayers` to insert a named layer relative to a current
vanilla layer and return the appropriate draw result. Handle the layer being
absent rather than inserting at an unchecked index. Use `GameTime` and the
documented UI update/draw lifecycle rather than updating gameplay from draw.

## Input and focus

- Register keybinds through the current keybind system and handle them only on
  the local client.
- Make opening/closing idempotent; repeated key presses should not stack the
  same state or event handler.
- Respect `Main.gameMenu`, pause, chat, inventory, and other contexts where the
  UI should not consume input.
- Scale anchors and measurements with the UI scale system. Test long localized
  labels and controller/gamepad navigation when supported by the feature.

## Unload and reload

On unload, remove the interface state, clear references to UI elements and
assets, unregister hooks/keybinds created by the system, and restore any global
draw-layer registration. A second build/reload is a required test for duplicate
clicks, stale textures, and leaked static state.

## Tile/entity UI

Resolve the tile entity from a validated top-left tile coordinate, show a
snapshot of its state, and send mutations through a server-validated path. The
UI should close or refresh when the tile is removed, the player moves away, or
the entity becomes invalid.
