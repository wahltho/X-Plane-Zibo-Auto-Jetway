# Installation and removal

## Requirements

- An unmodified stock Zibo 4.05.35 installation.
- Python 3.10 or newer.
- X-Plane closed while files are changed.
- A separate recoverable aircraft backup.

## Preflight

From this repository, run:

```bash
python3 z_Install.py check --aircraft-root "/path/to/B737-800X"
```

`check` verifies the manifest, payloads, source hashes and generated result
hashes without changing the aircraft. A failure means the target is missing,
modified or not the supported release.

## Install

```bash
python3 z_Install.py install --aircraft-root "/path/to/B737-800X"
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
python3 z_Install.py verify --aircraft-root "/path/to/B737-800X"
```

## Uninstall

Close X-Plane and run:

```bash
python3 z_Install.py uninstall --aircraft-root "/path/to/B737-800X"
```

Uninstall first verifies that the installed Lua files still match the recorded
installed hashes. This prevents silently overwriting later Zibo updates or
manual edits. Successful uninstall restores both original files byte-for-byte.

An `AUTO JETWAY` line left in an existing config file is harmless because an
unpatched upstream version ignores unknown keys.
