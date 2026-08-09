# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect static assets & data files
datas = [
    ('app/resources/fonts', 'app/resources/fonts'),
]

hiddenimports = [
    'kisskh_downloader',
    'kisskh_downloader.cli',
    'kisskh_downloader.downloader',
    'playwright',
    'sqlite3',
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtNetwork',
]

# Collect package dependencies
try:
    tmp_ret = collect_all('kisskh_downloader')
    datas += tmp_ret[0]
    hiddenimports += tmp_ret[1]
except Exception:
    pass

try:
    tmp_ret_pw = collect_all('playwright')
    datas += tmp_ret_pw[0]
    hiddenimports += tmp_ret_pw[1]
except Exception:
    pass

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='KissKH_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KissKH_Downloader',
)

# For macOS bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='KissKH_Downloader.app',
        icon=None,
        bundle_identifier='org.kisskh.downloader',
    )
