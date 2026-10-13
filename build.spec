# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for RadioCastOS Windows builds."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

ROOT = Path(SPEC).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"

import sys
sys.path.insert(0, str(SRC))
from version import APP_VERSION  # single version source (src/version.py)  # noqa: E402
print(f"Building RadioCastOS {APP_VERSION}")

ENTRY = SRC / "main.py"
ICON = ASSETS / "icon.ico"
FFMPEG = ASSETS / "ffmpeg.exe"
FFPLAY = ASSETS / "ffplay.exe"
FFPROBE = ASSETS / "ffprobe.exe"   # optional: lets the Emergency Media Vault read exact durations

if not ENTRY.exists():
    raise SystemExit(f"Missing application entry point: {ENTRY}")

if not FFMPEG.exists():
    raise SystemExit(
        f"Missing {FFMPEG}. Download/stage the Windows FFmpeg runtime before building."
    )

if not FFPLAY.exists():
    raise SystemExit(
        f"Missing {FFPLAY}. Download/stage the Windows FFmpeg runtime before building."
    )

# All application modules are imported from src. Listing them explicitly keeps
# the build deterministic. collect_submodules('mutagen') prevents optional
# metadata readers from disappearing from the frozen application.
APP_MODULES = [
    "ai_ducker",
    "ai_presenter",
    "ai_presenter_autopilot",
    "offline_voice",
    "piper_voice",
    "kokoro_voice",
    "offline_script",
    "presenter_persona",
    "voice_clone",
    "tts_runtime",
    "ai_queue",
    "broadcast_intelligence",
    "app_gui",
    "asrun",
    "config",
    "console_logic",
    "console_icons",
    "credentials",
    "devices",
    "dragdrop",
    "gui_ai_console",
    "gui_ai_queue",
    "gui_automation",
    "gui_control",
    "gui_dragdrop",
    "levels",
    "library",
    "log_setup",
    "mixer",
    "player",
    "programme_air_report",
    "preflight",
    "recorder",
    "scheduler",
    "shoutcast_v1",
    "source_client",
    "connection_test",
    "listeners",
    "show_builder",
    "streamer",
    "theme",
    "ui_kit",
    "theme_polish",
    "version",
    "web_news",
    "stream_presets",
    "station_status",
    "gui_stations",
    "ops_ui",
    "gui_fleet",
    "fleet",
    "gui_alerts",
    "alerts",
    "gui_monitor",
    "stream_monitor",
    "remote_control",
    "gui_remote",
    "remote_agent",
    "status_page",
    "local_secrets",
    "licensing",
    "gui_license",
    "admin_tools",
    "audio_asset_workflow",
    "audio_codecs",
    "automation_pro",
    "broadcast_continuity",
    "broadcast_core",
    "broadcast_engine",
    "broadcast_playout_adapter",
    "scheduled_playout",
    "broadcast_queue",
    "commercial_compliance",
    "commercial_revenue",
    "commercial_traffic_intelligence",
    "copilot_intelligence",
    "copilot_voice",
    "deployment",
    "diagnostics",
    "emergency",
    "emergency_media_vault",
    "executive_operations",
    "failover_readiness",
    "gui_analytics",
    "gui_emergency",
    "countdown_timers",
    "gui_intelligence_studio",
    "gui_pads",
    "gui_campaign_form",
    "commercial_form",
    "gui_live_show_copilot",
    "gui_presenter_command",
    "gui_roles",
    "incident_center",
    "intelligence_operations",
    "intelligence_orchestration",
    "intelligence_runtime",
    "jingle_pads",
    "live_show_copilot",
    "playout_engine",
    "preproduce",
    "reliability",
    "roles",
    "show_intelligence",
    "station_health_center",
    "station_profiles",
]

HIDDEN_IMPORTS = APP_MODULES + collect_submodules("mutagen")

# Optional: tkinterdnd2 lets users drop files from Explorer onto the playlist.
# Its native tkdnd library must ship with the app; if the package is not
# installed the build still succeeds and Explorer drops are simply unavailable.
try:
    import tkinterdnd2  # noqa: F401
    HIDDEN_IMPORTS += ["tkinterdnd2"]
    TKDND_DATA = collect_data_files("tkinterdnd2")
except Exception:
    TKDND_DATA = []

binaries = [
    (str(FFMPEG), "."),
    (str(FFPLAY), "."),
]
if FFPROBE.exists():
    binaries.append((str(FFPROBE), "."))

a = Analysis(
    [str(ENTRY)],
    pathex=[str(SRC)],
    binaries=binaries,
    datas=([(str(ICON), ".")] if ICON.exists() else []) + [(str(ASSETS / "clone_worker.py"), ".")] + TKDND_DATA,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RadioCastOS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON) if ICON.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="RadioCastOS",
)
