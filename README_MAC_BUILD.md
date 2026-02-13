# Building Adrian's PDF Manipulator for macOS

## Prerequisites
- macOS 10.13 or later
- Python 3.8 or later (install from [python.org](https://www.python.org/downloads/) or via Homebrew: `brew install python3`)

## Quick Build Instructions

### Option 1: Simple Executable
```bash
chmod +x build_macos.sh
./build_macos.sh
```
This creates: `dist/AdriansPDFManipulator` (Unix executable)

### Option 2: Mac .app Bundle (Recommended for distribution)
```bash
chmod +x build_macos_app.sh
./build_macos_app.sh
```
This creates: `dist/Adrian's PDF Manipulator.app` (double-clickable app)

## Manual Build Instructions

If the scripts don't work, build manually:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install pypdf pyinstaller

# 3. Build
pyinstaller --onefile --windowed --name "Adrian's PDF Manipulator" AdriansPDFManipulator.py

# 4. Find your app
open dist/
```

## Distribution

The resulting `.app` file can be:
- Zipped and shared with friends
- Dragged to the Applications folder
- Distributed via DMG (requires additional tools like `create-dmg`)

## Troubleshooting

**"App is damaged and can't be opened"**: macOS Gatekeeper blocks unsigned apps. Users need to:
1. Right-click the app → "Open"
2. Click "Open" in the security dialog
OR run in Terminal: `xattr -cr "path/to/Adrian's PDF Manipulator.app"`

**Missing icon**: To add a custom icon, create an `icon.icns` file and place it in the project root before building.

**Tkinter issues**: If you get "tkinter is not installed", install Python from python.org (Homebrew Python sometimes has issues with tkinter).
