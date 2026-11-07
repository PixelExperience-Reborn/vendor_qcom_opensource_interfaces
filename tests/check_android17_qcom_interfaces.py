#!/usr/bin/env python3
"""Host-only contract checks for the PE-Reborn Qualcomm interface review.

This does not assert Android 17 Soong build, vendor ABI or physical device support.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
BT = ROOT / "bluetooth_audio" / "aidl"
AIDL_PATH = BT / "vendor/qti/hardware/bluetooth/audio"


class Aosp17QualcommInterfaceChecks(unittest.TestCase):
    def test_bluetooth_audio_has_a_vintf_stable_ndk_interface(self):
        bp = (BT / "Android.bp").read_text(encoding="utf-8")
        self.assertEqual(bp.count('name: "vendor.qti.hardware.bluetooth.audio"'), 1)
        self.assertIn('stability: "vintf"', bp)
        self.assertIn('vendor_available: true', bp)
        self.assertIn('cpp: {\n            enabled: false,', bp)
        self.assertIn('version: "1"', bp)
        self.assertIn('"vendor/qti/hardware/bluetooth/audio/*.aidl"', bp)
        self.assertNotIn('"vendor/qti//hardware/', bp)

    def test_all_original_vendor_types_are_vintf_stable(self):
        sources = sorted(AIDL_PATH.glob("*.aidl"))
        self.assertEqual(len(sources), 7)
        for source in sources:
            with self.subTest(type=source.name):
                code = source.read_text(encoding="utf-8")
                self.assertIn("package vendor.qti.hardware.bluetooth.audio;", code)
                self.assertIn("@VintfStability", code)

    def test_frozen_v1_api_remains_available(self):
        frozen = BT / "aidl_api/vendor.qti.hardware.bluetooth.audio/1"
        self.assertTrue(re.fullmatch(
            r"[0-9a-f]{40}", (frozen / ".hash").read_text().strip()))
        self.assertEqual(
            len(list(frozen.glob("vendor/qti/hardware/bluetooth/audio/*.aidl"))),
            7,
        )

    def test_historical_fm_hidl_requires_separate_product_exclusion(self):
        # This mixed 2023 tree has FM HIDL. It is NOT safe to import wholesale.
        fm = (ROOT / "fm/1.0/Android.bp").read_text(encoding="utf-8")
        self.assertIn('name: "vendor.qti.hardware.fm@1.0"', fm)
        root = (ROOT / "Android.bp").read_text(encoding="utf-8")
        self.assertIn('name: "vendor.qti.hardware.fm"', root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
