# Installation Guide for macOS

## Download
1. Go to [Releases](https://github.com/J4GitHub1/Adrian-s-PDF-Manipulator/releases)
2. Download **`AdriansPDFManipulator-macOS.zip`** from the latest release
3. Double-click the zip to extract `AdriansPDFManipulator.app`

## Installation
Drag `AdriansPDFManipulator.app` to your **Applications** folder (optional).

## First Launch (IMPORTANT!)

⚠️ **Don't double-click!** macOS will block the app because it's not from the App Store.

### Method 1: Right-Click to Open
1. **Right-click** (or Control+click) on `AdriansPDFManipulator.app`
2. Select **"Open"**
3. Click **"Open"** in the security dialog
4. ✅ Done! The app will open.

After this first time, you can double-click normally.

### Method 2: Terminal Command
If Method 1 doesn't work:
```bash
xattr -cr /path/to/AdriansPDFManipulator.app
```
Then double-click the app.

## Usage
Once opened, the app is straightforward:
1. Browse for PDF files
2. Enter search terms (comma-separated)
3. Choose options (AND/OR logic, case sensitivity, page buffer)
4. Extract matching pages

See the [main README](README.md) for detailed features.

## Troubleshooting

**"App is damaged and can't be opened"**
- Run: `xattr -cr /path/to/AdriansPDFManipulator.app`

**"No application is set to open the document"**
- The file is a `.app` bundle, not a `.dmg`. Just right-click → Open.

**Still having issues?**
- Open an issue: https://github.com/J4GitHub1/Adrian-s-PDF-Manipulator/issues
