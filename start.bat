@echo off
cd /d "%~dp0"
echo Starting PassForge...
echo Open http://127.0.0.1:18080 in your browser
echo Press Ctrl+C to stop
echo.
uv run python app.py
pause
