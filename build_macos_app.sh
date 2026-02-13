#!/bin/bash
# Build macOS .app bundle (better for Mac users)

echo "Building Adrian's PDF Manipulator as macOS .app bundle..."

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

# Build the application as a .app bundle
echo "Building .app bundle..."
pyinstaller AdriansPDFManipulator_macOS.spec

# Check if build was successful
if [ -d "dist/AdriansPDFManipulator.app" ]; then
    echo "✓ Build successful!"

    # Ad-hoc sign the app to allow right-click → Open to work
    echo "Signing app..."
    codesign --force --deep --sign - dist/AdriansPDFManipulator.app
    codesign --verify --verbose dist/AdriansPDFManipulator.app

    echo "✓ App signed!"
    echo "Application location: dist/AdriansPDFManipulator.app"
    echo ""
    echo "Your Mac friends can now drag this .app to their Applications folder!"
else
    echo "✗ Build failed. Check the output above for errors."
    exit 1
fi

deactivate
