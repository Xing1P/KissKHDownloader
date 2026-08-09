#!/usr/bin/env python3
"""
Cross-Platform Build Automation Script for KissKH Downloader.
Supports building Windows (.exe) and macOS (.app / .dmg) with version tagging.
"""

import sys
import os
import shutil
import subprocess

# Ensure app module is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.__version__ import __version__

def run_command(cmd, cwd=None):
    """Executes a command and streams output."""
    print(f"==> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"FAILED: Command failed with return code {result.returncode}")
        sys.exit(result.returncode)

def build_windows(version: str):
    """Builds Windows Executable and creates a Zip archive."""
    print(f"Building for Windows (Version v{version})...")
    run_command([sys.executable, "-m", "PyInstaller", "--noconfirm", "KissKHDownloader.spec"])

    dist_dir = os.path.abspath("dist")
    app_dir = os.path.join(dist_dir, "KissKH_Downloader")
    zip_name = f"KissKH_Downloader_v{version}_Windows"
    zip_path = os.path.join(dist_dir, f"{zip_name}.zip")

    if os.path.exists(app_dir):
        print(f"Zipping Windows package into {zip_path}...")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        shutil.make_archive(os.path.join(dist_dir, zip_name), 'zip', app_dir)
        # Also copy/overwrite standard KissKH_Downloader_Windows.zip for CI compatibility
        shutil.copyfile(zip_path, os.path.join(dist_dir, "KissKH_Downloader_Windows.zip"))
        print(f"SUCCESS: Windows build completed -> {zip_path}")
    else:
        print("ERROR: Windows build folder not found!")

def build_macos(version: str):
    """Builds macOS .app bundle and packages into .dmg image."""
    print(f"Building for macOS (Version v{version})...")
    run_command([sys.executable, "-m", "PyInstaller", "--noconfirm", "KissKHDownloader.spec"])

    dist_dir = os.path.abspath("dist")
    app_path = os.path.join(dist_dir, "KissKH_Downloader.app")
    dmg_path = os.path.join(dist_dir, f"KissKH_Downloader_v{version}_macOS.dmg")

    if not os.path.exists(app_path):
        print("ERROR: macOS .app bundle not found in dist/")
        return

    print(f"Creating macOS DMG disk image: {dmg_path}...")
    if os.path.exists(dmg_path):
        os.remove(dmg_path)

    # Use native macOS hdiutil tool
    hdi_cmd = [
        "hdiutil", "create",
        "-volname", f"KissKH Downloader v{version}",
        "-srcfolder", app_path,
        "-ov",
        "-format", "UDZO",
        dmg_path
    ]
    run_command(hdi_cmd)
    # Also copy/overwrite standard KissKH_Downloader_macOS.dmg for CI compatibility
    shutil.copyfile(dmg_path, os.path.join(dist_dir, "KissKH_Downloader_macOS.dmg"))
    print(f"SUCCESS: macOS DMG build completed -> {dmg_path}")

def main():
    version = __version__
    print(f"Starting KissKH Downloader v{version} Build System on platform: {sys.platform}")

    # Ensure output directories exist
    os.makedirs("dist", exist_ok=True)

    if sys.platform.startswith("win"):
        build_windows(version)
    elif sys.platform == "darwin":
        build_macos(version)
    else:
        print(f"Platform '{sys.platform}' detected. Running generic PyInstaller build...")
        run_command([sys.executable, "-m", "PyInstaller", "--noconfirm", "KissKHDownloader.spec"])

if __name__ == "__main__":
    main()
