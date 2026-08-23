from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from patchlib import PatchError, apply_exact_text_replacements


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPOSITORY_ROOT / "z_Install.py"
TARGETS = (
    "plugins/xlua/scripts/B738.a_fms/B738.a_fms.lua",
    "plugins/xlua/scripts/B738.tablet/B738.tablet.lua",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TextPatchUnitTests(unittest.TestCase):
    def test_ambiguous_original_block_is_rejected(self) -> None:
        spec = {
            "format": "exact-text-replacements-v1",
            "replacements": [
                {
                    "name": "ambiguous",
                    "oldLines": ["old"],
                    "newLines": ["new"],
                }
            ],
        }
        with self.assertRaisesRegex(PatchError, "original=2"):
            apply_exact_text_replacements(b"old\nold\n", spec)

    def test_line_endings_and_final_newline_are_preserved(self) -> None:
        spec = {
            "format": "exact-text-replacements-v1",
            "replacements": [
                {
                    "name": "replace",
                    "oldLines": ["one"],
                    "newLines": ["one", "two"],
                }
            ],
        }
        self.assertEqual(
            b"one\r\ntwo\r\nthree\r\n",
            apply_exact_text_replacements(b"one\r\nthree\r\n", spec),
        )


class InstallerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        upstream = os.environ.get("ZIBO_40535_ROOT")
        if not upstream:
            raise unittest.SkipTest("Set ZIBO_40535_ROOT for integration tests")
        cls.upstream = Path(upstream)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="zibo-auto-jetway-test-")
        self.aircraft_root = Path(self.temporary.name) / "B737-800X"
        for relative in TARGETS:
            source = self.upstream / relative
            destination = self.aircraft_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        self.original_hashes = {
            relative: sha256(self.aircraft_root / relative) for relative in TARGETS
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_installer(self, action: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                action,
                "--aircraft-root",
                str(self.aircraft_root),
            ],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, msg=result.stdout + result.stderr)
        return result

    def test_check_install_verify_and_uninstall(self) -> None:
        self.run_installer("check")
        self.assertEqual(
            self.original_hashes,
            {relative: sha256(self.aircraft_root / relative) for relative in TARGETS},
        )

        self.run_installer("install")
        self.run_installer("verify")
        self.run_installer("install")

        state = json.loads(
            (self.aircraft_root / ".zibo-auto-jetway-patch/state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("wahltho.zibo-40535.auto-jetway", state["packageId"])
        self.assertEqual("0.1.0", state["packageVersion"])
        self.assertEqual(2, len(state["files"]))

        fms_bytes = (self.aircraft_root / TARGETS[0]).read_bytes()
        tablet_bytes = (self.aircraft_root / TARGETS[1]).read_bytes()
        fms = fms_bytes.decode("utf-8")
        tablet = tablet_bytes.decode("utf-8")

        self.assertEqual(fms_bytes.count(b"\n"), fms_bytes.count(b"\r\n"))
        self.assertEqual(0, tablet_bytes.count(b"\r\n"))
        self.assertEqual(1, fms.count('create_dataref("laminar/B738/tab/auto_jetway"'))
        self.assertIn('fms_txt == "AUTO JETWAY" and xfile_path_cfg == ""', fms)
        self.assertIn(
            'if xfile_path_cfg == "" then\r\n\t\t\t\tfms_line = "AUTO JETWAY',
            fms,
        )
        self.assertEqual(1, tablet.count('find_dataref("laminar/B738/tab/auto_jetway"'))
        self.assertEqual(3, tablet.count("B738CMD_jetways_toggle:once()"))
        self.assertEqual(3, tablet.count("if B738DR_auto_jetway ~= 0 then"))
        self.assertEqual(1, tablet.count('find_command("sim/ground_ops/jetway")'))
        self.assertNotIn('create_command("sim/ground_ops/jetway"', tablet)

        luac = shutil.which("luac")
        if luac:
            syntax = subprocess.run(
                [luac, "-p", str(self.aircraft_root / TARGETS[0]), str(self.aircraft_root / TARGETS[1])],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, syntax.returncode, msg=syntax.stdout + syntax.stderr)

        installed_tablet = (self.aircraft_root / TARGETS[1]).read_bytes()
        (self.aircraft_root / TARGETS[1]).write_bytes(installed_tablet + b"-- later change\n")
        refused = self.run_installer("uninstall", expected=1)
        self.assertIn("Installed file was changed after installation", refused.stderr)
        (self.aircraft_root / TARGETS[1]).write_bytes(installed_tablet)

        self.run_installer("uninstall")
        self.assertEqual(
            self.original_hashes,
            {relative: sha256(self.aircraft_root / relative) for relative in TARGETS},
        )
        self.assertFalse((self.aircraft_root / ".zibo-auto-jetway-patch").exists())
        self.run_installer("check")

    def test_modified_source_is_rejected_without_writes(self) -> None:
        tablet = self.aircraft_root / TARGETS[1]
        tablet.write_bytes(tablet.read_bytes() + b"-- local modification\n")
        before = {relative: sha256(self.aircraft_root / relative) for relative in TARGETS}
        result = self.run_installer("check", expected=1)
        self.assertIn("Unsupported or modified source file", result.stderr)
        self.assertEqual(
            before,
            {relative: sha256(self.aircraft_root / relative) for relative in TARGETS},
        )


if __name__ == "__main__":
    unittest.main()
