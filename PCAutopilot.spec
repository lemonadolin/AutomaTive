# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for PC Autopilot.

Builds a single-folder Windows app (recommended for reliability -- faster
startup and fewer AV false positives than one-file). The main artifact is
dist/PCAutopilot/PCAutopilot.exe.

We deliberately do NOT strip DLLs or exclude native modules; hidden imports for
the Windows audio / COM / win32 stack are declared so nothing breaks at runtime.
Build on Windows:  pyinstaller PCAutopilot.spec  (or run build.bat)
"""

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
# Windows-native integrations (present only on the Windows build machine).
for mod in ("pycaw", "comtypes", "win32gui", "win32process", "win32con",
            "win32api", "keyring.backends.Windows"):
    try:
        __import__(mod)
        hiddenimports.append(mod)
    except Exception:
        pass
hiddenimports += collect_submodules("keyring.backends")

block_cipher = None

import os as _os
_datas = []
if _os.path.isdir(_os.path.join("pcautopilot", "resources")):
    _datas.append((_os.path.join("pcautopilot", "resources"),
                   _os.path.join("pcautopilot", "resources")))

a = Analysis(
    ["run_app.py"],
    pathex=[],
    binaries=[],
    datas=_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "PySide6.QtWebEngineCore"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PCAutopilot",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # GUI app -- no console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="pcautopilot/resources/icon.ico" if __import__("os").path.exists(
        "pcautopilot/resources/icon.ico") else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="PCAutopilot",
)
