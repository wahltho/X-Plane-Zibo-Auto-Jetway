# AUTO JETWAY patch for Zibo and LevelUp 737NG

This unofficial source patch adds a persistent `AUTO JETWAY: ON / OFF` option
to supported stock Zibo and LevelUp Lua Tablets. It does not contain complete
Zibo, LevelUp or X-Plane aircraft files and does not modify `zibomod.xpl`.

The option is located on `REALISM SETTINGS`, page 2.

## Behavior

`ON` is the default and retains the original automatic behavior. A missing,
old, non-numeric or out-of-range config value also resolves to `ON`, so an
existing installation remains behaviorally unchanged.

`OFF` suppresses only the three aircraft-owned automatic calls to
`sim/ground_ops/jetway`:

1. boarding and ground-service start;
2. boarding completion;
3. post-landing ground-service start.

Manual jetway operation through X-Plane, key or joystick assignments,
hardware and other plugins remains available. The native simulator command is
not replaced or intercepted. Jetway detection, door selection, boarding state
and the remaining ground-service logic retain the original aircraft behavior.

The option is independent of the existing aircraft `AIRSTAIRS` setting.

## Supported baselines

- Stock Zibo 4.05.35 Lua files for X-Plane 12.
- Stock LevelUp 737NG Series V2.S1 Lua files for X-Plane 12.
- Stock LevelUp 737NG Series V2.S1.50 Lua files for X-Plane 12.
- Known source hashes are declared in `package-manifest.json` and documented in
  `SOURCE.md` for release identification.

The installer reports a known FMS/Tablet baseline pair when the hashes match.
For locally modified or newer files, it instead validates every owned source
or installed block structurally. Missing, duplicated or modified owned blocks
remain a hard error; unrelated patch blocks do not prevent installation.

## Install

Close X-Plane, download or clone this repository, then run:

```bash
python3 z_Install.py check --aircraft-root "/path/to/aircraft-root"
python3 z_Install.py install --aircraft-root "/path/to/aircraft-root"
```

On Windows, use `py` or `python` if `python3` is unavailable. Restart X-Plane
after installation and save the Tablet settings normally when the desired
value has been selected.

## Verify and uninstall

```bash
python3 z_Install.py verify --aircraft-root "/path/to/aircraft-root"
python3 z_Install.py uninstall --aircraft-root "/path/to/aircraft-root"
```

Installation creates exact audit backups under `.zibo-auto-jetway-patch/backups/`
inside the selected aircraft root. Uninstall reverses only AUTO JETWAY-owned
blocks and preserves unrelated changes made before or after installation.

The historical package ID and state-directory name are intentionally retained
so an existing v0.1.0 Zibo installation remains verifiable and safely
uninstallable with v0.2.3. The AUTO JETWAY source transformation itself is
unchanged for that Zibo baseline, so reinstalling the feature is unnecessary.

See `INSTALLATION.md` for the complete procedure and `RUNTIME_TEST_PLAN.md`
for the requested simulator acceptance tests.

## Package contract

`package-manifest.json` uses schema version 3 and declares every target,
payload hash and known source/result baseline pairs. The only operation is an
exact UTF-8 text replacement with an exact inverse that preserves each source
file's original line endings and final-newline convention.

This small declarative operation set is suitable for later integration into a
manifest-driven aircraft maintenance tool.

## Validation status

The unchanged patch payload has been validated for unique structural
application and byte-exact reversal against the effective Zibo 4.05.35 files.
Earlier automated coverage remains available for both supported LevelUp
baselines; a complete v0.2.3 suite rerun remains pending. Simulator-runtime
validation of the stock Lua packages remains open.

## Disclaimer

This project is unofficial and is not supported by Zibo, LevelUp or Laminar
Research. Keep a separate aircraft backup and use the patch at your own risk.
