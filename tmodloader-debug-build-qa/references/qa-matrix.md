# QA matrix

Choose checks based on the feature's risk. Do not claim a full QA pass when a
scenario is not relevant or was not run.

| Feature | Minimum evidence | Stronger evidence |
| --- | --- | --- |
| item/recipe | build, reload, acquire/use/craft | save/reload, prefixes, multiplayer use |
| projectile | spawn, movement, hit/collision | two clients, owner disconnect, child spawns |
| NPC/boss | natural/manual spawn, AI, death/loot | progression, target loss, dedicated server |
| buff/player effect | apply, tick, expire/reset | death/respawn, save/load, join/relay |
| world generation | new worlds in relevant sizes/seeds | multiple mod sets, missing pass fallback |
| tile/entity | place/break/use/save | wiring/liquids, two clients, server validation |
| UI/client | open/close/draw/input | UI scales, resolutions, languages, reload twice |
| localization | build/reload, language switch | long strings, all supported languages, fallback |
| config/command | valid/invalid input and reload | server/client permissions and persistence |
| porting | clean build in target lane | old saves, old clients if supported, feature regression |

## Release evidence

Record:

```text
target tModLoader lane/version:
mod commit/build metadata:
build + reload result:
dedicated-server load result:
new world/character result:
existing save result:
multiplayer result:
localization/assets result:
known untested cases:
```

A known untested case is a useful QA result. Do not hide it behind a green
summary.
