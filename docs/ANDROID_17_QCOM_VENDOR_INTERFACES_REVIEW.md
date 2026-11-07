# Android 17 Qualcomm vendor interface contract review — mondrian

Scope: independent PixelExperience-Reborn AOSP Android 17 for POCO F5 Pro / Redmi K60 (mondrian, SM8475). **Not a complete vendor HAL port.** Do not import any other ROM tree.

## Verified historical source
- PE-Reborn branch `seventeen`: commit `07b8b1a504692a43265c8c379e8dfa37932d2605`, Git tree `ef1584a36b910de64fa72ccd8c0107811b4914f1`, November 8, 2023; 447 source files in 16 functional groups.
- Mixed HIDL interfaces: Qualcomm Bluetooth audio 1.0/2.0/2.1, display composer/allocator/config, FM 1.0, camera, perf, Wi-Fi and others. The Android 17 AOSP public standard HAL contracts are **not** replaceable by a QTI extension.
- Existing Qualcomm-specific AIDL includes `vendor.qti.hardware.bluetooth.audio` frozen V1 (7 annotated types, checked-in hash), plus camera AON/offlinecamera, debugutils, qspa and others. The Bluetooth extension is **not** the platform `android.hardware.bluetooth.audio` contract.
- Mixed archive includes `fm/1.0` `vendor.qti.hardware.fm@1.0` and an HIDL package root in `Android.bp`. **Do not import the entire historical interfaces tree to the mondrian build**: FM is explicitly out of product scope, and the old HIDL graphics paths have not been validated against a modern AIDL/Composer3 vendor stack.

## Real source fix in the PE-Reborn review branch
- `bluetooth_audio/aidl/Android.bp`: explicitly add `stability: "vintf"` for the already `@VintfStability`-annotated Qualcomm vendor Bluetooth audio AIDL V1 API.
- Normalize the source glob to `vendor/qti/hardware/bluetooth/audio/*.aidl`. Leave the frozen V1 API and `.hash` unchanged. No ABI bump or claimed new Bluetooth feature.
- `tests/check_android17_qcom_interfaces.py` enforces the matching Soong/AIDL declarations and preserves the original frozen contract. The test **also explicitly detects the archived FM HIDL tree as a blocker**; it is not a proof of hardware absence or Android 17 Soong success.

## Decision and remaining blockers
The 2023 umbrella source is **not activated in active AOSP17 manifest profiles**. AOSP17 `hardware/interfaces` remains authoritative. If actual mondrian vendor blobs require a specific QTI private interface, independently select an owner and compatible version using exact binary/HAL dependency evidence; audit Soong namespace and generated library collisions, VINTF/FCM, vendor ABI, SELinux, AIDL freezing/NDK, and device CTS/VTS before inclusion. Modern Qualcomm-derived implementations and LF52406's LineageOS-based device information may be compared **read-only**, not imported as a ROM base or copied.

Official architecture: https://source.android.com/docs/core/architecture/aidl/aidl-hals and https://source.android.com/docs/core/architecture/aidl/stable-aidl

**Status:** real source fix plus host-only tests; no Android 17 full build, service registration, verified Bluetooth audio route, vendor ABI proof or mondrian boot test.
