@echo off
cd /d "%~dp0"
echo Starting WeakPass...
echo Open http://127.0.0.1:8089 in your browser
echo Press Ctrl+C to stop
echo.
uv run python app.py
pause
