# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for EyeType4You application.
"""

import os
from pathlib import Path

PROJ_ROOT = os.path.dirname(os.path.dirname(SPEC))
SRC_PATH = os.path.join(PROJ_ROOT, 'src')
ASSETS_PATH = os.path.join(PROJ_ROOT, 'assets')
DATA_PATH = os.path.join(PROJ_ROOT, 'data')

ICON_PATH = None
possible_icons = [os.path.join(ASSETS_PATH, 'eyes.ico'), os.path.join(ASSETS_PATH, 'icon.ico')]
for icon in possible_icons:
    if os.path.exists(icon):
        ICON_PATH = icon
        break

a = Analysis(
    [os.path.join(PROJ_ROOT, 'main.py')],
    pathex=[SRC_PATH],
    binaries=[],
    datas=[
        (ASSETS_PATH, 'assets'),
        (DATA_PATH, 'data'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'PyQt5.QtCore',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EyeType4You',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)
