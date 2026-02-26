from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QFormLayout, 
                             QGroupBox, QCheckBox, QGridLayout, QMessageBox,
                             QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QDialogButtonBox,
                             QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import json
from gui.styles import Theme

# ==========================================
# Instrument Setup Dialog
# ==========================================
class InstrumentSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instrument Setup")
        self.resize(800, 400)
        
        layout = QVBoxLayout(self)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Address", "Max V", "Max I", "Max P", "Status", "Test"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Name
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Type
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Address
        layout.addWidget(self.table)
        
        # Initial Population from Manager
        from instruments.manager import InstrumentManager
        self.mgr = InstrumentManager()
        
        self.table.setRowCount(len(self.mgr.instruments))
        for i, inst in enumerate(self.mgr.instruments):
            self._add_row_ui(i, inst)
            
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Instrument")
        add_btn.clicked.connect(self.add_row)
        btn_layout.addWidget(add_btn)
        
        del_btn = QPushButton("Remove Selected")
        del_btn.clicked.connect(self.remove_row)
        btn_layout.addWidget(del_btn)

        test_btn = QPushButton("Test All Connections")
        test_btn.clicked.connect(self.test_all)
        btn_layout.addWidget(test_btn)
        
        layout.addLayout(btn_layout)
        
        # Dialog Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def _add_row_ui(self, row, inst):
        # Name
        self.table.setItem(row, 0, QTableWidgetItem(inst.get("name", "New Instrument")))
        
        # Type
        type_combo = QComboBox()
        type_combo.addItems([
            "AC Source", "DC Source", "AC/DC Source", "Bidirectional DC Supply",
            "DC Load", "AC Load", "Scope", "Multimeter"
        ])
        type_combo.setCurrentText(inst.get("type", "AC Source"))
        self.table.setCellWidget(row, 1, type_combo)
        
        # Address
        self.table.setItem(row, 2, QTableWidgetItem(inst.get("address", "")))
        
        # Limits
        limits = inst.get("limits", {})
        self.table.setItem(row, 3, QTableWidgetItem(str(limits.get("V", 0))))
        self.table.setItem(row, 4, QTableWidgetItem(str(limits.get("I", 0))))
        self.table.setItem(row, 5, QTableWidgetItem(str(limits.get("P", 0))))
        
        # Status
        status_item = QTableWidgetItem("Not Checked")
        self.table.setItem(row, 6, status_item)
        
        # Test Btn
        btn = QPushButton("Connect")
        btn.clicked.connect(lambda checked, r=row: self.test_row(r))
        self.table.setCellWidget(row, 7, btn)
        
    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        default_inst = {
            "name": "New Instrument",
            "type": "AC Source",
            "address": "GPIB0::?::INSTR",
            "limits": {"V": 0, "I": 0, "P": 0}
        }
        self._add_row_ui(row, default_inst)
        
    def remove_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
 
    def test_row(self, row):
        addr_item = self.table.item(row, 2)
        if not addr_item: return
        addr = addr_item.text()
        
        # Status column is 6
        try:
            from instruments.drivers import Instrument
            # Pass the global simulation mode to avoid false positives
            inst = Instrument(addr, simulation_mode=self.mgr.simulation_mode)
            
            if inst.connect():
                 idn = inst.query_idn()
                 self.table.item(row, 6).setText(f"OK: {idn.split(',')[0]}")
                 
                 # Update Name with Model from IDN
                 # Format typically: Manufacturer,Model,Serial,Version
                 parts = idn.split(',')
                 if len(parts) >= 2:
                     model_name = parts[1].strip()
                     # Update the name column
                     self.table.item(row, 0).setText(model_name)
            else:
                 self.table.item(row, 6).setText("Failed")
        except Exception as e:
             self.table.item(row, 6).setText(f"Error: {str(e)}")
 
    def test_all(self):
        for i in range(self.table.rowCount()):
            self.test_row(i)
            
    def save_and_accept(self):
        new_list = []
        for i in range(self.table.rowCount()):
            name = self.table.item(i, 0).text()
            inst_type = self.table.cellWidget(i, 1).currentText()
            addr = self.table.item(i, 2).text()
            
            try:
                v = float(self.table.item(i, 3).text())
                c = float(self.table.item(i, 4).text())
                p = float(self.table.item(i, 5).text())
            except:
                v, c, p = 0, 0, 0
            
            # Decide driver class based on type (Simplification)
            driver = "Instrument"
            if "Source" in inst_type or "Supply" in inst_type: 
                driver = "ChromaPowerSupply"
            elif "Load" in inst_type: 
                driver = "ChromaElectronicLoad"
            elif "Scope" in inst_type: 
                driver = "TektronixScope"
            
            inst = {
                "name": name,
                "type": inst_type,
                "driver": driver,
                "address": addr,
                "limits": {"V": v, "I": c, "P": p}
            }
            new_list.append(inst)
            
        self.mgr.instruments = new_list
        self.mgr.save_config()
        self.accept()

# ==========================================
# 2. Configuration Window
# ==========================================
class ConfigWindow(QWidget):
    def __init__(self, on_next_callback, on_back_callback, on_imported_callback=None):
        super().__init__()
        self.on_next = on_next_callback
        self.on_back = on_back_callback
        self.on_imported = on_imported_callback
        
        main_layout = QVBoxLayout(self)
        header = QLabel("Test Configuration")
        header.setObjectName("HeaderLabel")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap("assets/config_header.png")
        if not pixmap.isNull():
             # Scale if too wide (e.g. max 800px width)
             if pixmap.width() > 800:
                 pixmap = pixmap.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
             image_label.setPixmap(pixmap)
        main_layout.addWidget(image_label)
        
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # DUT Details
        dut_group = QGroupBox("Device Under Test (DUT) Details")
        dut_form = QFormLayout()
        
        self.converter_type = QComboBox()
        self.converter_type.addItems(["AC/DC Converter", "DC/DC Converter", "MPPT DC/DC Converter", "DC/AC Inverter"])
        
        self.project_name = QLineEdit()
        self.part_number = QLineEdit()
        self.build_version = QLineEdit()
        self.fw_checksum = QLineEdit()
        self.tester_name = QLineEdit()
        
        # New electrical fields
        self.power_rating = QLineEdit()
        self.input_nominal_voltage = QLineEdit()
        self.input_min_voltage = QLineEdit()
        self.input_max_voltage = QLineEdit()
        self.output_nominal_voltage = QLineEdit()
        self.output_min_voltage = QLineEdit()
        self.output_max_voltage = QLineEdit()
        
        # Conditional fields (managed by visibility)
        self.input_freq_range = QLineEdit() # For AC/DC
        self.output_freq = QLineEdit()      # For DC/AC
        
        # Labels for dynamic fields to hide/show them properly
        self.lbl_input_freq = QLabel("Input Freq Range (Hz):")
        self.lbl_output_freq = QLabel("Output Frequency (Hz):")
 
        dut_form.addRow("Converter Type:", self.converter_type)
        dut_form.addRow("Project Name:", self.project_name)
        dut_form.addRow("Part Number:", self.part_number)
        dut_form.addRow("Build Version:", self.build_version)
        dut_form.addRow("FW Checksum:", self.fw_checksum)
        dut_form.addRow("Tester Name:", self.tester_name)
        
        dut_group.setLayout(dut_form)
        
        # Electrical Details Layout (New Section)
        elec_group = QGroupBox("Electrical Details")
        elec_layout = QGridLayout()
        elec_layout.setColumnStretch(1, 1) # Stretch input field
        elec_layout.setColumnStretch(4, 1) # Stretch input field
        
        # Row 0
        elec_layout.addWidget(QLabel("Power Rating:"), 0, 0)
        elec_layout.addWidget(self.power_rating, 0, 1)
        elec_layout.addWidget(QLabel("W"), 0, 2)
        
        elec_layout.addWidget(QLabel("Input Nominal:"), 0, 3)
        elec_layout.addWidget(self.input_nominal_voltage, 0, 4)
        elec_layout.addWidget(QLabel("V"), 0, 5)
        
        # Row 1
        elec_layout.addWidget(QLabel("Input Min Voltage:"), 1, 0)
        elec_layout.addWidget(self.input_min_voltage, 1, 1)
        elec_layout.addWidget(QLabel("V"), 1, 2)
        
        elec_layout.addWidget(QLabel("Input Max Voltage:"), 1, 3)
        elec_layout.addWidget(self.input_max_voltage, 1, 4)
        elec_layout.addWidget(QLabel("V"), 1, 5)
        
        # Row 2
        elec_layout.addWidget(QLabel("Output Nominal:"), 2, 0)
        elec_layout.addWidget(self.output_nominal_voltage, 2, 1)
        elec_layout.addWidget(QLabel("V"), 2, 2)
        
        elec_layout.addWidget(QLabel("Output Min Voltage:"), 2, 3)
        elec_layout.addWidget(self.output_min_voltage, 2, 4)
        elec_layout.addWidget(QLabel("V"), 2, 5)
        
        # Row 3
        elec_layout.addWidget(QLabel("Output Max Voltage:"), 3, 0)
        elec_layout.addWidget(self.output_max_voltage, 3, 1)
        elec_layout.addWidget(QLabel("V"), 3, 2)
 
        # Row 4 (Dynamic Freq)
        self.lbl_input_freq.setText("Input Freq Range:")
        self.lbl_input_freq_unit = QLabel("Hz")
        elec_layout.addWidget(self.lbl_input_freq, 4, 0)
        elec_layout.addWidget(self.input_freq_range, 4, 1)
        elec_layout.addWidget(self.lbl_input_freq_unit, 4, 2)
        
        # Output Freq (for DC/AC)
        self.lbl_output_freq.setText("Output Frequency:")
        self.lbl_output_freq_unit = QLabel("Hz")
        elec_layout.addWidget(self.lbl_output_freq, 4, 3)
        elec_layout.addWidget(self.output_freq, 4, 4)
        elec_layout.addWidget(self.lbl_output_freq_unit, 4, 5)
 
        elec_group.setLayout(elec_layout)
        
        # Setup Left Column (DUT + Electrical)
        left_layout = QVBoxLayout()
        left_layout.addWidget(dut_group)
        left_layout.addWidget(elec_group)
        left_layout.addStretch()
        
        content_layout.addLayout(left_layout, stretch=2)
                 
        
        # Instruments
        inst_group = QGroupBox("Instrumentation Setup")
        inst_form = QFormLayout()
        
        self.input_source = QComboBox()
        self.output_load = QComboBox()
        self.refresh_instrument_lists()
        
        inst_form.addRow("Input Source:", self.input_source)
        inst_form.addRow("Output Load:", self.output_load)
        
        from instruments.manager import InstrumentManager
        self.sim_mode_chk = QCheckBox("Simulation Mode (Use Dummy Data)")
        self.sim_mode_chk.setChecked(InstrumentManager().simulation_mode)
        self.sim_mode_chk.stateChanged.connect(self.toggle_sim_mode)
        inst_form.addRow(self.sim_mode_chk)
 
        self.setup_btn = QPushButton("Setup Instruments")
        self.setup_btn.clicked.connect(self.open_setup_dialog)
        inst_form.addRow(self.setup_btn)
        
        inst_group.setLayout(inst_form)
        content_layout.addWidget(inst_group)
 
        
        # Navigation
        nav_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(on_back_callback)
        nav_layout.addWidget(back_btn)
        
        # Backup/Import (Same line as Back)
        backup_btn = QPushButton("Backup Settings")
        backup_btn.clicked.connect(self.on_backup)
        nav_layout.addWidget(backup_btn)
        
        import_btn = QPushButton("Import Settings")
        import_btn.clicked.connect(self.on_import)
        nav_layout.addWidget(import_btn)
        
        nav_layout.addStretch()
        
        next_btn = QPushButton("Next: Select Tests")
        next_btn.setObjectName("PrimaryButton")
        next_btn.clicked.connect(self.validate_and_proceed)
        nav_layout.addWidget(next_btn)
        main_layout.addLayout(nav_layout)
 
        # Connect signal
        self.converter_type.currentIndexChanged.connect(self.update_fields_visibility)
        self.update_fields_visibility() # Set initial state
 
    def toggle_sim_mode(self, state):
        from instruments.manager import InstrumentManager
        mgr = InstrumentManager()
        mgr.simulation_mode = (state == Qt.CheckState.Checked.value)
        mgr.save_config()
 
    def open_setup_dialog(self):
        dlg = InstrumentSetupDialog(self)
        dlg.exec()
        self.refresh_instrument_lists()
 
    def refresh_instrument_lists(self):
        from instruments.manager import InstrumentManager
        mgr = InstrumentManager()
        
        ctype = self.converter_type.currentText()
        
        req_ac_source = "AC/DC" in ctype
        req_dc_source = "DC/DC" in ctype or "DC/AC" in ctype
        
        req_dc_load = "AC/DC" in ctype or "DC/DC" in ctype
        req_ac_load = "DC/AC" in ctype
 
        all_insts = mgr.instruments
        
        valid_sources = []
        for inst in all_insts:
            t = inst.get("type", "")
            is_valid = False
            
            if req_ac_source:
                if t in ["AC Source", "AC/DC Source"]: is_valid = True
            elif req_dc_source:
                if t in ["DC Source", "AC/DC Source", "Bidirectional DC Supply"]: is_valid = True
                
            if is_valid: valid_sources.append(inst)
            
        current_src = self.input_source.currentText()
        self.input_source.clear()
        self.input_source.addItems([s["name"] for s in valid_sources])
        self.input_source.addItems(["Simulated Source"])
        
        idx = self.input_source.findText(current_src)
        if idx >= 0: self.input_source.setCurrentIndex(idx)
 
        # Filter Loads
        valid_loads = []
        for inst in all_insts:
            t = inst.get("type", "")
            is_valid = False
            
            if req_dc_load:
                if t in ["DC Load", "Bidirectional DC Supply"]: is_valid = True
            elif req_ac_load:
                if t in ["AC Load"]: is_valid = True
            
            if is_valid: valid_loads.append(inst)
 
        current_load = self.output_load.currentText()
        self.output_load.clear()
        self.output_load.addItems([l["name"] for l in valid_loads])
        self.output_load.addItems(["Resistive Load Bank", "Simulated Load"])
        
        idx = self.output_load.findText(current_load)
        if idx >= 0: self.output_load.setCurrentIndex(idx)
 
    def update_fields_visibility(self):
        self.refresh_instrument_lists()
        ctype = self.converter_type.currentText()
        
        if "AC/DC" in ctype:
            self.lbl_input_freq.setVisible(True)
            self.input_freq_range.setVisible(True)
            self.lbl_input_freq_unit.setVisible(True)
        else:
            self.lbl_input_freq.setVisible(False)
            self.input_freq_range.setVisible(False)
            self.lbl_input_freq_unit.setVisible(False)
            
        if "DC/AC" in ctype:
            self.lbl_output_freq.setVisible(True)
            self.output_freq.setVisible(True)
            self.lbl_output_freq_unit.setVisible(True)
        else:
            self.lbl_output_freq.setVisible(False)
            self.output_freq.setVisible(False)
            self.lbl_output_freq_unit.setVisible(False)
        
    def validate_and_proceed(self):
        data = self.get_data()
        for k, v in data.items():
            if not v or v.strip() == "":
                QMessageBox.warning(self, "Validation Error", f"Field '{k}' cannot be empty.")
                return
 
        try:
            power = float(data["Power Rating"])
            in_nom = float(data["Input Nominal V"])
            in_min = float(data["Input Min V"])
            in_max = float(data["Input Max V"])
            out_nom = float(data["Output Nominal V"])
            out_min = float(data["Output Min V"])
            out_max = float(data["Output Max V"])
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter valid numeric values for electrical fields.")
            return
 
        from instruments.manager import InstrumentManager
        mgr = InstrumentManager()
        
        source_name = data["Input Source"]
        src_config = mgr.get_instrument_by_name(source_name)
        
        if src_config:
             limits = src_config.get("limits", {})
             src_max_v = limits.get("V", 0)
             src_max_p = limits.get("P", 0)
             src_max_i = limits.get("I", 0)
             
             if in_max > src_max_v:
                  QMessageBox.critical(self, "Source Limitation", f"Selected Source ({source_name}) configured max is {src_max_v}V.\nDUT requires {in_max}V.")
                  return
             
             if power > src_max_p:
                  QMessageBox.critical(self, "Source Limitation", f"Selected Source ({source_name}) configured max is {src_max_p}W.\nDUT requires {power}W.")
                  return
                  
             if in_min > 0:
                  max_required_i = power / in_min
                  if max_required_i > src_max_i:
                       QMessageBox.critical(self, "Source Limitation", f"Selected Source ({source_name}) configured max is {src_max_i}A.\nDUT requires ~{max_required_i:.2f}A (at {in_min}V).")
                       return
        
        load_name = data["Output Load"]
        load_config = mgr.get_instrument_by_name(load_name)
        
        if load_config:
             limits = load_config.get("limits", {})
             load_max_v = limits.get("V", 0)
             load_max_p = limits.get("P", 0)
             load_max_i = limits.get("I", 0)
             
             if out_max > load_max_v:
                   QMessageBox.critical(self, "Load Limitation", f"Selected Load ({load_name}) configured max is {load_max_v}V.\nDUT outputs up to {out_max}V.")
                   return
             
             if power > load_max_p: 
                   QMessageBox.critical(self, "Load Limitation", f"Selected Load ({load_name}) configured max is {load_max_p}W.\nDUT puts out {power}W.")
                   return
                   
             if out_min > 0:
                  max_out_i = power / out_min
                  if max_out_i > load_max_i:
                       QMessageBox.critical(self, "Load Limitation", f"Selected Load ({load_name}) configured max is {load_max_i}A.\nDUT puts out ~{max_out_i:.2f}A.")
                       return
                        
        if src_config:
             try:
                 driver = mgr.get_driver_instance(source_name)
                 if not driver.connect():
                      raise Exception("Failed to connect")
                 idn = driver.query_idn()
                 print(f"Source IDN: {idn}")
             except Exception as e:
                 QMessageBox.critical(self, "Instrument Error", f"Failed to connect to Source: {source_name}\nError: {str(e)}")
                 return
 
        if load_config:
             try:
                 driver = mgr.get_driver_instance(load_name)
                 if not driver.connect():
                      raise Exception("Failed to connect")
                 idn = driver.query_idn()
                 print(f"Load IDN: {idn}")
             except Exception as e:
                 QMessageBox.critical(self, "Instrument Error", f"Failed to connect to Load: {load_name}\nError: {str(e)}")
                 return
 
        self.on_next()
        
    def get_data(self):
        data = {
            "Converter Type": self.converter_type.currentText(),
            "Project Name": self.project_name.text(),
            "Part Number": self.part_number.text(),
            "Build Version": self.build_version.text(),
            "FW Checksum": self.fw_checksum.text(),
            "Tester Name": self.tester_name.text(),
            "Power Rating": self.power_rating.text(),
            "Input Nominal V": self.input_nominal_voltage.text(),
            "Input Min V": self.input_min_voltage.text(),
            "Input Max V": self.input_max_voltage.text(),
            "Output Nominal V": self.output_nominal_voltage.text(),
            "Output Min V": self.output_min_voltage.text(),
            "Output Max V": self.output_max_voltage.text(),
            "Input Source": self.input_source.currentText(),
            "Output Load": self.output_load.currentText()
        }
        
        if self.input_freq_range.isVisible():
            data["Input Freq Range"] = self.input_freq_range.text()
            
        if self.output_freq.isVisible():
            data["Output Frequency"] = self.output_freq.text()
            
        return data

    def set_data(self, data):
        # 1. Update Converter Type first (triggers visibility changes)
        ctype = data.get("Converter Type", "")
        idx = self.converter_type.findText(ctype)
        if idx >= 0:
            self.converter_type.setCurrentIndex(idx)
        
        # 2. Basic Fields
        self.project_name.setText(data.get("Project Name", ""))
        self.part_number.setText(data.get("Part Number", ""))
        self.build_version.setText(data.get("Build Version", ""))
        self.fw_checksum.setText(data.get("FW Checksum", ""))
        self.tester_name.setText(data.get("Tester Name", ""))
        
        # 3. Electrical Fields
        self.power_rating.setText(data.get("Power Rating", ""))
        self.input_nominal_voltage.setText(data.get("Input Nominal V", ""))
        self.input_min_voltage.setText(data.get("Input Min V", ""))
        self.input_max_voltage.setText(data.get("Input Max V", ""))
        self.output_nominal_voltage.setText(data.get("Output Nominal V", ""))
        self.output_min_voltage.setText(data.get("Output Min V", ""))
        self.output_max_voltage.setText(data.get("Output Max V", ""))
        
        # 4. Optional Fields (Frequency)
        if "Input Freq Range" in data:
            self.input_freq_range.setText(data["Input Freq Range"])
        if "Output Frequency" in data:
            self.output_freq.setText(data["Output Frequency"])
            
        # 5. Instruments (refresh lists first since converter type might have changed)
        self.refresh_instrument_lists()
        
        src_idx = self.input_source.findText(data.get("Input Source", ""))
        if src_idx >= 0: self.input_source.setCurrentIndex(src_idx)
        
        load_idx = self.output_load.findText(data.get("Output Load", ""))
        if load_idx >= 0: self.output_load.setCurrentIndex(load_idx)

    def on_backup(self):
        # 1. Gather all data (using default structure for consistency)
        backup_data = {
            "dut_data": self.get_data(),
            "test_params": {}, # Empty on this screen unless we want to track state across navigation
            "selected_tests": []
        }
        
        # 2. Open Save Dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Backup Settings", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(backup_data, f, indent=4)
                QMessageBox.information(self, "Success", f"Settings backed up to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save backup: {str(e)}")

    def on_import(self):
        # 1. Open Open Dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # 2. Validate basic structure
                if "dut_data" not in data:
                    raise Exception("Invalid settings file format.")
                
                # 3. Update UI
                self.set_data(data["dut_data"])
                
                # 4. Notify Parent (to sync to TestSelectionWindow)
                if self.on_imported:
                    # Pass the whole data object so TestSelection can sync its params/selection too
                    self.on_imported(data)
                
                QMessageBox.information(self, "Success", "Settings imported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import settings: {str(e)}")
