# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PassForge is a cryptographically secure password generator with a web UI. Password generation happens entirely in the frontend using `crypto.getRandomValues()`, with a Flask backend serving the UI and providing a fallback API.

## Common Commands

```bash
# Run the application
uv run python app.py

# Run tests
uv run pytest test_generator.py -v

# Install dependencies
uv sync

# Build standalone exe
build.bat
```

## Architecture

### Frontend-First Design

The primary password generation logic lives in `static/password-generator.js` (the `PasswordGenerator` class). The backend `generator.py` is only used as a fallback via the `/api/generate` endpoint.

### Password Types

1. **Standard** - Configurable length (4-128), character sets (upper/lower/digits/special), policy templates
2. **Passphrase** - Diceware-style using `static/wordlist.js` (~2000 words), configurable word count (4-10), separator, capitalization
3. **JWT Key** - HS256 (32 bytes) / HS512 (64 bytes), displayed in Base64url/Hex/PEM formats

### Key Files

- `app.py` - Flask server, system tray icon (pystray), auto-opens browser, port 18080
- `generator.py` - Backend password generation (fallback), entropy calculation
- `static/password-generator.js` - Frontend `PasswordGenerator` class with all generation methods
- `static/wordlist.js` - Word list for passphrase generation (loaded as global `WORDLIST`)
- `templates/index.html` - Single-page UI with inline JavaScript
- `static/style.css` - Dark theme styles
- `logo/passforge.png` - Application icon (tray icon + exe)

### API Endpoints

- `GET /` - Serve main UI
- `GET /api/config` - Return configuration constants
- `POST /api/generate` - Backend password generation (fallback)
- `POST /api/shutdown` - Exit application

## Testing

Tests in `test_generator.py` cover backend generation only. Frontend logic is tested manually via the browser.

## Build & Distribution

`build.bat` uses PyInstaller to create `dist/PassForge.exe` as a standalone executable with all static assets bundled.
