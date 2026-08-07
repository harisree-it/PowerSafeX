
import time
import os
import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from threading import Event

from instruments.manager import InstrumentManager

class TestRunner(QThread):
    progress_updated = pyqtSignal(int) # Overall progress 0-100
    log_message = pyqtSignal(str)
    test_finished = pyqtSignal(str, str, list) # name, status, images
    all_tests_finished = pyqtSignal()
    comm_error_signal = pyqtSignal(str, object) # msg, runner_instance
    
    def __init__(self, selected_tests, dut_data, test_params):
        """
        selected_tests: list of strings (names)
        """
        super().__init__()
        self.test_names = selected_tests
        self.dut_data = dut_data
        self.test_params = test_params
        self.is_running = True
        
        # For error handling
        self.error_event = Event()
        self.error_choice = "Cancel"
        
    def run(self):
        # Connect to instruments
        self.log_message.emit("Initializing Instruments...")
        mgr = InstrumentManager()
        mgr.set_logger(self.log_message.emit)
        mgr.set_error_handler(self.handle_instrument_error)
        
        # DEBUG: Check if we should force a communication error for testing
        force_err = self.test_params.get("Debug: Force Comm Error", False)
        if force_err:
            self.log_message.emit("!!! DEBUG MODE: Forcing Communication Errors enabled !!!")
            # Apply to all existing and future driver instances
            for driver in mgr._driver_instances.values():
                if hasattr(driver, 'force_comm_error'):
                    driver.force_comm_error = True
            # Also set it in manager to apply to future instances
            # Actually, manager doesn't have a direct way to set it on new instances yet,
            # but for our current flow, instances are created during connect_all() or first access.
            # We'll modify InstrumentManager.get_driver_instance to handle this.
            mgr.force_comm_error_debug = True # Custom flag for manager
            
        if not mgr.connect_all():
            self.log_message.emit("Error: Could not connect to instruments!")
            return
            
        custom_sequences = self.test_params.get("_custom_sequences", {})
        total_tests = len(self.test_names)
        
        for idx, test_name in enumerate(self.test_names):
            if not self.is_running:
                break
                
            self.log_message.emit(f"--- Starting Test: {test_name} ---")
            images = []
            
            # Check for custom sequence first
            print(f"DEBUG: Checking for custom sequence. Test: '{test_name}'")
            print(f"DEBUG: Available Custom Sequences: {list(custom_sequences.keys())}")
            
            if test_name in custom_sequences:
                self.log_message.emit(f"Running Custom Sequence for {test_name}")
                code = custom_sequences[test_name]["code"]
                print(f"DEBUG: Code to execute:\n{code}")
                
                if not code or not code.strip():
                    self.log_message.emit("Error: Custom sequence is empty!")
                    status = "Fail"
                else:
                    # Execute custom code
                    try:
                        # Get test params for this specific test
                        # self.test_params is the global dict {test_name: params}
                        current_params = self.test_params.get(test_name, {})
                        
                        # Define context for exec()
                        context = {
                            "mgr": mgr,
                            "log_callback": self.log_message.emit,
                            "time": time,
                            "os": os,
                            "test_params": current_params,
                            "dut_data": self.dut_data,
                            "progress_callback": self.progress_updated.emit,
                            "images": images
                        }
                        exec(code, context)
                        status = "Pass" # Default if no exception
                    except Exception as e:
                        self.log_message.emit(f"Custom Sequence Error: {e}")
                        status = "Fail"
            else:
                # Enforce Custom Sequence
                err_msg = f"Error: Test sequence not defined for '{test_name}'"
                self.log_message.emit(err_msg)
                self.log_message.emit("Please create a sequence using the 'Edit Sequence' button.")
                status = "Fail"
            
            # Capture results and exit test loop
            self.test_finished.emit(test_name, status, images)
            time.sleep(0.5) # Gap between tests
            
        self.all_tests_finished.emit()

    def handle_instrument_error(self, msg):
        """Callback from Instrument driver on persistent error."""
        self.error_event.clear()
        self.comm_error_signal.emit(msg, self)
        # Block until GUI responds (sets self.error_choice and self.error_event.set())
        self.error_event.wait()
        return self.error_choice

    def stop(self):
        self.is_running = False

