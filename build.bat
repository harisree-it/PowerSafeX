@echo off
REM Build script for Test Automation GUI
REM This script creates a standalone executable using PyInstaller

echo ========================================
echo Test Automation GUI - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Step 1: Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "TestAutomationGUI.spec" del "TestAutomationGUI.spec"

echo.
echo Step 2: Building executable...
pyinstaller --clean ^
    --name=TestAutomationGUI ^
    --windowed ^
    --onefile ^
    --add-data="assets;assets" ^
    --add-data="instruments.json;." ^
    --hidden-import=pyvisa ^
    --hidden-import=PyQt6 ^
    --hidden-import=matplotlib ^
    --hidden-import=numpy ^
    --hidden-import=docx ^
    --hidden-import=reportlab ^
    --collect-all=pyvisa ^
    --collect-all=PyQt6 ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\TestAutomationGUI.exe
echo.
echo You can now distribute the executable from the 'dist' folder.
echo.
pause
