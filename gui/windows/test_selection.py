from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QComboBox, QLineEdit, QFormLayout, QGridLayout,
                             QGroupBox, QRadioButton, QScrollArea,
                             QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox,
                             QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import json
import os
import datetime
from gui.windows.block_editor import BlockEditorWindow
from engine.config import BACKUPS_DIR, DATA_DIR

TEST_PARAMS_SCHEMA = {
    "Input voltage range verification": [
        {"name": "Nominal Voltage", "type": "float", "unit": "V", "default": 48.0, "default_key": "Input Nominal V"},
        {"name": "Input Min Voltage", "type": "float", "unit": "V", "default": 40.0, "default_key": "Input Min V"},
        {"name": "Input Max Voltage", "type": "float", "unit": "V", "default": 60.0, "default_key": "Input Max V"},
        {"name": "Input UVLO Point", "type": "float", "unit": "V", "default": 38.0},
        {"name": "Input UVLO Recovery", "type": "float", "unit": "V", "default": 39.0},
        {"name": "Input OVP Point", "type": "float", "unit": "V", "default": 62.0},
        {"name": "Input OVP Recovery", "type": "float", "unit": "V", "default": 61.0},
        {"name": "Startup Time", "type": "float", "unit": "ms", "default": 100.0},
        {"name": "Load Mode", "type": "combo", "options": ["CC", "CV", "CP", "CR"], "default": "CC"},
        {"name": "Load Value", "type": "float", "unit": "A/V/W/Ohm", "default": 10.0, "default_key": "Power Rating"}
    ],
    "Output voltage accuracy": [
        {"name": "Nominal Voltage", "type": "float", "unit": "V", "default": 48.0, "default_key": "Input Nominal V"},
        {"name": "Input Min Voltage", "type": "float", "unit": "V", "default": 40.0, "default_key": "Input Min V"},
        {"name": "Input Max Voltage", "type": "float", "unit": "V", "default": 60.0, "default_key": "Input Max V"},
        {"name": "Input UVLO Point", "type": "float", "unit": "V", "default": 38.0},
        {"name": "Input UVLO Recovery", "type": "float", "unit": "V", "default": 39.0},
        {"name": "Input OVP Point", "type": "float", "unit": "V", "default": 62.0},
        {"name": "Input OVP Recovery", "type": "float", "unit": "V", "default": 61.0},
        {"name": "Startup Time", "type": "float", "unit": "ms", "default": 100.0},
        {"name": "Load Mode", "type": "combo", "options": ["CC", "CV", "CP", "CR"], "default": "CC"},
        {"name": "Load Value", "type": "float", "unit": "A/V/W/Ohm", "default": 10.0, "default_key": "Power Rating"}
    ]
}

class TestParameterDialog(QDialog):
    def __init__(self, test_name, existing_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Config: {test_name}")
        self.resize(400, 500)
        self.test_name = test_name
        self.fields = {}
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel(f"Parameters for\n{test_name}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        form_layout = QFormLayout()
        
        schema = TEST_PARAMS_SCHEMA.get(test_name, [])
        if not schema:
            layout.addWidget(QLabel("No specific parameters for this test."))
        
        for field in schema:
            fname = field["name"]
            ftype = field["type"]
            funit = field.get("unit", "")
            fdefault = field.get("default", "")
            
            # Use existing data if available, else default
            val = existing_data.get(fname, fdefault) if existing_data else fdefault
            
            if ftype == "float":
                widget = QLineEdit(str(val))
                self.fields[fname] = widget
                label = f"{fname} ({funit}):" if funit else f"{fname}:"
                form_layout.addRow(label, widget)
                
            elif ftype == "combo":
                widget = QComboBox()
                widget.addItems(field["options"])
                widget.setCurrentText(str(val))
                self.fields[fname] = widget
                form_layout.addRow(f"{fname}:", widget)
                
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_data(self):
        data = {}
        for fname, widget in self.fields.items():
            if isinstance(widget, QComboBox):
                data[fname] = widget.currentText()
            else:
                data[fname] = widget.text() 
        return data

class TestSelectionWindow(QWidget):
    # Persistent file for saving block flows (custom sequences)
    SEQUENCES_FILE = os.path.join(DATA_DIR, "custom_sequences.json")

    def __init__(self, on_next_callback, on_back_callback, on_imported_callback=None):
        super().__init__()
        self.on_next = on_next_callback 
        self.on_back = on_back_callback
        self.on_imported = on_imported_callback
        self.dut_data = {}
        
        layout = QVBoxLayout(self)
        
        header = QLabel("Select Test Items")
        header.setObjectName("HeaderLabel")
        layout.addWidget(header)
        
        content = QHBoxLayout()
        layout.addLayout(content)
        
        # Test Table
        self.test_table = QTableWidget()
        self.test_table.setColumnCount(3)
        self.test_table.setHorizontalHeaderLabels(["", "S.No", "Test Item"])
        self.test_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.test_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.test_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.test_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.test_table.verticalHeader().setVisible(False)
        self.test_table.setShowGrid(False) 
        
        self.test_table.setStyleSheet("""
            QTableWidget::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #555;
                border-radius: 4px;
                background-color: transparent;
            }
            QTableWidget::indicator:checked {
                border: 2px solid #00FF00;
                image: url(assets/checkbox_checked.svg);
            }
            QTableWidget::indicator:unchecked:hover {
                border: 2px solid #FFF;
            }
        """)
        
        tests = [
            "1. Input voltage range verification", "2. Output voltage accuracy", "3. Load regulation",
            "4. Line regulation", "5. Power-ON startup", "6. Power-OFF / shutdown behavior",
            "7. Enable / Disable function", "8. Soft-start operation", "9. Input under-voltage lockout (UVLO)",
            "10. Input over-voltage protection", "11. Output over-current protection", "12. Output short-circuit protection",
            "13. Output over-voltage protection", "14. Thermal protection", "15. Rated output power capability",
            "16. Efficiency measurement", "17. No-load / standby power", "18. Output voltage ripple & noise",
            "19. Load transient response", "20. Line transient response", "21. Isolation withstand (Hi-Pot) test",
            "22. Insulation resistance test", "23. High-temperature functional test", "24. Low-temperature functional test"
        ]
        
        self.test_table.setRowCount(len(tests))
        for i, t in enumerate(tests):
            if ". " in t:
                sno, name = t.split(". ", 1)
            else:
                sno, name = str(i+1), t
            
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            chk_item.setCheckState(Qt.CheckState.Unchecked)
            self.test_table.setItem(i, 0, chk_item)
            self.test_table.setItem(i, 1, QTableWidgetItem(sno))
            self.test_table.setItem(i, 2, QTableWidgetItem(name))
            
        self.test_params = {}
        self.custom_sequences = self._load_sequences()  # Auto-load persisted block flows
        self.test_table.currentItemChanged.connect(self.update_details_panel)
        
        content.addWidget(self.test_table, stretch=1)
        
        # Details Panel (Sidebar)
        self.details_group = QGroupBox("Test Configuration")
        self.details_layout = QVBoxLayout()
        self.details_group.setLayout(self.details_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.details_group)
        content.addWidget(scroll, stretch=1)
        
        # Reports
        report_group = QGroupBox("Report Options")
        report_layout = QHBoxLayout()
        # Mutually exclusive report format (previously QCheckBox, which let both
        # or neither be checked even though only one format can actually be produced).
        self.pdf_radio = QRadioButton("PDF Report (Default)")
        self.pdf_radio.setChecked(True)
        self.word_radio = QRadioButton("Word Report")
        report_layout.addWidget(self.pdf_radio)
        report_layout.addWidget(self.word_radio)
        
        self.word_pass = QLineEdit()
        self.word_pass.setPlaceholderText("Password for Word")
        self.word_pass.setEchoMode(QLineEdit.EchoMode.Password)
        report_layout.addWidget(self.word_pass)
        
        report_group.setLayout(report_layout)
        layout.addWidget(report_group)
        
        # Navigation & Settings Buttons
        nav_layout = QHBoxLayout()
        
        # Back Button
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(on_back_callback)
        nav_layout.addWidget(back_btn)
        
        # Backup/Import (Same Line as Back)
        backup_btn = QPushButton("Backup Settings")
        backup_btn.clicked.connect(self.on_backup)
        nav_layout.addWidget(backup_btn)
        
        import_btn = QPushButton("Import Settings")
        import_btn.clicked.connect(self.on_import)
        nav_layout.addWidget(import_btn)
        
        nav_layout.addStretch()
        
        # Start Button (Right Aligned)
        start_btn = QPushButton("Start Test Sequence")
        start_btn.setObjectName("PrimaryButton")
        start_btn.clicked.connect(self.on_start_tests)
        nav_layout.addWidget(start_btn)
        layout.addLayout(nav_layout)
        self.update_details_panel(self.test_table.currentItem())
        
        self.editor_window = None

    def set_dut_data(self, data):
        self.dut_data = data
        self.update_details_panel(self.test_table.currentItem())

    def set_session_data(self, session_data):
        self.dut_data = session_data.get("dut_data", {})
        self.test_params = session_data.get("test_params", {})
        self.custom_sequences = session_data.get("custom_sequences", {})
        self._save_sequences()  # Persist imported sequences to disk
        selected = session_data.get("selected_tests", [])
        self.refresh_table_checks(selected)
        self.update_details_panel(self.test_table.currentItem())
    
    def update_details_panel(self, current, previous=None):
        if not current:
            return
            
        row = current.row()
        name_item = self.test_table.item(row, 2)
        if not name_item:
            return
            
        test_name = name_item.text()
        self.current_test_name = test_name
        
        while self.details_layout.count():
            child = self.details_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # Remove nested layouts
                while child.layout().count():
                    subchild = child.layout().takeAt(0)
                    if subchild.widget():
                        subchild.widget().deleteLater()
                
        # Title
        title_label = QLabel(f"<b>{test_name}</b>")
        self.details_layout.addWidget(title_label)
        
        # Edit Sequence Button
        edit_seq_btn = QPushButton("Edit Sequence (Block Editor)")
        edit_seq_btn.clicked.connect(lambda: self.open_block_editor(test_name))
        self.details_layout.addWidget(edit_seq_btn)
        
        # Show status if custom sequence exists
        if test_name in self.custom_sequences:
            self.details_layout.addWidget(QLabel("<i>Custom sequence active</i>"))
        
        # Diagram if applicable
        if "Input voltage range verification" in test_name:
             diagram_label = QLabel()
             pixmap = QPixmap("assets/input_voltage_diagram.png")
             if not pixmap.isNull():
                  scaled = pixmap.scaledToWidth(350, Qt.TransformationMode.SmoothTransformation)
                  diagram_label.setPixmap(scaled)
                  diagram_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                  self.details_layout.addWidget(diagram_label)
        
        schema = TEST_PARAMS_SCHEMA.get(test_name, [])
        if not schema:
            self.details_layout.addWidget(QLabel("No specific parameters from schema."))
            return
            
        if test_name not in self.test_params:
            self.test_params[test_name] = {}
            
        current_data = self.test_params[test_name]
        
        # Create 2-column grid layout for parameters
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(15)
        grid_layout.setVerticalSpacing(10)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align to top
        
        row = 0
        col = 0
        
        for field in schema:
            fname = field["name"]
            ftype = field["type"]
            funit = field.get("unit", "")
            fdefault = field.get("default", "")
            default_key = field.get("default_key")
            
            val = current_data.get(fname)
            
            if val is None:
                if default_key and default_key in self.dut_data:
                    val = self.dut_data[default_key]
                    if val == "": val = fdefault
                else:
                    val = fdefault
                current_data[fname] = val
                
            if ftype == "float":
                label_text = f"{fname} ({funit}):" if funit else f"{fname}:"
                label = QLabel(label_text)
                widget = QLineEdit(str(val))
                widget.textChanged.connect(lambda text, k=fname: self.update_param(k, text))
                
                grid_layout.addWidget(label, row, col * 2)
                grid_layout.addWidget(widget, row, col * 2 + 1)
                
            elif ftype == "combo":
                label = QLabel(f"{fname}:")
                widget = QComboBox()
                widget.addItems(field["options"])
                widget.setCurrentText(str(val))
                widget.currentTextChanged.connect(lambda text, k=fname: self.update_param(k, text))
                
                grid_layout.addWidget(label, row, col * 2)
                grid_layout.addWidget(widget, row, col * 2 + 1)
            
            # Move to next column, or next row if we've filled both columns
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        self.details_layout.addLayout(grid_layout)
        self.details_layout.addStretch()  # Push content to top
                
    def update_param(self, key, value):
        if hasattr(self, 'current_test_name'):
             self.test_params[self.current_test_name][key] = value

    def open_block_editor(self, test_name):
        existing_xml = None
        if test_name in self.custom_sequences:
            existing_xml = self.custom_sequences[test_name].get("xml")
            print(f"Opening editor for {test_name}. Found XML: {str(existing_xml)[:50]}...")
            
        # Get current params for this test
        current_params = self.test_params.get(test_name, {})
        
        self.editor_window = BlockEditorWindow(
            test_name, current_params, existing_xml,
            self.save_custom_sequence,
            dut_data=getattr(self, 'dut_data', {})
        )
        self.editor_window.show()
        
    def save_custom_sequence(self, test_name, python_code, xml_content):
        self.custom_sequences[test_name] = {
            "code": python_code,
            "xml": xml_content
        }
        self._save_sequences()  # Auto-persist to disk
        # Refresh details to show "Custom sequence active"
        if self.current_test_name == test_name:
             self.update_details_panel(self.test_table.currentItem())

    def _load_sequences(self):
        """Load custom sequences from persistent JSON file."""
        try:
            if os.path.exists(self.SEQUENCES_FILE):
                with open(self.SEQUENCES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"Loaded {len(data)} custom sequence(s) from {self.SEQUENCES_FILE}")
                return data
        except Exception as e:
            print(f"Warning: Could not load custom sequences: {e}")
        return {}

    def _save_sequences(self):
        """Save custom sequences to persistent JSON file."""
        try:
            os.makedirs(os.path.dirname(self.SEQUENCES_FILE), exist_ok=True)
            with open(self.SEQUENCES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.custom_sequences, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.custom_sequences)} custom sequence(s) to {self.SEQUENCES_FILE}")
        except Exception as e:
            print(f"Warning: Could not save custom sequences: {e}")

    def on_backup(self):
        # 1. Gather all data
        backup_data = {
            "dut_data": self.dut_data,
            "test_params": self.test_params,
            "selected_tests": self.get_selected_tests_list(),
            "custom_sequences": self.custom_sequences
        }
        
        # 2. Open Save Dialog (defaults to data/backups/)
        os.makedirs(BACKUPS_DIR, exist_ok=True)
        default_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Backup Settings", os.path.join(BACKUPS_DIR, default_name), "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(backup_data, f, indent=4)
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Success", f"Settings backed up to {file_path}")
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Error", f"Failed to save backup: {str(e)}")

    def on_import(self):
        # 1. Open Open Dialog (defaults to data/backups/)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", BACKUPS_DIR, "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # 2. Validate basic structure
                if "dut_data" not in data or "test_params" not in data:
                    raise Exception("Invalid settings file format.")
                
                # 3. Update Internal State
                self.dut_data = data["dut_data"]
                self.test_params = data["test_params"]
                self.custom_sequences = data.get("custom_sequences", {})
                self._save_sequences()  # Persist imported sequences to disk
                selected = data.get("selected_tests", [])
                
                # 4. Refresh UI
                self.refresh_table_checks(selected)
                self.update_details_panel(self.test_table.currentItem())
                
                # 5. Notify Parent (to sync back to ConfigWindow)
                if self.on_imported:
                    self.on_imported(self.dut_data)
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Success", "Settings imported successfully.")
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Error", f"Failed to import settings: {str(e)}")

    def get_selected_tests_list(self):
        selected = []
        for i in range(self.test_table.rowCount()):
            chk_item = self.test_table.item(i, 0)
            if chk_item.checkState() == Qt.CheckState.Checked:
                name_item = self.test_table.item(i, 2)
                if name_item:
                    selected.append(name_item.text())
        return selected

    def refresh_table_checks(self, selected_list):
        for i in range(self.test_table.rowCount()):
            name_item = self.test_table.item(i, 2)
            chk_item = self.test_table.item(i, 0)
            if name_item and chk_item:
                if name_item.text() in selected_list:
                    chk_item.setCheckState(Qt.CheckState.Checked)
                else:
                    chk_item.setCheckState(Qt.CheckState.Unchecked)

    def on_start_tests(self):
        from engine.config import REPORT_PASSWORD
        if self.word_radio.isChecked() and self.word_pass.text() != REPORT_PASSWORD:
             from PyQt6.QtWidgets import QMessageBox
             QMessageBox.warning(self, "Password Error", "Incorrect password for Word report!")
             return
             
        selected_tests = []
        for i in range(self.test_table.rowCount()):
            chk_item = self.test_table.item(i, 0)
            if chk_item.checkState() == Qt.CheckState.Checked:
                name_item = self.test_table.item(i, 2)
                if name_item:
                    selected_tests.append(name_item.text())
                
        if not selected_tests:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "No Selection", "Please select at least one test.")
            return
            
        # VALIDATION: Check if every selected test has a custom sequence defined
        missing_sequences = []
        for test_name in selected_tests:
            if test_name not in self.custom_sequences or not self.custom_sequences[test_name].get("code", "").strip():
                missing_sequences.append(test_name)
        
        if missing_sequences:
            from PyQt6.QtWidgets import QMessageBox
            msg = "The following tests are missing a sequence:\n\n"
            msg += "\n".join([f"• {t}" for t in missing_sequences])
            msg += "\n\nPlease click 'Edit Sequence' for each test before starting."
            QMessageBox.critical(self, "Missing Sequences", msg)
            return

        # Add Custom Sequences to params so Runner receives them
        # We'll just pass them as a separate argument to on_next, OR embed them in test_params
        # Embedding in test_params under a special key is easier without changing signature of on_next
        self.test_params["_custom_sequences"] = self.custom_sequences

        report_fmt = "Word" if self.word_radio.isChecked() else "PDF"
        self.on_next(selected_tests, self.test_params, report_fmt)
