"""
Setup script for creating executable using PyInstaller
"""
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = [
        'main.py',                          # Entry point
        '--name=TestAutomationGUI',         # Application name
        '--windowed',                       # No console window
        '--onefile',                        # Single executable
        '--icon=assets/icon.ico',           # Application icon (if available)
        '--add-data=assets;assets',         # Include assets folder
        '--add-data=instruments.json;.',    # Include config file
        '--hidden-import=pyvisa',           # Ensure pyvisa is included
        '--hidden-import=PyQt6',            # Ensure PyQt6 is included
        '--hidden-import=matplotlib',       # Ensure matplotlib is included
        '--hidden-import=numpy',            # Ensure numpy is included
        '--hidden-import=docx',             # Ensure python-docx is included
        '--hidden-import=reportlab',        # Ensure reportlab is included
        '--collect-all=pyvisa',             # Collect all pyvisa files
        '--collect-all=PyQt6',              # Collect all PyQt6 files
    ]
    
    run(opts)
