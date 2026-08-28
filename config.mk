# Copyright (C) 2017-2025 crDroid Android Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

LOCAL_PATH := $(call my-dir)
include $(call all-subdir-makefiles,$(LOCAL_PATH))

ifeq ($(TARGET_HAS_UDFPS),true)
PRODUCT_PACKAGES += \
    UdfpsIcons \
    UdfpsAnimations
endif

# Custom Overlays
PRODUCT_PACKAGES += \
    PixelLauncherOverlayCustom

# Fonts
PRODUCT_PACKAGES += \
    fonts_customization.xml \
    FontRalewayOverlay\
    ClockFontRalewayOverlay

# Navbar styles
PRODUCT_PACKAGES += \
    NavbarAndroidOverlay \
    NavbarAsusOverlay \
    NavbarDoraOverlay \
    NavbarMotoOverlay \
    NavbarNexusOverlay \
    NavbarOldOverlay \
    NavbarOnePlusOverlay \
    NavbarOneUiOverlay \
    NavbarSammyOverlay \
    NavbarTecnoCamonOverlay \
    NavbarAndroidOverlayPixel \
    NavbarAsusOverlayPixel \
    NavbarDoraOverlayPixel \
    NavbarMotoOverlayPixel \
    NavbarNexusOverlayPixel \
    NavbarOldOverlayPixel \
    NavbarOnePlusOverlayPixel \
    NavbarOneUiOverlayPixel \
    NavbarSammyOverlayPixel \
    NavbarTecnoCamonOverlayPixel

# Icon packs
include vendor/addons/themes/iconpacks/iconpack_packages.mk

# Status bar Wi‑Fi icon styles
PRODUCT_PACKAGES += \
    WifiIconCompactOverlay \
    AuroraWiFiOverlay \
    BarsWiFiOverlay \
    DoraWiFiOverlay \
    FaintUIWiFiOverlay \
    ForlornWiFiOverlay \
    GradiconWiFiOverlay \
    InsideWiFiOverlay \
    NothingDotWiFiOverlay \
    PlumpyWiFiOverlay \
    RoundWiFiOverlay \
    SneakyWiFiOverlay \
    StrokeWiFiOverlay \
    WavyWiFiOverlay \
    WeedWiFiOverlay \
    XperiaWiFiOverlay \
    ZigZagWiFiOverlay

# Status bar cellular / signal icon styles
PRODUCT_PACKAGES += \
    SignalIconCompactOverlay \
    AquariumSignalOverlay \
    AuroraSignalOverlay \
    BarsSignalOverlay \
    ButterflySignalOverlay \
    CircleSignalOverlay \
    DaunSignalOverlay \
    DecSignalOverlay \
    DeepSignalOverlay \
    DoraSignalOverlay \
    EqualSignalOverlay \
    FaintUISignalOverlay \
    FanSignalOverlay \
    ForlornSignalOverlay \
    GradiconSignalOverlay \
    HuaweiSignalOverlay \
    InsideSignalOverlay \
    IosSignalOverlay \
    MiniSignalOverlay \
    NothingDotSignalOverlay \
    PillsSignalOverlay \
    PlumpySignalOverlay \
    RelSignalOverlay \
    RomanSignalOverlay \
    RoundSignalOverlay \
    ScrollSignalOverlay \
    SeaSignalOverlay \
    SneakySignalOverlay \
    StackSignalOverlay \
    StrokeSignalOverlay \
    WannuiSignalOverlay \
    WavySignalOverlay \
    WindowsSignalOverlay \
    WingSignalOverlay \
    XperiaSignalOverlay \
    ZigZagSignalOverlay

# Themes
PRODUCT_PACKAGES += \
    AndroidBlackThemeOverlay \
    BackGestureDotTrailOverlay \
    BatteryStyleSmileyOverlay

PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,*,vendor/addons/prebuilt/product/fonts,$(TARGET_COPY_OUT_PRODUCT)/fonts)

# AlphaVisuals: theme catalog on product image (not APK resources; regenerate with themes/tools/adapt_ax_catalog.py)
PRODUCT_COPY_FILES += \
    vendor/addons/themes/overlay_catalog.json:$(TARGET_COPY_OUT_PRODUCT)/etc/assets/overlay_catalog.json
