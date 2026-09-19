# Item implementation guide

## Start from the item contract

Before coding, write down:

```text
use style and timing:
damage class and damage/knockback:
ammo or projectile:
consumption and reuse rules:
equipment/accessory state:
recipe or acquisition:
save data on the item instance:
client-only visuals:
```

Then inspect the current [ModItem API](https://docs.tmodloader.net/docs/stable/class_mod_item.html)
and a comparable file in [ExampleMod/Content/Items](https://github.com/tModLoader/tModLoader/tree/stable/ExampleMod/Content/Items).

## Defaults and hooks

- Use `SetStaticDefaults` for static sets, frame counts, and type-wide metadata.
- Use `SetDefaults` for the item's per-type gameplay fields.
- Use the narrowest hook that expresses the behavior: `UseItem`, `Shoot`,
  `ModifyShootStats`, `CanUseItem`, `UseStyle`, `HoldItem`, or equipment
  hooks as appropriate.
- Treat `CanUseItem` as side-effect-free. If a resource must be consumed,
  use the consumption hook or the confirmed successful-use path.
- When changing ammo behavior, inspect both the weapon-side and ammo-side
  hooks in the current API. The 1.4.4-era API has separate selection and
  consumption hooks; old `ConsumeAmmo` examples may be wrong for the target.
- For accessories and armor, decide whether state is stored on the item
  instance or projected into a `ModPlayer`. Visual equipment may be drawn from
  an equip texture rather than the live inventory item.

## Recipes and acquisition

- Prefer the current `CreateRecipe`/`Recipe` API and register every recipe.
- Use typed mod-content references for modded ingredients/tiles where the
  target lane supports them; use vanilla IDs only for vanilla content.
- Check crafting station, recipe groups, conditions, shimmer/decrafting, and
  stack amounts in-game. A recipe that compiles can still be unavailable or
  use the wrong station.
- Keep loot, shops, and recipes owned by the feature's appropriate class or
  system. See [Basic Recipes](https://github.com/tModLoader/tModLoader/wiki/Basic-Recipes)
  and [NPC Drops and Loot](https://github.com/tModLoader/tModLoader/wiki/Basic-NPC-Drops-and-Loot-1.4)
  for the current patterns.

## Visual and localization completeness

For a new item, inspect all of the following before calling it complete:

- source file and matching texture path;
- equipment textures if an equip attribute requires them;
- display name and tooltip localization;
- recipe, shop, loot, or creative/journey behavior;
- held/inventory/world drawing if the default drawing is not suitable;
- sound and asset loading side constraints.

Let `tmodloader-localization` own HJSON details and `tmodloader-ui-client`
own advanced drawing/assets.
