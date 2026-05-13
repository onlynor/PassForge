@echo off
cd /d "%~dp0"
echo ========================================
echo   Building WeakPass exe with PyInstaller
echo ========================================
echo.

REM Kill running WeakPass if exists
taskkill /f /im WeakPass.exe >nul 2>&1

REM Install PyInstaller if not present
uv run pip install pyinstaller --quiet

echo Building...
uv run pyinstaller ^
    --onefile ^
    --noconsole ^
    --name WeakPass ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import flask ^
    --hidden-import jinja2 ^
    --hidden-import werkzeug ^
    --hidden-import tkinter ^
    app.py

echo.
if exist dist\WeakPass.exe (
    echo ========================================
    echo   Build successful!
    echo   Output: dist\WeakPass.exe
    echo ========================================
) else (
    echo Build failed. Check the output above.
)
pause
