# Installation and removal

## Requirements

- A structurally compatible Zibo or LevelUp installation. Known supported
  baselines are Zibo 4.05.35, LevelUp V2.S1 and LevelUp V2.S1.50.
- Python 3.10 or newer.
- X-Plane closed while files are changed.
- A separate recoverable aircraft backup.

## Preflight

From this repository, run:

```bash
python3 z_Install.py check --aircraft-root "/path/to/aircraft-root"
```

`check` verifies the manifest and payloads, reports a known paired FMS/Tablet
baseline when available, and validates every owned source or installed block
without changing the aircraft. Missing, duplicated or modified owned blocks
cause a safe failure. Unrelated patch blocks are retained.

## Install

```bash
python3 z_Install.py install --aircraft-root "/path/to/aircraft-root"
```

The installer creates exact audit backups, stages both patched results and
records their hashes. It rolls back the transaction if either replacement
fails.

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

Uninstall first verifies that every AUTO JETWAY-owned replacement is still
present and unmodified. It then reverses only those replacements. Later
Zibo/LevelUp changes and unrelated patch blocks remain untouched; the original
backups are retained as audit/recovery material rather than copied blindly.

An `AUTO JETWAY` line left in an existing config file is harmless because an
unpatched upstream version ignores unknown keys.

Existing v0.1.0 Zibo installations use the same package ID and state directory.
They remain verifiable and uninstallable with this installer; no feature
reinstall is required.

Existing v0.2.2 installations already contain the same patch payload and do
not require reinstallation for v0.2.3. The newer release corrects baseline
identification and provenance metadata only.

## Installation ownership

MTK and the standalone installer remain separate supported installation methods.
Use the same owner for updates and removal. To switch, uninstall through the
current owner first, then install through the other. Neither installer adopts
already patched files on the strength of matching hashes alone.

Keep the complete extracted package, including `standalone_guard.py` and
`standalone-ownership.json`. The standalone installer checks its recorded
original backups and stops if MTK owns this patch or a shared target file.
Unknown, duplicate or incomplete patch blocks and unowned companion files also
block the operation. Other correctly installed patches are preserved.

A failed operation restores the bytes it changed. If the process is interrupted,
keep the `.patch-ownership` receipt, transaction journal and lock, together with
any older patch backup/state directory. Do not delete them to retry. Ask for
support before changing those files.

Older standalone installs without a complete receipt are not automatically
migrated. Remove them using the installer and original backups that created
them. This source change affects installation checks only; runtime payloads and
patch versions are unchanged. Installer and recovery tests cover these checks.
