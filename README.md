# PowerSafe - Converter Test Automation (GUI)

<div align="center">
  <img src="assets/logo.png" alt="PowerSafe Logo" width="300"/>
</div>

## 📖 Overview

**PowerSafe - Converter Test Automation** is a comprehensive, desktop-based graphical user interface (GUI) application designed for the automated testing of power converters. Built using Python and PyQt6, the software provides a seamless and intuitive workflow for engineers to configure Devices Under Test (DUTs), setup hardware instruments, execute automated test sequences, monitor live progress, and generate detailed standardized test reports.

The application communicates with professional test equipment (such as Chroma DC Power Supplies and Electronic Loads) using PyVISA to automate complex test procedures like Input Voltage Range Verification and Output Voltage Accuracy checks.

---

## ✨ Key Features

- **Intuitive User Interface**: Modern, wizard-like navigation built with PyQt6, guiding the user from setup to execution and result viewing.
- **DUT Configuration**: Easily input and save parameters for the Device Under Test, such as part numbers, expected input/output voltage ranges, and current specifications.
- **Instrument Management**: Built-in setup and connection testing for hardware instruments:
  - Chroma 62000D Series Bidirectional DC Power Supply
  - Chroma DC Electronic Load
- **Automated Test Sequences**: 
  - Input Voltage Range Verification
  - Output Voltage Accuracy
  - *Extensible framework for adding custom test scripts.*
- **Live Test Execution**: Real-time progress tracking, live instrument logging, and an emergency stop mechanism during test execution.
- **Blockly Integration**: Visual block-based editor to optionally build or customize test sequences visually without writing raw code.
- **Automated Report Generation**: Generates comprehensive test reports automatically in both `.docx` (using a standard template) and `.pdf` formats, complete with test results, captured screenshots, and pass/fail metrics.

---

## 🏗️ Architecture & Modules

The project is structured into modular components for scalability and maintainability:

- `engine/`: Contains the core execution engine (`runner.py`) and application configuration constants (`config.py`).
- `gui/`: Contains standard stylesheet definitions (`styles.py`) and all PyQt6 window classes (`windows/`):
  - `welcome.py`, `config.py`, `test_selection.py`, `execution.py`, `results.py`, `instrument_setup.py`, `block_editor.py`.
- `instruments/`: Manages hardware communication (`manager.py`, `drivers.py`) using PyVISA, with specific instrument command implementations in subdirectories (e.g., `chroma/`).
- `reports/`: Handles the parsing of test results and generating Word/PDF documents based on the template in this directory.
- `tests/`: Contains the concrete test sequence logic. All tests inherit from the `BaseTest` class.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harisree-it/PowerSafeX.git
   cd PowerSafeX
   ```

2. Create and activate a virtual environment (Recommended):
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This includes `PyQt6`, `pyvisa`, `python-docx`, `comtypes`, etc.)*

### Running the Application

To launch the application from the source code, run:
```bash
python main.py
```

---

## 🛠️ Building the Standalone Executable

You can compile the application into a standalone Windows executable (.exe) using PyInstaller so it can run without requiring a Python installation.

**Option 1: Using the Batch Script (Recommended)**
Simply double-click `build_simple.bat`. The executable will be generated in the `dist/` directory as `TestAutomationGUI.exe`.

**Option 2: Command Line**
```bash
pyinstaller --clean --noconfirm --name=TestAutomationGUI --windowed --onefile --add-data="instruments.json;." main.py
```

For more detailed build instructions, please refer to the [`BUILD_GUIDE.md`](BUILD_GUIDE.md).

---

## 📡 Hardware Setup

1. Ensure your Chroma Instruments are properly connected to your PC via USB, GPIB, or LAN.
2. Install the necessary VISA drivers (e.g., NI-VISA or Keysight VISA) on your machine.
3. Open the "Instrument Setup" window in the application to discover connected devices and verify connections using the `*IDN?` queries.

---

## 📝 Adding New Tests

1. Create a new Python file in the `tests/` directory (e.g., `test_03_efficiency.py`).
2. Define a class that inherits from `BaseTest`.
3. Implement the `run(self, progress_callback, log_callback)` method.
4. Add the new test configuration inside `engine/config.py` or the test selection registry to make it available in the GUI.

---

## 📄 License

This project is proprietary. All rights reserved.
