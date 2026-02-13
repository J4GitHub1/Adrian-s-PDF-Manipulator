# Automated Multi-Platform Builds with GitHub Actions

## What This Does
Automatically builds your PDF Manipulator for **both Windows and macOS** whenever you push a version tag, using GitHub's free CI/CD service.

## Setup (One-Time)

1. **Push your project to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ApdfM.git
   git push -u origin main
   ```

2. **That's it!** GitHub Actions is enabled by default.

## Usage

### Automatic Builds on Version Tags
```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
- Build Windows .exe
- Build macOS .app
- Create a GitHub Release with both files attached

### Manual Builds
1. Go to your GitHub repo
2. Click "Actions" tab
3. Click "Build Executables" workflow
4. Click "Run workflow" button

## Downloading the Built Files

After a build completes:

**Option 1 - From Releases** (if you used a version tag):
- Go to your repo's "Releases" page
- Download the Windows or macOS version

**Option 2 - From Actions Artifacts**:
1. Go to "Actions" tab
2. Click on the completed workflow run
3. Scroll to "Artifacts" section
4. Download `AdriansPDFManipulator-Windows` or `AdriansPDFManipulator-macOS`

## Benefits
- ✅ No need to own a Mac
- ✅ Consistent build environment
- ✅ Automatic builds on new releases
- ✅ Free for public repositories
- ✅ Build history and logs

## Customization

Edit `.github/workflows/build.yml` to:
- Change trigger conditions
- Add Linux builds
- Run tests before building
- Add code signing (requires certificates)
