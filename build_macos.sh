#!/bin/bash
# Build script for macOS

echo "Building Adrian's PDF Manipulator for macOS..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Build the application
echo "Building executable..."
pyinstaller AdriansPDFManipulator.spec

# Check if build was successful
if [ -f "dist/AdriansPDFManipulator" ]; then
    echo "✓ Build successful!"
    echo "Executable location: dist/AdriansPDFManipulator"
    echo ""
    echo "To create a .app bundle, run: pyinstaller --onefile --windowed AdriansPDFManipulator.py"
else
    echo "✗ Build failed. Check the output above for errors."
    exit 1
fi

deactivate
