"""
Test 02: Output Voltage Accuracy

This test verifies that the output voltage is within the specified accuracy
across different load conditions.
"""
from tests.base_test import BaseTest
import time

class OutputVoltageAccuracyTest(BaseTest):
    """Output voltage accuracy test"""
    
    def run(self, progress_callback, log_callback):
        """
        Test Sequence:
        1. Set nominal input voltage
        2. Turn on source
        3. Measure output voltage at no load
        4. Apply load steps (25%, 50%, 75%, 100%)
        5. Measure output voltage at each load
        6. Verify voltage accuracy within tolerance
        """
        
        # Step 1: Set nominal voltage
        nom_vin = float(self.get_param("Nominal Voltage", 48.0))
        nom_vout = float(self.get_param("Output Nominal V", 24.0))
        tolerance = 0.05  # 5% tolerance
        
        log_callback(f"Step 1: Setting Source Voltage to {nom_vin}V")
        self.mgr.ac_source.set_voltage(nom_vin)
        progress_callback(10)
        
        # Step 2: Turn on source
        log_callback("Step 2: Turning Source ON")
        self.mgr.ac_source.output_on()
        time.sleep(1)  # Stabilization time
        progress_callback(20)
        
        # Step 3: Measure at no load
        log_callback("Step 3: Measuring output voltage at no load")
        v_no_load = self.mgr.dc_load.measure_voltage()
        log_callback(f"  No Load Vout: {v_no_load:.3f}V")
        
        # Check accuracy
        error_pct = abs(v_no_load - nom_vout) / nom_vout * 100
        log_callback(f"  Error: {error_pct:.2f}%")
        progress_callback(30)
        
        # Step 4-5: Test at different load levels
        load_levels = [25, 50, 75, 100]  # Percentage of rated load
        rated_current = float(self.get_param("Power Rating", 100.0)) / nom_vout
        
        all_passed = True
        
        for i, load_pct in enumerate(load_levels):
            load_current = rated_current * (load_pct / 100.0)
            log_callback(f"Step {4+i}: Testing at {load_pct}% load ({load_current:.2f}A)")
            
            # Set load
            self.mgr.dc_load.set_mode("CC")
            self.mgr.dc_load.set_current(load_current)
            self.mgr.dc_load.load_on()
            time.sleep(2)  # Stabilization time
            
            # Measure voltage
            v_out = self.mgr.dc_load.measure_voltage()
            error_pct = abs(v_out - nom_vout) / nom_vout * 100
            
            log_callback(f"  Vout: {v_out:.3f}V, Error: {error_pct:.2f}%")
            
            # Check if within tolerance
            if error_pct > (tolerance * 100):
                log_callback(f"  ✗ FAIL: Exceeds {tolerance*100}% tolerance")
                all_passed = False
            else:
                log_callback(f"  ✓ PASS: Within tolerance")
            
            progress_callback(30 + (i + 1) * 15)
        
        # Turn off load
        self.mgr.dc_load.load_off()
        
        # Final result
        progress_callback(100)
        if all_passed:
            log_callback("✓ OVERALL PASS: Output voltage accuracy within specification")
            return "Pass"
        else:
            log_callback("✗ OVERALL FAIL: Output voltage accuracy out of specification")
            return "Fail"
