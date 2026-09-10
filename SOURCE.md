# Source and owner evidence

## Target baselines

The package was derived from locally preserved, untouched stock Zibo and
LevelUp aircraft files. The effective Zibo 4.05.35 baseline is the stock
4.05.00 base plus the cumulative 4.05.35 update, with an update file taking
precedence whenever its relative path exists. Both Lua targets below are owned
by that update; their hashes also match the original update ZIP whose
`version.txt` reports `4.05.35`. No complete upstream file is distributed by
this repository.

| Baseline | File | Source SHA-256 | Installed SHA-256 |
|---|---|---|---|
| Zibo 4.05.35 | `B738.a_fms.lua` | `ff313b0e88c62845ad1c4a2b1f4bd599f57d8799e8d6707bfc10a3369fd63a8e` | `6dc07cac5cd89c4645890ed4d29f0bf1c6ccddba62cc31b2be827bb0f7c8f9d6` |
| Zibo 4.05.35 | `B738.tablet.lua` | `7c9e445a2a002f1ef81a0b738ad3c3b791a63c2c313d44d993517e260cd32141` | `ce0e634c979696c0f17a9c2a2fd69bfe72b243b2c266fce6ea1486951ffca76d` |
| LevelUp V2.S1 | `B738.a_fms.lua` | `43916b6288d397854a24ce59745967f50d13e6d183f51137364463d0f398f582` | `2474610fecbac8e05c580a95c9880ba090d770a49167dd6708c96d0e2c7b0096` |
| LevelUp V2.S1 | `B738.tablet.lua` | `89598db3a999bade26faf960ad5c76f2d15bb08e7b1f8106a597e2998a2e8c72` | `397eaa6babefe43031a7b16626678b691fc3a5cf150617ffd7642f882d6aec95` |
| LevelUp V2.S1.50 | `B738.a_fms.lua` | `757057120c2953a9cdefbfebcd593bdb4fd9636721328fb1ce6d6550f8f49384` | `99d981f0b7824140b35b2334cbfc303d1e8ce3b62eed3b63b3f6575c05e1be42` |
| LevelUp V2.S1.50 | `B738.tablet.lua` | `0cad13f73440f5045d8916c94600a5333d22bef6d71495ffab6872eb0feae730` | `ed6e7cef41808cf43a71b8eb91214b3887cd980b07a5e374e595374a46b66a3b` |

Zibo 4.05.35 and LevelUp V2.S1 use CRLF for FMS and LF for Tablet. LevelUp
V2.S1.50 uses CRLF for both. The installer preserves each target's existing
convention.

Manifest schema 3 reports an exact baseline only when both hashes match the
same known pair. Other structurally compatible files remain eligible only when
every owned replacement anchor validates unambiguously.

Version 0.2.3 corrects Zibo hashes that earlier releases mislabeled as 4.05.35
even though they came from the 4.05.00 base tree. The patch payload and runtime
behavior are unchanged.

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
