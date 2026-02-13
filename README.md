# Adrian's PDF Manipulator

A GUI application for extracting pages from PDF files based on search terms.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## Features

- 🔍 **Search PDFs by text** - Find pages containing specific terms
- 📄 **Multiple file support** - Process multiple PDFs at once
- 🎯 **Smart matching** - AND/OR logic, case-sensitive options
- 📚 **Context pages** - Include surrounding pages (±N pages)
- 🔄 **Merge results** - Combines all matches into one PDF
- 🖥️ **User-friendly GUI** - Simple, intuitive interface

## Installation

### 🌐 **Web Version (Easiest - Works Everywhere!)**
Download `AdriansPDFManipulator.html` from the [Releases](../../releases) page, then:
1. Double-click the HTML file
2. It opens in your browser
3. Done! No installation, no security warnings

**✅ Works on Windows, Mac, Linux - Zero installation required**

### 💻 Windows
Download the `.exe` from the [Releases](../../releases) page. No installation needed!

### 🍎 macOS
Download the `.app` from the [Releases](../../releases) page.

**⚠️ Important**: macOS will block unsigned apps. See [MACOS_INSTALL.md](MACOS_INSTALL.md) for detailed installation instructions.

**Quick start**: Right-click the app → "Open" → Click "Open" in the dialog.

**Easier alternative**: Use the web version above (zero hassle!)

Or see [README_MAC_BUILD.md](README_MAC_BUILD.md) to build from source.

## Building from Source

### Prerequisites
- Python 3.8 or later
- pip

### Windows
```bash
pip install -r requirements.txt
pyinstaller AdriansPDFManipulator.spec
```

### macOS
```bash
chmod +x build_macos_app.sh
./build_macos_app.sh
```

See [README_MAC_BUILD.md](README_MAC_BUILD.md) for detailed instructions.

## Usage

1. **Select PDF(s)**: Click "Browse..." to choose one or more PDF files
2. **Enter search terms**: Type comma-separated terms (e.g., "invoice, receipt, 2024")
3. **Configure options**:
   - Match logic: ANY term (OR) or ALL terms (AND)
   - Case sensitivity
   - Page buffer: Include ±N pages around matches
   - Keep first N pages: Always include first pages
4. **Extract**: Click "Extract Matching Pages" and choose output location

## Technologies

- **Python 3** - Core language
- **tkinter** - GUI framework
- **pypdf** - PDF manipulation
- **PyInstaller** - Executable packaging

## Development

See [README_GITHUB_ACTIONS.md](README_GITHUB_ACTIONS.md) for automated multi-platform builds.

## License

Personal project by Adrian.
