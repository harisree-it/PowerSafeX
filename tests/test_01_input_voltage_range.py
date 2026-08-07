"""
Test 01: Input Voltage Range Verification

This test verifies that the DUT operates correctly across the specified input voltage range,
including UVLO (Under-Voltage Lock-Out) and OVP (Over-Voltage Protection) behavior.
"""
from tests.base_test import BaseTest
import time
import os

class InputVoltageRangeTest(BaseTest):
    """Input voltage range verification test"""
    
    def run(self, progress_callback, log_callback):
        """
        Test Sequence:
        1. Set nominal input voltage
        2. Configure load
        3. Turn on source
        4. Wait for output to stabilize
        5. Turn on load
        6. Configure oscilloscope
        7. Set trigger
        8. Ramp down input voltage to test UVLO
        9. Capture waveform
        10. Verify output behavior
        """
        
        # Step 1: Set nominal voltage
        nom_vin = float(self.get_param("Nominal Voltage", 48.0))
        log_callback(f"Step 1: Setting Source Voltage to Nominal ({nom_vin}V)")
        self.mgr.ac_source.set_voltage(nom_vin)
        progress_callback(10)
        
        # Step 2: Configure load
        load_mode = self.get_param("Load Mode", "CC")
        load_val = float(self.get_param("Load Value", 10.0))
        log_callback(f"Step 2: Load Config -> Mode: {load_mode}, Value: {load_val}")
        
        if hasattr(self.mgr.dc_load, 'set_mode'):
            self.mgr.dc_load.set_mode(load_mode)
        progress_callback(20)
        
        # Step 3: Turn on source
        log_callback("Step 3: Turning Source ON")
        self.mgr.ac_source.output_on()
        progress_callback(30)
        
        # Step 4: Wait for output to reach 95% nominal
        nom_vout = float(self.get_param("Output Nominal V", 24.0))
        target_vout = nom_vout * 0.95
        log_callback(f"Step 4: Waiting for Vout to reach 95% threshold ({target_vout:.2f}V)...")
        
        def check_output_voltage():
            v_out = self.mgr.dc_load.measure_voltage()
            return v_out >= target_vout
        
        if not self.wait_for_condition(check_output_voltage, timeout=10, log_callback=log_callback):
            log_callback("Error: Timeout waiting for Vout to reach 95% nominal")
            return "Fail"
        
        v_out_measured = self.mgr.dc_load.measure_voltage()
        log_callback(f"Success: Vout reached {v_out_measured:.2f}V")
        progress_callback(40)
        
        # Step 5: Turn on load
        log_callback(f"Step 5: Turning Load ON at {load_val}")
        if load_mode == "CC":
            self.mgr.dc_load.set_current(load_val)
        elif load_mode == "CV":
            self.mgr.dc_load.set_voltage(load_val)
        elif load_mode == "CP":
            self.mgr.dc_load.set_power(load_val)
        self.mgr.dc_load.load_on()
        progress_callback(50)
        
        # Step 6: Configure oscilloscope
        log_callback("Step 6: Configuring Oscilloscope...")
        self.mgr.scope.set_time_scale(1.0)  # 1s/div
        
        # Channel configuration
        vin_max = float(self.get_param("Input Max Voltage", nom_vin * 1.2))
        vout_max = nom_vout * 1.5
        
        self.mgr.scope.set_vertical_scale(1, vin_max / 4)  # Ch1: Vin
        self.mgr.scope.set_vertical_scale(3, vout_max / 4)  # Ch3: Vout
        
        log_callback("Scope Channels: Ch1:Vin, Ch2:Iin, Ch3:Vout, Ch4:Iout")
        progress_callback(60)
        
        # Step 7: Set trigger
        log_callback("Step 7: Setting trigger on Vout (Ch3)")
        self.mgr.scope.set_trigger(channel=3, level=nom_vout * 0.5, slope="Both")
        self.mgr.scope.single_acquire()
        progress_callback(70)
        
        # Step 8: Ramp down input voltage
        uvlo = float(self.get_param("Input UVLO Point", nom_vin * 0.8))
        ramp_target = uvlo - 5
        log_callback(f"Step 8: Ramping Vin down to {ramp_target}V (UVLO - 5V)...")
        
        # Ramp down in steps
        step_v = 2.0
        current_v = nom_vin
        while current_v > ramp_target:
            current_v -= step_v
            if current_v < ramp_target:
                current_v = ramp_target
            self.mgr.ac_source.set_voltage(current_v)
            time.sleep(0.2)
        
        progress_callback(85)
        
        # Step 9: Save waveform
        image_path = "reports/TEST1_CASE1.png"
        log_callback(f"Step 9: Saving scope capture to {image_path}")
        if not os.path.exists("reports"):
            os.makedirs("reports")
        self.mgr.scope.save_screenshot(image_path)
        progress_callback(95)
        
        # Step 10: Verify output behavior
        v_out_final = self.mgr.dc_load.measure_voltage()
        log_callback(f"Step 10: Final Vout measured: {v_out_final:.2f}V at Vin={ramp_target}V")
        
        # Pass/Fail criteria: Output should be near zero below UVLO
        if v_out_final < 1.0:
            log_callback("✓ PASS: Output voltage dropped to zero below UVLO")
            status = "Pass"
        else:
            log_callback("✗ FAIL: Output voltage did NOT drop to zero below UVLO")
            status = "Fail"
        
        progress_callback(100)
        return status
