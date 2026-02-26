from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from instruments.manager import InstrumentManager
from gui.windows.instrument_dialogs import InstrumentDialog

class InstrumentSetupWindow(QWidget):
    def __init__(self, on_back_callback):
        super().__init__()
        self.on_back_callback = on_back_callback
        self.manager = InstrumentManager()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Instrument Setup & Connection")
        title.setObjectName("TitleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(120, 35)
        refresh_btn.clicked.connect(self.refresh_instruments)
        header_layout.addWidget(refresh_btn)

        add_btn = QPushButton("➕ Add")
        add_btn.setFixedSize(120, 35)
        add_btn.clicked.connect(self.on_add_instrument)
        header_layout.addWidget(add_btn)

        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setFixedSize(120, 35)
        edit_btn.clicked.connect(self.on_edit_instrument)
        header_layout.addWidget(edit_btn)

        remove_btn = QPushButton("🗑️ Remove")
        remove_btn.setFixedSize(120, 35)
        remove_btn.clicked.connect(self.on_remove_instrument)
        header_layout.addWidget(remove_btn)
        
        layout.addLayout(header_layout)
        
        # Info label
        info_label = QLabel("Configure and test connections to your instruments")
        info_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(info_label)
        
        # Instruments Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Address", "Status", "Action"])
        
        # Table styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back to Welcome")
        back_btn.setFixedSize(180, 40)
        back_btn.clicked.connect(on_back_callback)
        bottom_layout.addWidget(back_btn)
        
        bottom_layout.addStretch()
        
        connect_all_btn = QPushButton("Connect All")
        connect_all_btn.setObjectName("PrimaryButton")
        connect_all_btn.setFixedSize(150, 40)
        connect_all_btn.clicked.connect(self.connect_all_instruments)
        bottom_layout.addWidget(connect_all_btn)
        
        disconnect_all_btn = QPushButton("Disconnect All")
        disconnect_all_btn.setFixedSize(150, 40)
        disconnect_all_btn.clicked.connect(self.disconnect_all_instruments)
        bottom_layout.addWidget(disconnect_all_btn)
        
        layout.addLayout(bottom_layout)
        
        # Load instruments on initialization
        self.refresh_instruments()
    
    def refresh_instruments(self):
        """Reload instruments from config and update table"""
        self.manager.load_config()
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with instruments from the manager"""
        instruments = self.manager.instruments
        self.table.setRowCount(len(instruments))
        
        for row, inst in enumerate(instruments):
            # Name
            name_item = QTableWidgetItem(inst.get("name", "Unknown"))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(inst.get("type", "Unknown"))
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 1, type_item)
            
            # Address
            address_item = QTableWidgetItem(inst.get("address", "N/A"))
            address_item.setFlags(address_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, address_item)
            
            # Status
            status_text = "🔴 Disconnected"
            status_color = QColor(150, 150, 150) # Gray
            btn_text = "Connect"
            
            # Check actual connection state
            # Accessing internal _driver_instances to avoid overhead/unnecessary creation if possible, 
            # though get_driver_instance is safe too.
            inst_name = inst.get("name", "Unknown")
            driver = self.manager._driver_instances.get(inst_name)
            if driver and driver.connected:
                 status_text = "🟢 Connected"
                 status_color = QColor(0, 200, 0) # Green
                 btn_text = "Disconnect"
            
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(status_color)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 3, status_item)
            
            # Action button
            connect_btn = QPushButton(btn_text)
            connect_btn.setFixedSize(100, 30)
            connect_btn.setProperty("instrument_name", inst.get("name"))
            connect_btn.setProperty("row", row)
            connect_btn.clicked.connect(lambda checked, r=row: self.toggle_connection(r))
            self.table.setCellWidget(row, 4, connect_btn)
    
    def toggle_connection(self, row):
        """Toggle connection for a specific instrument"""
        button = self.table.cellWidget(row, 4)
        instrument_name = button.property("instrument_name")
        status_item = self.table.item(row, 3)
        
        current_status = status_item.text()
        
        if "Disconnected" in current_status or "Error" in current_status:
            # Attempt to connect
            self.connect_instrument(row, instrument_name, button, status_item)
        else:
            # Disconnect
            self.disconnect_instrument(row, instrument_name, button, status_item)
    
    def connect_instrument(self, row, instrument_name, button, status_item):
        """Connect to a specific instrument"""
        # Update status to connecting
        status_item.setText("🟡 Connecting...")
        button.setEnabled(False)
        
        # Use QTimer to allow UI to update
        QTimer.singleShot(100, lambda: self._perform_connection(row, instrument_name, button, status_item))
    
    def _perform_connection(self, row, instrument_name, button, status_item):
        """Perform the actual connection"""
        try:
            # Get driver instance from manager (persistent)
            driver = self.manager.get_driver_instance(instrument_name)
            if driver is None:
                raise Exception("Failed to create driver instance")
            
            # Attempt connection if not already connected
            if not driver.connected:
                success = driver.connect()
                
                if not success:
                    raise Exception("Connection failed")
            
            status_item.setText("🟢 Connected")
            status_item.setForeground(QColor(0, 200, 0))
            button.setText("Disconnect")
            
            # Query IDN if available
            try:
                idn = driver.query_idn()
                status_item.setToolTip(f"IDN: {idn}")
                
                # Auto-update name if possible
                try:
                    parts = idn.split(',')
                    if len(parts) >= 2:
                        new_name = parts[1].strip()
                        if "CHROMA" in parts[0].upper():
                            new_name = f"Chroma {new_name}"
                        
                        # Update config if changed
                        if self.manager.instruments[row]["name"] != new_name:
                             # We update the dictionary directly in manager
                             self.manager.instruments[row]["name"] = new_name
                             self.manager.save_config()
                             
                             # Update UI
                             self.table.item(row, 0).setText(new_name)
                except Exception as update_e:
                    print(f"Failed to auto-update name: {update_e}")

            except:
                pass
                
        except Exception as e:
            error_msg = str(e)
            status_item.setText(f"⚠️ Error")
            status_item.setForeground(QColor(200, 0, 0))
            status_item.setToolTip(error_msg)
            button.setText("Retry")
            
            # Formatting user-friendly message
            if "Instrument not found" in error_msg or "Connection Error" in error_msg:
                 detailed_msg = (f"Failed to connect to {instrument_name}.\n\n"
                                 f"Reason: {error_msg}\n\n"
                                 "Suggestions:\n"
                                 "- Check if the instrument is powered ON.\n"
                                 "- Verify the address/resource string matches.\n"
                                 "- Ensure the cable (GPIB/USB/LAN) is securely connected.")
                 msg_title = "Connection Failed"
            else:
                 detailed_msg = f"An unexpected error occurred: {error_msg}"
                 msg_title = "Error"

            # Show error dialog
            QMessageBox.warning(self, msg_title, detailed_msg)
        finally:
            button.setEnabled(True)
    
    def disconnect_instrument(self, row, instrument_name, button, status_item):
        """Disconnect from a specific instrument"""
        try:
            driver = self.manager.get_driver_instance(instrument_name)
            if driver and driver.connected:
                driver.disconnect()
            
            status_item.setText("🔴 Disconnected")
            status_item.setForeground(QColor(150, 150, 150))
            status_item.setToolTip("")
            button.setText("Connect")
            
        except Exception as e:
            QMessageBox.warning(self, "Disconnection Error", 
                              f"Error disconnecting {instrument_name}:\n{str(e)}")
    
    def connect_all_instruments(self):
        """Connect to all instruments"""
        for row in range(self.table.rowCount()):
            button = self.table.cellWidget(row, 4)
            status_item = self.table.item(row, 3)
            
            if "Disconnected" in status_item.text() or "Error" in status_item.text():
                self.toggle_connection(row)
    
    def disconnect_all_instruments(self):
        """Disconnect from all instruments"""
        for row in range(self.table.rowCount()):
            button = self.table.cellWidget(row, 4)
            status_item = self.table.item(row, 3)
            
            if "Connected" in status_item.text():
                self.toggle_connection(row)
    
    def on_add_instrument(self):
        """Open dialog to add a new instrument"""
        dialog = InstrumentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Invalid Input", "Instrument name is required.")
                return
                
            self.manager.add_instrument(data)
            self.refresh_instruments()

    def on_edit_instrument(self):
        """Edit selected instrument"""
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()))
        if len(rows) != 1:
            QMessageBox.information(self, "Selection Required", "Please select exactly one instrument to edit.")
            return
            
        row = rows[0]
        data = self.manager.instruments[row]
        
        dialog = InstrumentDialog(self, data)
        if dialog.exec():
            new_data = dialog.get_data()
            if not new_data["name"]:
                QMessageBox.warning(self, "Invalid Input", "Instrument name is required.")
                return
                
            self.manager.update_instrument(row, new_data)
            self.refresh_instruments()
            
    def on_remove_instrument(self):
        """Remove selected instrument"""
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()))
        if not rows:
            QMessageBox.information(self, "No Selection", "Please select an instrument to remove.")
            return
            
        if QMessageBox.question(self, "Confirm Deletion", 
                              f"Are you sure you want to remove {len(rows)} instrument(s)?",
                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            
            # Remove in reverse order to correct indices
            for row in reversed(rows):
                self.manager.remove_instrument(row)
                
            self.refresh_instruments()
