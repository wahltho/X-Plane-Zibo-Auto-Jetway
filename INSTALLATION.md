# Installation and removal

## Requirements

- An unmodified supported installation: Zibo 4.05.35, LevelUp V2.S1 or
  LevelUp V2.S1.50.
- Python 3.10 or newer.
- X-Plane closed while files are changed.
- A separate recoverable aircraft backup.

## Preflight

From this repository, run:

```bash
python3 z_Install.py check --aircraft-root "/path/to/aircraft-root"
```

`check` verifies the manifest, payloads, paired FMS/Tablet baseline and
generated result hashes without changing the aircraft. A failure means the
target is missing, modified, mixed between releases or unsupported.

## Install

```bash
python3 z_Install.py install --aircraft-root "/path/to/aircraft-root"
```

The installer backs up both complete original Lua files, stages both patched
results and records their hashes. It rolls back the transaction if either
replacement fails.

After restarting X-Plane, use:

```text
TABLET -> SETTINGS -> REALISM SETTINGS -> page 2 -> AUTO JETWAY
```

No shipped config file needs to be edited. Until Tablet settings are saved,
the missing key resolves to `ON`.

## Verify

```bash
python3 z_Install.py verify --aircraft-root "/path/to/aircraft-root"
```

## Uninstall

Close X-Plane and run:

```bash
python3 z_Install.py uninstall --aircraft-root "/path/to/aircraft-root"
```

Uninstall first verifies that the installed Lua files still match the recorded
installed hashes. This prevents silently overwriting later Zibo/LevelUp
updates or manual edits. Successful uninstall restores both original files
byte-for-byte.

An `AUTO JETWAY` line left in an existing config file is harmless because an
unpatched upstream version ignores unknown keys.

Existing v0.1.0 Zibo installations use the same package ID and state directory.
They remain verifiable and uninstallable with this installer; no feature
reinstall is required.
