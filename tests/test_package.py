from __future__ import annotations

import json
import unittest
from pathlib import Path

from patchlib import sha256_path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class PackageContractTests(unittest.TestCase):
    def test_manifest_payload_integrity_and_target_closure(self) -> None:
        manifest = json.loads(
            (REPOSITORY_ROOT / "package-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(3, manifest["schemaVersion"])
        self.assertEqual("compatibilityPackage", manifest["packageType"])
        self.assertEqual("0.2.3", manifest["packageVersion"])
        self.assertEqual(
            ["zibo-737ng", "levelup-737ng"],
            manifest["supportedProducts"],
        )
        payloads = {item["path"]: item for item in manifest["payloads"]}
        targets = manifest["targets"]
        self.assertEqual(set(payloads), {target["payload"] for target in targets})
        self.assertEqual(2, len(targets))
        target_paths = {target["relativePath"] for target in targets}
        baselines = manifest["supportedBaselines"]
        self.assertEqual(
            {"zibo-4.05.35", "levelup-v2.s1", "levelup-v2.s1.50"},
            {baseline["id"] for baseline in baselines},
        )
        zibo = next(
            baseline for baseline in baselines if baseline["id"] == "zibo-4.05.35"
        )
        self.assertEqual(
            {
                "plugins/xlua/scripts/B738.a_fms/B738.a_fms.lua": {
                    "sourceSha256": "ff313b0e88c62845ad1c4a2b1f4bd599f57d8799e8d6707bfc10a3369fd63a8e",
                    "resultSha256": "6dc07cac5cd89c4645890ed4d29f0bf1c6ccddba62cc31b2be827bb0f7c8f9d6",
                },
                "plugins/xlua/scripts/B738.tablet/B738.tablet.lua": {
                    "sourceSha256": "7c9e445a2a002f1ef81a0b738ad3c3b791a63c2c313d44d993517e260cd32141",
                    "resultSha256": "ce0e634c979696c0f17a9c2a2fd69bfe72b243b2c266fce6ea1486951ffca76d",
                },
            },
            {
                item["relativePath"]: {
                    "sourceSha256": item["sourceSha256"],
                    "resultSha256": item["resultSha256"],
                }
                for item in zibo["files"]
            },
        )
        fingerprints = set()
        for baseline in baselines:
            files = {item["relativePath"]: item for item in baseline["files"]}
            self.assertEqual(target_paths, set(files))
            fingerprint = tuple(
                sorted((relative, item["sourceSha256"]) for relative, item in files.items())
            )
            self.assertNotIn(fingerprint, fingerprints)
            fingerprints.add(fingerprint)
            for item in files.values():
                self.assertEqual(64, len(item["sourceSha256"]))
                self.assertEqual(64, len(item["resultSha256"]))
        for relative, metadata in payloads.items():
            path = REPOSITORY_ROOT / relative
            self.assertTrue(path.is_file())
            self.assertEqual(metadata["size"], path.stat().st_size)
            self.assertEqual(metadata["sha256"], sha256_path(path))

        self.assertEqual(1, len(manifest["modules"]))
        module = manifest["modules"][0]
        self.assertEqual("auto-jetway", module["moduleId"])
        self.assertEqual("optional", module["policy"])
        self.assertFalse(module["defaultEnabled"])
        self.assertEqual(payloads, {item["path"]: item for item in module["payloads"]})
        self.assertEqual(targets, [
            {key: value for key, value in target.items() if key != "sourceSha256"}
            for target in module["targets"]
        ])

    def test_repository_does_not_ship_complete_aircraft_targets(self) -> None:
        forbidden = {
            "B738.a_fms.lua",
            "B738.tablet.lua",
            "zibomod.xpl",
        }
        shipped = {path.name for path in REPOSITORY_ROOT.rglob("*") if path.is_file()}
        self.assertTrue(forbidden.isdisjoint(shipped))


if __name__ == "__main__":
    unittest.main()
