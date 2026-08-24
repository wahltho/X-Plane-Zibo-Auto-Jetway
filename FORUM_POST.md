# Suggested forum post

## Experimental AUTO JETWAY ON/OFF patch for Zibo and LevelUp

Following the recent discussion about automatic jetway movement, this
experimental source patch adds a separate persistent Tablet option:

```text
AUTO JETWAY: ON / OFF
```

`ON` is the compatibility default and preserves the existing aircraft behavior.
Missing, old or invalid configuration values also resolve to `ON`.

`OFF` suppresses only the three aircraft-owned automatic calls to X-Plane's native
`sim/ground_ops/jetway` command: boarding start, boarding completion and
post-landing ground-service start. Manual operation through X-Plane, assigned
controls, hardware and other plugins remains available.

The option is independent of `AIRSTAIRS`. It does not reclassify the stand,
alter jetway detection or redirect the lifecycle into a different stairs or
ground-service branch.

Only the stock `B738.a_fms.lua` and `B738.tablet.lua` files are patched. No
complete aircraft file and no modified `zibomod.xpl` is distributed.

The attached package includes a hash-checking installer, automatic backups,
verification and safe uninstall. It supports untouched Zibo 4.05.35, LevelUp
V2.S1 and LevelUp V2.S1.50 source pairs. Modified, mixed or unsupported
targets are refused before any write.

Static package validation, Lua syntax validation and byte-exact uninstall
restoration have passed. Stock-Lua simulator testing remains open, so this is
provided as an experimental test candidate. Feedback for all three lifecycle
points, manual command pass-through, aircraft reload and full X-Plane restart
would be appreciated.

This is an unofficial patch and is not supported by Zibo, LevelUp or Laminar
Research.
