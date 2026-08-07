# Test Automation GUI - Quick Build Guide

## PyInstaller is Already Installed! ✅

Good news: PyInstaller is already installed on your system.

## Quick Build Instructions

### Option 1: Use the Simple Build Script (Recommended)

1. **Double-click** `build_simple.bat`
2. **Wait** for the build to complete (2-5 minutes)
3. **Find executable** in `dist\TestAutomationGUI.exe`

### Option 2: Command Line

Open Command Prompt in the project folder and run:

```cmd
pyinstaller --clean --noconfirm --name=TestAutomationGUI --windowed --onefile --add-data="instruments.json;." main.py
```

## What Gets Created

After building:
```
dist/
└── TestAutomationGUI.exe  ← Standalone executable (100-200 MB)
```

## Testing the Executable

```cmd
cd dist
TestAutomationGUI.exe
```

## Distribution

To distribute your software:

1. **Copy from `dist` folder**:
   - `TestAutomationGUI.exe`

2. **Also include**:
   - `instruments.json` (place in same folder as .exe)
   - `assets/` folder (if you have images)

3. **Create distribution package**:
   ```
   TestAutomationGUI_v1.0/
   ├── TestAutomationGUI.exe
   ├── instruments.json
   └── README.txt
   ```

4. **Zip it**: `TestAutomationGUI_v1.0.zip`

## Troubleshooting

### If build fails:

1. **Check Python version**:
   ```cmd
   python --version
   ```
   Should be Python 3.8 or higher

2. **Reinstall PyInstaller**:
   ```cmd
   pip uninstall pyinstaller
   pip install pyinstaller
   ```

3. **Try without --onefile** (creates folder instead):
   ```cmd
   pyinstaller --windowed main.py
   ```

### If executable doesn't run:

1. **Check for missing DLLs**: Run from command prompt to see errors
2. **Disable antivirus** temporarily (may block PyInstaller)
3. **Run as administrator**

## File Size

The executable will be large (100-200 MB) because it includes:
- Python interpreter
- PyQt6 libraries
- All dependencies

This is normal for PyInstaller executables.

## Next Steps

1. Run `build_simple.bat`
2. Test `dist\TestAutomationGUI.exe`
3. If it works, distribute the `dist` folder contents

That's it! Your software is ready to distribute.
