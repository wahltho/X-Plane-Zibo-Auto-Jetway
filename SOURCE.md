# Source and owner evidence

## Target baseline

The package was derived from locally preserved, untouched stock Zibo 4.05.35
aircraft files. No complete upstream file is distributed by this repository.

| Relative path | Source SHA-256 | Installed SHA-256 |
|---|---|---|
| `plugins/xlua/scripts/B738.a_fms/B738.a_fms.lua` | `e2e427adffb030a3b7c8dc02a1adb971417be61bd22aa67a18e08f14d9d9390a` | `d603ccd5e8ca9ad52972112f1f34ff3843f22a1173ba515eacfbd61e77ae211f` |
| `plugins/xlua/scripts/B738.tablet/B738.tablet.lua` | `89598db3a999bade26faf960ad5c76f2d15bb08e7b1f8106a597e2998a2e8c72` | `397eaa6babefe43031a7b16626678b691fc3a5cf150617ffd7642f882d6aec95` |

The FMS file uses CRLF and the Tablet file uses LF in this baseline. The
installer preserves the existing convention of each target.

## Owner chain

```text
REALISM SETTINGS page 2 / line command 15
  -> laminar/B738/tab/auto_jetway
  -> FMS-owned default and global config loader
  -> AUTO JETWAY config key
  -> three Tablet lifecycle guards
  -> native sim/ground_ops/jetway command
```

The FMS Lua owns the DataRef, compatibility default, validation and flat
aircraft configuration. The Tablet Lua owns display, click cycling and the
three automatic command callsites.

## Persistence contract

- The default is set to `1` before configuration loading.
- Exact numeric `0` selects `OFF`; every other parsed or invalid value selects
  `ON`.
- The key is loaded and saved only through the global variant configuration.
- Livery configuration loading and saving ignores the key, so an old livery
  cannot override the global owner.

## Automatic callsite closure

All stock occurrences of `B738CMD_jetways_toggle:once()` are guarded:

1. auto-flight state 1: boarding and ground-service start;
2. auto passenger status 4: boarding completion after L1/L2 close;
3. auto-flight state 4: post-landing ground-service start.

The guards are nested inside the existing nearby-jetway branches. The
surrounding door, timer, boarding, stairs, bus, belt and state-transition logic
is not moved or reset. No simulator command handler is added.
