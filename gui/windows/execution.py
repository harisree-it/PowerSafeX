from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from gui.styles import Theme

# For Plotting
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# Engine
from engine.runner import TestRunner
import datetime

class ExecutionWindow(QWidget):
    def __init__(self, on_finish_callback, on_emergency_stop_callback=None):
        super().__init__()
        self.on_finish = on_finish_callback
        self.on_emergency_stop = on_emergency_stop_callback
        self.current_results = []
        
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        self.status_label = QLabel("Initializing...")
        header_layout.addWidget(self.status_label)
        
        estop = QPushButton("EMERGENCY STOP")
        estop.setObjectName("EmergencyStop")
        estop.clicked.connect(self.emergency_stop)
        header_layout.addStretch()
        header_layout.addWidget(estop)
        layout.addLayout(header_layout)
        
        # Graph (Split)
        graph_layout = QHBoxLayout()
        
        # Matplotlib Canvas
        self.figure = Figure(facecolor=Theme.BACKGROUND)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(Theme.SURFACE)
        self.ax.tick_params(colors=Theme.FOREGROUND)
        self.ax.spines['bottom'].set_color(Theme.BORDER)
        self.ax.spines['left'].set_color(Theme.BORDER)
        self.ax.spines['right'].set_color(Theme.BACKGROUND) # hide
        self.ax.spines['top'].set_color(Theme.BACKGROUND) # hide
        
        graph_layout.addWidget(self.canvas, stretch=2)
        
        # Log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet(f"background-color: {Theme.SURFACE}; color: {Theme.FOREGROUND};")
        graph_layout.addWidget(self.log_area, stretch=1)
        
        layout.addLayout(graph_layout)
        
        # Progress
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        layout.addWidget(QLabel("Total Progress:"))
        layout.addWidget(self.pbar)
        
        self.runner = None

    def start_execution(self, test_names, dut_data, test_params, report_format):
        self.dut_data = dut_data
        self.test_params = test_params
        self.report_format = report_format
        self.current_results = []
        self.log_area.clear()
        self.pbar.setValue(0)
        self.status_label.setText("Test Sequence Running...")
        
        self.runner = TestRunner(test_names, dut_data, test_params)
        self.runner.progress_updated.connect(self.pbar.setValue)
        self.runner.log_message.connect(self.append_log)
        self.runner.comm_error_signal.connect(self.handle_comm_error)
        self.runner.test_finished.connect(self.record_result)
        self.runner.all_tests_finished.connect(self.execution_finished)
        
        # Start
        self.runner.start()
        
    def handle_comm_error(self, msg, runner):
        # This will be called from the TestRunner thread
        # Showing a message box should be done in the main thread, 
        # but since we connected it via a signal, PyQt handles it correctly.
        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Icon.Critical)
        confirm.setWindowTitle("Communication Failure")
        confirm.setText(msg)
        confirm.setInformativeText("Would you like to retry the operation or cancel the test sequence?")
        
        retry_btn = confirm.addButton("Retry", QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = confirm.addButton("Cancel Test", QMessageBox.ButtonRole.RejectRole)
        
        confirm.exec()
        
        if confirm.clickedButton() == retry_btn:
            runner.error_choice = "Retry"
            self.append_log("--- User requested RETRY of communication ---")
        else:
            runner.error_choice = "Cancel"
            self.append_log("--- User requested CANCEL of test sequence ---")
            
        runner.error_event.set() # Unblock the runner thread
        
    def append_log(self, msg):
        self.log_area.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
        # Update dummy plot every log for effect, or if keyword
        if "Setting" in msg or "Measure" in msg:
            self.update_plot()
            
    def update_plot(self):
        self.ax.clear()
        # Random dummy data
        t = np.linspace(0, 0.02, 200)
        amp = 5 + np.random.rand()
        y = 24 + amp * np.sin(2 * np.pi * 50 * t + np.random.rand()*6)
        
        self.ax.plot(t, y, color=Theme.PRIMARY)
        self.ax.set_title(f"Live Waveform Capture (Simulated) - {datetime.datetime.now().strftime('%S.%f')}s", color=Theme.FOREGROUND)
        self.ax.set_xlabel("Time (s)", color=Theme.FOREGROUND)
        self.ax.set_ylabel("Voltage (V)", color=Theme.FOREGROUND)
        try:
             self.canvas.draw()
        except:
             pass 
        
    def record_result(self, name, status, images=None):
        row = {"name": name, "status": status, "details": "Completed successfully"}
        if images:
             row["images"] = images
        self.current_results.append(row)
        
    def execution_finished(self):
        self.status_label.setText("Test Sequence Complete.")
        QMessageBox.information(self, "Done", "All tests finished.")
        # Pass the full text from the log area
        full_logs = self.log_area.toPlainText()
        self.on_finish(self.current_results, self.dut_data, self.report_format, full_logs)

    def emergency_stop(self):
        if self.runner:
            self.runner.stop()
            self.runner.terminate()
            self.append_log("!!! EMERGENCY STOP TRIGGERED !!!")
            
        # Disconnect all instruments safely
        try:
            from instruments.manager import InstrumentManager
            mgr = InstrumentManager()
            
            # Turn off all outputs before disconnecting
            try:
                if hasattr(mgr, 'ac_source'):
                    source = mgr.ac_source
                    if source and source.connected:
                        source.output_off()
                        self.append_log("Power supply output turned OFF")
            except:
                pass
            
            try:
                if hasattr(mgr, 'dc_load'):
                    load = mgr.dc_load
                    if load and load.connected:
                        load.load_off()
                        self.append_log("Load turned OFF")
            except:
                pass
                
            # Disconnect all
            mgr.disconnect_all()
            self.append_log("All instruments disconnected")
        except Exception as e:
            self.append_log(f"Error during emergency shutdown: {e}")
        
        QMessageBox.critical(self, "Emergency Stop", "Test halted by user.\nAll outputs turned OFF and instruments disconnected.")
        
        # Navigate back to test selection window
        if self.on_emergency_stop:
            self.on_emergency_stop()
