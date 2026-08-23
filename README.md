# AUTO JETWAY patch for Zibo 4.05.35

This unofficial source patch adds a persistent `AUTO JETWAY: ON / OFF` option
to the stock Zibo 4.05.35 Tablet. It does not contain complete Zibo or X-Plane
aircraft files and does not modify `zibomod.xpl`.

The option is located on `REALISM SETTINGS`, page 2.

## Behavior

`ON` is the default and retains the original automatic behavior. A missing,
old, non-numeric or out-of-range config value also resolves to `ON`, so an
existing installation remains behaviorally unchanged.

`OFF` suppresses only the three Zibo-owned automatic calls to
`sim/ground_ops/jetway`:

1. boarding and ground-service start;
2. boarding completion;
3. post-landing ground-service start.

Manual jetway operation through X-Plane, key or joystick assignments,
hardware and other plugins remains available. The native simulator command is
not replaced or intercepted. Jetway detection, door selection, boarding state
and the remaining ground-service logic retain the original Zibo behavior.

The option is independent of the existing aircraft `AIRSTAIRS` setting.

## Supported baseline

- Stock Zibo 4.05.35 Lua files for X-Plane 12.
- Exact supported source hashes are declared in `package-manifest.json` and
  documented in `SOURCE.md`.

The installer intentionally refuses unsupported or locally modified source
files. Do not force installation after a Zibo update.

## Install

Close X-Plane, download or clone this repository, then run:

```bash
python3 z_Install.py check --aircraft-root "/path/to/B737-800X"
python3 z_Install.py install --aircraft-root "/path/to/B737-800X"
```

On Windows, use `py` or `python` if `python3` is unavailable. Restart X-Plane
after installation and save the Tablet settings normally when the desired
value has been selected.

## Verify and uninstall

```bash
python3 z_Install.py verify --aircraft-root "/path/to/B737-800X"
python3 z_Install.py uninstall --aircraft-root "/path/to/B737-800X"
```

Installation creates complete backups under
`.zibo-auto-jetway-patch/backups/` inside the selected aircraft root. An
uninstall is refused if either installed target was subsequently modified.

See `INSTALLATION.md` for the complete procedure and `RUNTIME_TEST_PLAN.md`
for the requested simulator acceptance tests.

## Package contract

`package-manifest.json` uses schema version 2 and declares every target,
payload hash, supported source hash and installed result hash. The only
operation is an exact UTF-8 text replacement that preserves each source
file's original line endings and final-newline convention.

This small declarative operation set is suitable for later integration into a
manifest-driven aircraft maintenance tool.

## Validation status

The patch has passed source-hash validation, forward and reverse transformation,
byte-exact uninstall restoration, line-ending preservation and Lua syntax
validation against the stock 4.05.35 baseline. Simulator-runtime validation of
the stock Lua package remains open.

## Disclaimer

This project is unofficial and is not supported by Zibo or Laminar Research.
Keep a separate aircraft backup and use the patch at your own risk.
