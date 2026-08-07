
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QComboBox, QDialogButtonBox, QGroupBox,
                             QDoubleSpinBox, QLabel)
from PyQt6.QtCore import Qt

class InstrumentDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Instrument" if not data else "Edit Instrument")
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Form Layout
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Lab Source 1")
        form_layout.addRow("Name:", self.name_input)
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Bidirectional DC Supply", "DC Supply", "AC Source", "Electronic Load", "Scope", "Other"])
        form_layout.addRow("Type:", self.type_input)
        
        self.driver_input = QComboBox()
        self.driver_input.addItems(["ChromaPowerSupply", "ChromaAcSource", "ChromaElectronicLoad", "TektronixScope", "Instrument"])
        form_layout.addRow("Driver:", self.driver_input)
        
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("e.g. GPIB0::1::INSTR")
        form_layout.addRow("Address:", self.address_input)
        
        layout.addLayout(form_layout)
        
        # Limits Group
        limits = data.get("limits", {}) if data else {}
        
        self.limits_group = QGroupBox("Safety Limits")
        limits_layout = QFormLayout()
        
        self.max_v = QDoubleSpinBox()
        self.max_v.setRange(0, 5000)
        self.max_v.setValue(limits.get("V", 80))
        self.max_v.setSuffix(" V")
        limits_layout.addRow("Max Voltage:", self.max_v)
        
        self.max_i = QDoubleSpinBox()
        self.max_i.setRange(0, 1000)
        self.max_i.setValue(limits.get("I", 60))
        self.max_i.setSuffix(" A")
        limits_layout.addRow("Max Current:", self.max_i)
        
        self.max_p = QDoubleSpinBox()
        self.max_p.setRange(0, 50000)
        self.max_p.setValue(limits.get("P", 1200))
        self.max_p.setSuffix(" W")
        limits_layout.addRow("Max Power:", self.max_p)
        
        self.limits_group.setLayout(limits_layout)
        layout.addWidget(self.limits_group)
        
        # Hide safety limits for measurement-only instruments (Scope)
        self.type_input.currentTextChanged.connect(self._on_type_changed)
        self._on_type_changed(self.type_input.currentText())
        
        # Pre-fill data if available
        if data:
            self.name_input.setText(data.get("name", ""))
            self.type_input.setCurrentText(data.get("type", ""))
            self.driver_input.setCurrentText(data.get("driver", ""))
            self.address_input.setText(data.get("address", ""))
        
        # Buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        
    def _on_type_changed(self, type_text):
        """Hide safety limits for Scope (measurement-only instrument)."""
        is_scope = type_text == "Scope"
        self.limits_group.setVisible(not is_scope)
        # Shrink dialog when limits are hidden
        if is_scope:
            self.resize(400, 280)
        else:
            self.resize(400, 500)

    def get_data(self):
        result = {
            "name": self.name_input.text(),
            "type": self.type_input.currentText(),
            "driver": self.driver_input.currentText(),
            "address": self.address_input.text(),
        }
        # Only include limits for instruments that have outputs
        no_limits_types = {"Scope"}
        if self.type_input.currentText() not in no_limits_types:
            result["limits"] = {
                "V": self.max_v.value(),
                "I": self.max_i.value(),
                "P": self.max_p.value()
            }
        return result
