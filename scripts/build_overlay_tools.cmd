@echo off
cd /d "%~dp0.."
uv sync
uv run pyinstaller scripts\OverlayTools.spec
echo Done!