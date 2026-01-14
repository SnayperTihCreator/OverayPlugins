# -*- mode: python ; coding: utf-8 -*-
import os

# noinspection PyUnusedImports
from PyInstaller.building.build_main import Analysis, EXE, COLLECT, PYZ, logger
BASE_DIR = os.path.dirname(SPECPATH)

a = Analysis(
    [os.path.join(BASE_DIR, 'src', "overlay_tools",'overlay_tools.py')],
    pathex=[os.path.join(BASE_DIR, 'src', "overlay_tools",)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OverlayTools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
