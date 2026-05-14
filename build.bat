@echo off
cd /d "%~dp0"
echo ========================================
echo   Building PassForge exe with PyInstaller
echo ========================================
echo.

REM Kill running PassForge if exists
taskkill /f /im PassForge.exe >nul 2>&1

REM Install PyInstaller if not present
uv pip install pyinstaller --quiet

echo Building...
uv run python -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --name PassForge ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "logo;logo" ^
    --hidden-import flask ^
    --hidden-import jinja2 ^
    --hidden-import werkzeug ^
    --hidden-import tkinter ^
    --hidden-import pystray._win32 ^
    app.py

echo.
if exist dist\PassForge.exe (
    echo ========================================
    echo   Build successful!
    echo   Output: dist\PassForge.exe
    echo ========================================
) else (
    echo Build failed. Check the output above.
)
pause
