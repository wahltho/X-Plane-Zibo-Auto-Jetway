# Changelog

## 0.2.1 - 2026-08-24

- Accept structurally compatible shared Lua files even when unrelated patches
  change their whole-file hashes.
- Verify AUTO JETWAY-owned replacements semantically instead of requiring an
  unchanged full-file hash after installation.
- Uninstall only AUTO JETWAY-owned blocks and preserve unrelated later changes.
- Retain exact baseline fingerprints for release identification and diagnostics.

## 0.2.0 - 2026-08-24

- Add exact baseline support for LevelUp 737NG Series V2.S1 and V2.S1.50.
- Upgrade the manifest to schema 3 with paired FMS/Tablet baseline detection.
- Reject mixed Zibo/LevelUp or mixed LevelUp-version source file sets.
- Extend installer, uninstall, line-ending and Lua-syntax tests across all
  three supported baselines.
- Preserve verify and uninstall compatibility with existing v0.1.0 Zibo
  installation state.

## 0.1.0 - 2026-08-23

- Add a persistent `AUTO JETWAY: ON / OFF` Tablet option.
- Preserve the original automatic behavior as the compatibility default.
- Gate all three stock automatic jetway command callsites without intercepting
  the native X-Plane command.
- Add a manifest-driven installer with backups, verification and uninstall.
