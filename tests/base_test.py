"""
Base Test Class for all test sequences
"""
from instruments.manager import InstrumentManager
import time

class BaseTest:
    """Base class for all test sequences"""
    
    def __init__(self, test_name, dut_data, test_params):
        """
        Initialize test
        
        Args:
            test_name: Name of the test
            dut_data: DUT configuration data from ConfigWindow
            test_params: Test-specific parameters from TestSelectionWindow
        """
        self.test_name = test_name
        self.dut_data = dut_data
        self.test_params = test_params
        self.mgr = InstrumentManager()
    
    def run(self, progress_callback, log_callback):
        """
        Execute the test sequence
        
        Args:
            progress_callback: Function to update progress (0-100)
            log_callback: Function to log messages
            
        Returns:
            str: "Pass" or "Fail"
        """
        raise NotImplementedError("Subclass must implement run() method")
    
    def setup(self, log_callback):
        """
        Pre-test setup (optional override)
        
        Args:
            log_callback: Function to log messages
        """
        pass
    
    def teardown(self, log_callback):
        """
        Post-test cleanup (optional override)
        
        Args:
            log_callback: Function to log messages
        """
        pass
    
    def get_param(self, param_name, default=None):
        """
        Get test parameter with fallback to DUT data
        
        Args:
            param_name: Parameter name
            default: Default value if not found
            
        Returns:
            Parameter value
        """
        # Try test params first
        value = self.test_params.get(param_name)
        if value is not None:
            return value
        
        # Try DUT data
        value = self.dut_data.get(param_name)
        if value is not None:
            return value
        
        # Return default
        return default
    
    def wait_for_condition(self, condition_func, timeout=10, check_interval=0.5, log_callback=None):
        """
        Wait for a condition to be met
        
        Args:
            condition_func: Function that returns True when condition is met
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            log_callback: Optional logging function
            
        Returns:
            bool: True if condition met, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(check_interval)
        
        if log_callback:
            log_callback(f"Timeout waiting for condition after {timeout}s")
        return False
