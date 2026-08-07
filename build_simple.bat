@echo off
REM Build script using Python module syntax
echo ========================================
echo Building Test Automation GUI...
echo ========================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building executable (this may take a few minutes)...
echo.

REM Use python -m PyInstaller instead of pyinstaller command
python -m PyInstaller --clean --noconfirm ^
    --name=TestAutomationGUI ^
    --windowed ^
    --onefile ^
    --add-data="instruments.json;." ^
    --add-data="reports/template;reports/template" ^
    --hidden-import=pyvisa ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=matplotlib.backends.backend_qt5agg ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    echo.
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
echo To test the executable:
echo   cd dist
echo   TestAutomationGUI.exe
echo.
pause
