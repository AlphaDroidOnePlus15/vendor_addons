#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 AlphaDroid
# SPDX-License-Identifier: Apache-2.0
"""Adapt Ax Theme Store repository JSON (v3) to local overlay_catalog.json (v4).

Reads short component ids and normalizes android.theme.customization.* keys for ThemeEngine.
Default input: ../ax_themes_repository.source.json
Default output: ../overlay_catalog.json (installed to product/etc/assets/ via vendor/addons/config.mk).
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PREFIX = "android.theme.customization."

# Legacy short id -> full ThemeEngine / overlay manifest category
SHORT_TO_FULL: dict[str, str] = {
    "signal": PREFIX + "signal_icon",
    "wifi": PREFIX + "wifi_icon",
    "back_gesture": PREFIX + "back_gesture",
    "charging_animation": PREFIX + "charging_animation",
    "battery_style": PREFIX + "battery_style",
}

# Legacy component section id -> catalog component id (matches overlay_catalog.template.json)
LEGACY_COMPONENT_ID: dict[str, str] = {
    "signal": "signal_icon",
    "wifi": "wifi_icon",
    "back_gesture": "back_gesture",
    "charging_animation": "charging_animation",
    "battery_style": "battery_style",
}


def normalize_component_id(raw: str) -> str:
    if raw.startswith(PREFIX):
        return raw
    return SHORT_TO_FULL.get(raw, PREFIX + raw if raw else raw)


def overlay_label(full_cid: str) -> str:
    if full_cid.endswith(".signal_icon"):
        return "Signal"
    if full_cid.endswith(".wifi_icon"):
        return "Wi‑Fi"
    if full_cid.endswith(".icon_pack.android"):
        return "Android"
    if full_cid.endswith(".icon_pack.systemui"):
        return "System UI"
    if full_cid.endswith(".icon_pack.settings"):
        return "Settings"
    if full_cid.endswith(".icon_pack.launcher"):
        return "Launcher"
    if full_cid.endswith(".icon_pack.themepicker"):
        return "Theme Picker"
    if full_cid.endswith(".charging_animation"):
        return "Charging animation"
    if full_cid.endswith(".battery_style"):
        return "Battery style"
    if full_cid.endswith(".back_gesture"):
        return "Back gesture"
    tail = full_cid.split(".")[-1].replace("_", " ")
    return tail[:1].upper() + tail[1:] if tail else full_cid


def target_package_for(full_cid: str) -> str:
    if ".icon_pack.android" in full_cid or full_cid.endswith(".wifi_icon") or full_cid.endswith(
        ".signal_icon"
    ):
        return "android"
    return "com.android.systemui"


def normalize_targets(raw_targets: list[str], full_cid: str) -> list[str]:
    out: list[str] = []
    for t in raw_targets:
        if t.startswith(PREFIX):
            out.append(t)
        else:
            out.append(SHORT_TO_FULL.get(t, full_cid))
    if not out:
        out = [full_cid]
    # Deduplicate preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for x in out:
        if x not in seen:
            seen.add(x)
            deduped.append(x)
    return deduped


def adapt_overlay(ov: dict[str, Any], keep_download_meta: bool) -> dict[str, Any]:
    raw_cid = ov.get("componentId", "")
    full_cid = normalize_component_id(raw_cid)
    pkg = ov.get("packageName", "")
    row: dict[str, Any] = {
        "componentId": full_cid,
        "packageName": pkg,
        "targetPackage": target_package_for(full_cid),
        "label": overlay_label(full_cid),
        "targets": normalize_targets(list(ov.get("targets") or []), full_cid),
    }
    if keep_download_meta:
        if ov.get("downloadUrl"):
            row["downloadUrl"] = ov["downloadUrl"]
        if "fileSize" in ov:
            row["fileSize"] = ov["fileSize"]
        if "enabled" in ov:
            row["enabled"] = ov["enabled"]
    return row


EXTRA_COMPONENTS: list[dict[str, Any]] = [
    {
        "id": "icon_pack_android",
        "name": "Icon pack (Android)",
        "description": "Themed Android icons",
        "engineCategory": PREFIX + "icon_pack.android",
        "targetPackage": "android",
        "icon": "category",
    },
    {
        "id": "icon_pack_systemui",
        "name": "Icon pack (System UI)",
        "description": "Themed System UI icons",
        "engineCategory": PREFIX + "icon_pack.systemui",
        "targetPackage": "com.android.systemui",
        "icon": "category",
    },
    {
        "id": "icon_pack_settings",
        "name": "Icon pack (Settings)",
        "description": "Themed Settings icons",
        "engineCategory": PREFIX + "icon_pack.settings",
        "targetPackage": "com.android.settings",
        "icon": "category",
    },
    {
        "id": "icon_pack_launcher",
        "name": "Icon pack (Launcher)",
        "description": "Themed Launcher icons",
        "engineCategory": PREFIX + "icon_pack.launcher",
        "targetPackage": "com.android.launcher3",
        "icon": "category",
    },
]


def adapt_components(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen_engine: set[str] = set()
    for c in components:
        lid = c.get("id", "")
        new_id = LEGACY_COMPONENT_ID.get(lid, lid)
        eng = SHORT_TO_FULL.get(lid, normalize_component_id(lid))
        row = {
            "id": new_id,
            "name": c.get("name", ""),
            "description": c.get("description", ""),
            "engineCategory": eng,
            "targetPackage": c.get("targetPackage", ""),
            "icon": c.get("icon", "palette"),
        }
        seen_engine.add(eng)
        out.append(row)
    for extra in EXTRA_COMPONENTS:
        if extra["engineCategory"] not in seen_engine:
            out.append(dict(extra))
            seen_engine.add(extra["engineCategory"])
    return out


def adapt_theme(theme: dict[str, Any], keep_download_meta: bool) -> dict[str, Any]:
    t = dict(theme)
    overlays = [adapt_overlay(o, keep_download_meta) for o in t.get("overlays") or []]
    t["overlays"] = overlays
    return t


_DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "overlay_catalog.json"

META = {
    "description": "Local overlay catalog for AlphaVisuals. Installed on device as /product/etc/assets/overlay_catalog.json (product image, not APK resources); source in vendor/addons/themes. Supplies titles, authors, categories, and ThemeEngine category keys for main + detail screens.",
    "delivery": "local",
    "authorDefault": "",
    "uiStateLabels": "enabled_disabled",
    "excludes": ["fonts"],
    "notes": [
        "Per-theme theme.author: set for real attribution; omit or empty → meta.authorDefault (empty hides \"by\" line on detail).",
        "overlay.componentId matches overlay manifest android:category (Settings.Secure / ThemeEngine).",
        "Generated by vendor/addons/themes/tools/adapt_ax_catalog.py (source: ax_themes_repository.source.json); PRODUCT_COPY_FILES installs to product/etc/assets/overlay_catalog.json.",
        "ui_styles: built-in QS/brightness decoration presets (id + author); not overlay themes.",
    ],
}

REPOSITORY = {
    "name": "Alpha vendor addons (local)",
    "description": "Bundled theme catalog co-located with vendor/addons/themes",
    "maintainer": "Alpha / AxionOS",
}

# SystemUI Settings.System `ui_style` presets (not RRO themes; see AlphaVisuals ThemeRepository.mapCatalogUiStyles).
DEFAULT_UI_STYLES: list[dict[str, str]] = [
    {"id": "system_default", "author": "AOSP"},
    {"id": "outline", "author": "AlphaDroid"},
    {"id": "neon", "author": "AlphaDroid"},
    {"id": "bevel", "author": "AlphaDroid"},
    {"id": "gradient", "author": "AlphaDroid"},
    {"id": "reflective", "author": "AlphaDroid"},
    {"id": "slash", "author": "AlphaDroid"},
    {"id": "aerogel", "author": "AlphaDroid"},
    {"id": "metallic", "author": "AlphaDroid"},
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "ax_themes_repository.source.json",
        help="Source Ax v3 JSON",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=_DEFAULT_OUTPUT,
        help="Output v4 JSON (default: vendor/addons/themes/overlay_catalog.json)",
    )
    ap.add_argument(
        "--keep-download-meta",
        action="store_true",
        help="Keep downloadUrl/fileSize/enabled on overlays (for mirrors / tooling)",
    )
    args = ap.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    version = int(data.get("version", 3))
    if version > 4:
        raise SystemExit(f"Unsupported source version {version}")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out: dict[str, Any] = {
        "version": 4,
        "lastUpdated": now,
        "meta": META,
        "repository": REPOSITORY,
        "components": adapt_components(list(data.get("components") or [])),
        "categories": data.get("categories") or [],
        "ui_styles": DEFAULT_UI_STYLES,
        "themes": [adapt_theme(t, args.keep_download_meta) for t in data.get("themes") or []],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.output} ({len(out['themes'])} themes)")


if __name__ == "__main__":
    main()
