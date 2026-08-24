# Source and owner evidence

## Target baselines

The package was derived from locally preserved, untouched stock Zibo and
LevelUp aircraft files. No complete upstream file is distributed by this
repository.

| Baseline | File | Source SHA-256 | Installed SHA-256 |
|---|---|---|---|
| Zibo 4.05.35 | `B738.a_fms.lua` | `e2e427adffb030a3b7c8dc02a1adb971417be61bd22aa67a18e08f14d9d9390a` | `d603ccd5e8ca9ad52972112f1f34ff3843f22a1173ba515eacfbd61e77ae211f` |
| Zibo 4.05.35 | `B738.tablet.lua` | `89598db3a999bade26faf960ad5c76f2d15bb08e7b1f8106a597e2998a2e8c72` | `397eaa6babefe43031a7b16626678b691fc3a5cf150617ffd7642f882d6aec95` |
| LevelUp V2.S1 | `B738.a_fms.lua` | `43916b6288d397854a24ce59745967f50d13e6d183f51137364463d0f398f582` | `2474610fecbac8e05c580a95c9880ba090d770a49167dd6708c96d0e2c7b0096` |
| LevelUp V2.S1 | `B738.tablet.lua` | `89598db3a999bade26faf960ad5c76f2d15bb08e7b1f8106a597e2998a2e8c72` | `397eaa6babefe43031a7b16626678b691fc3a5cf150617ffd7642f882d6aec95` |
| LevelUp V2.S1.50 | `B738.a_fms.lua` | `757057120c2953a9cdefbfebcd593bdb4fd9636721328fb1ce6d6550f8f49384` | `99d981f0b7824140b35b2334cbfc303d1e8ce3b62eed3b63b3f6575c05e1be42` |
| LevelUp V2.S1.50 | `B738.tablet.lua` | `0cad13f73440f5045d8916c94600a5333d22bef6d71495ffab6872eb0feae730` | `ed6e7cef41808cf43a71b8eb91214b3887cd980b07a5e374e595374a46b66a3b` |

Zibo 4.05.35 and LevelUp V2.S1 use CRLF for FMS and LF for Tablet. LevelUp
V2.S1.50 uses CRLF for both. The installer preserves each target's existing
convention.

Manifest schema 3 binds both files into one detected baseline. A valid file
from one release combined with a valid file from another is rejected before
any write.

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
