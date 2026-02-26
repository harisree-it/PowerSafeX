
import random
import numpy as np
import time
import os

# Try to import pyvisa, but don't fail if it's not available
try:
    import pyvisa
    PYVISA_AVAILABLE = True
except ImportError:
    PYVISA_AVAILABLE = False
    print("Warning: pyvisa not available. Only simulation mode will work.")

try:
    from tm_devices import DeviceManager
    TM_DEVICES_AVAILABLE = True
except ImportError:
    TM_DEVICES_AVAILABLE = False
    print("Warning: tm_devices not available.")

class Instrument:
    def __init__(self, resource_name, simulation_mode=True, logger=None, on_error=None):
        self.resource_name = resource_name
        self.simulation_mode = simulation_mode
        self.connected = False
        self.instr = None  # VISA instrument handle
        self.logger = logger
        self.on_error = on_error # Callback for persistent errors
        self.force_comm_error = False # Debug flag
        
    def connect(self):
        """Connect to the instrument with retries and error handling."""
        while True:
            for attempt in range(1, 11):
                try:
                    if self.force_comm_error:
                        raise Exception("Forced Communication Error (Debug Mode)")

                    if self.simulation_mode:
                        # Simulation mode - just pretend to connect
                        msg = f"[{self.__class__.__name__}] Simulating connection to {self.resource_name}..."
                        print(msg)
                        if self.logger: self.logger(msg)
                        time.sleep(0.5)
                        self.connected = True
                        return True
                    else:
                        # Real VISA connection
                        if not PYVISA_AVAILABLE:
                            raise Exception("pyvisa library not available. Cannot connect to real instruments.")
                        
                        msg = f"[{self.__class__.__name__}] Connecting to {self.resource_name}..."
                        print(msg)
                        if self.logger: self.logger(msg)
                        rm = pyvisa.ResourceManager()
                        
                        # Validation: Check if resource is available
                        try:
                            available_resources = rm.list_resources()
                            if self.resource_name not in available_resources:
                                 print(f"Warning: {self.resource_name} not found in listed resources: {available_resources}")
                        except Exception as val_e:
                            print(f"Resource listing failed: {val_e}")

                        self.instr = rm.open_resource(self.resource_name)
                        self.instr.timeout = 5000
                        self.instr.write_termination = '\n'
                        self.instr.read_termination = '\n'
                        
                        # Test connection with IDN query
                        try:
                            idn = self.query("*IDN?")
                            msg = f"[{self.__class__.__name__}] Connected: {idn.strip()}"
                            print(msg)
                            if self.logger: self.logger(msg)
                        except:
                            msg = f"[{self.__class__.__name__}] Connected (IDN query not supported)"
                            print(msg)
                            if self.logger: self.logger(msg)
                        
                        self.connected = True
                        return True

                except Exception as e:
                    err_msg = f"[{self.__class__.__name__}] Connection Error (Attempt {attempt}/10): {e}"
                    print(err_msg)
                    if self.logger: self.logger(err_msg)
                    self.connected = False
                    
                    if attempt < 10:
                        time.sleep(0.5)
                    else:
                        if self.on_error:
                            choice = self.on_error(f"Failed to Connect to {self.resource_name}\nError: {e}")
                            if choice == "Retry":
                                break # Restart attempts
                            else:
                                raise Exception(f"Connection Aborted by User: {e}")
                        else:
                            raise e
    
    def disconnect(self):
        """Disconnect from the instrument."""
        if self.instr is not None:
            try:
                self.instr.close()
                msg = f"[{self.__class__.__name__}] Disconnected from {self.resource_name}"
                print(msg)
                if self.logger: self.logger(msg)
            except:
                pass
            self.instr = None
        self.connected = False
    
    def write(self, command):
        """Send a SCPI command to the instrument with retries."""
        msg = f"[{self.__class__.__name__}] TX: {command}"
        print(msg)
        if self.logger: self.logger(msg)
        
        while True:
            for attempt in range(1, 11):
                try:
                    if self.force_comm_error:
                        raise Exception("Forced Communication Error (Debug Mode)")

                    if self.simulation_mode:
                        return # Success in simulation (unless forced error)

                    if self.instr is None:
                        raise Exception("Not connected to instrument")
                    self.instr.write(command)
                    return # Success
                except Exception as e:
                    err_msg = f"[{self.__class__.__name__}] Write Error (Attempt {attempt}/10): {e}"
                    print(err_msg)
                    if self.logger: self.logger(err_msg)
                    if attempt < 10:
                        time.sleep(0.5)
                    else:
                        if self.on_error:
                            choice = self.on_error(f"Communication Failure on {self.resource_name}\nError: {e}")
                            if choice == "Retry":
                                break # Restart attempts
                            else:
                                raise Exception(f"Communication Aborted by User: {e}")
                        else:
                            raise e

    def query(self, command):
        """Send a SCPI query and return the response with retries."""
        msg = f"[{self.__class__.__name__}] TX: {command}"
        print(msg)
        if self.logger: self.logger(msg)
        
        while True:
            for attempt in range(1, 11):
                try:
                    if self.force_comm_error:
                        raise Exception("Forced Communication Error (Debug Mode)")

                    if self.simulation_mode:
                        resp = "SIMULATED_RESPONSE"
                        msg = f"[{self.__class__.__name__}] RX: {resp}"
                        print(msg)
                        if self.logger: self.logger(msg)
                        return resp

                    if self.instr is None:
                        raise Exception("Not connected to instrument")
                    resp = self.instr.query(command).strip()
                    msg = f"[{self.__class__.__name__}] RX: {resp}"
                    print(msg)
                    if self.logger: self.logger(msg)
                    return resp
                except Exception as e:
                    err_msg = f"[{self.__class__.__name__}] Query Error (Attempt {attempt}/10): {e}"
                    print(err_msg)
                    if self.logger: self.logger(err_msg)
                    if attempt < 10:
                        time.sleep(0.5)
                    else:
                        if self.on_error:
                            choice = self.on_error(f"Communication Failure on {self.resource_name}\nError: {e}")
                            if choice == "Retry":
                                break # Restart attempts
                            else:
                                raise Exception(f"Communication Aborted by User: {e}")
                        else:
                            raise e
        
    def query_idn(self):
        if self.simulation_mode:
            return "Generic,Instrument,0000,1.0"
        else:
            try:
                return self.query("*IDN?")
            except:
                return "Unknown Instrument"

class ChromaPowerSupply(Instrument):
    """Driver for Chroma 62000D Series DC Bidirectional Power Supply"""
    
    def __init__(self, resource_name, simulation_mode=True, model="62000D", logger=None, on_error=None):
        super().__init__(resource_name, simulation_mode, logger=logger, on_error=on_error)
        self.model = model
        
        # Import command library
        from instruments.chroma import get_command_set
        self.cmd = get_command_set(model)
        if self.cmd is None:
            raise ValueError(f"Unknown Chroma model: {model}")
        
        # Internal state for simulation
        self._target_voltage = 0.0
        self._current_limit = 0.0
        self._output_on = False
        
    def set_voltage(self, voltage):
        """Set output voltage in Volts"""
        self._target_voltage = float(voltage)
        if self.simulation_mode:
            print(f"[PowerSupply] Set Voltage: {self._target_voltage}V")
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE, self._target_voltage))
    
    def set_current_limit(self, current):
        """Set current limit in Amperes"""
        self._current_limit = float(current)
        if self.simulation_mode:
            print(f"[PowerSupply] Set Current Limit: {self._current_limit}A")
        self.write(self.cmd.format_command(self.cmd.SOURCE_CURRENT, self._current_limit))
    
    def set_power_limit(self, power):
        """Set power limit in Watts"""
        if self.simulation_mode:
            print(f"[PowerSupply] Set Power Limit: {power}W")
        self.write(self.cmd.format_command(self.cmd.SOURCE_POWER, power))
    
    def output_on(self):
        """Turn output ON"""
        self._output_on = True
        if self.simulation_mode:
            print(f"[PowerSupply] Output ON")
        self.write(self.cmd.format_command(self.cmd.CONFIGURE_OUTPUT, "ON"))
    
    def output_off(self):
        """Turn output OFF"""
        self._output_on = False
        if self.simulation_mode:
            print(f"[PowerSupply] Output OFF")
        self.write(self.cmd.format_command(self.cmd.CONFIGURE_OUTPUT, "OFF"))
    
    def measure_voltage(self):
        """Measure output voltage"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_VOLTAGE)
            return self._target_voltage + random.uniform(-0.1, 0.1)
        else:
            response = self.query(self.cmd.MEASURE_VOLTAGE)
            return float(response)
    
    def measure_current(self):
        """Measure output current"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_CURRENT)
            if self._output_on:
                return self._current_limit * 0.8 + random.uniform(-0.05, 0.05)
            return 0.0
        else:
            response = self.query(self.cmd.MEASURE_CURRENT)
            return float(response)
    
    def measure_power(self):
        """Measure output power"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_POWER)
            v = self._target_voltage + random.uniform(-0.1, 0.1)
            i = 0.0
            if self._output_on:
                i = self._current_limit * 0.8 + random.uniform(-0.05, 0.05)
            return v * i
        else:
            response = self.query(self.cmd.MEASURE_POWER)
            return float(response)
    
    def set_voltage_slew_rate(self, slew_rate):
        """Set voltage slew rate in V/ms"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE_SLEW, slew_rate))
    
    def set_current_slew_rate(self, slew_rate):
        """Set current slew rate in A/ms"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_CURRENT_SLEW, slew_rate))
    
    def set_ovp(self, voltage):
        """Set over-voltage protection level"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE_PROTECT_HIGH, voltage))
    
    def set_ocp(self, current):
        """Set over-current protection level"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_CURRENT_PROTECT_HIGH, current))
    
    def get_status(self):
        """Get instrument status"""
        if self.simulation_mode:
            self.query(self.cmd.FETCH_STATUS)
            return "OK"
        else:
            response = self.query(self.cmd.FETCH_STATUS)
            return response
    
    def reset(self):
        """Reset instrument to default state"""
        self.write(self.cmd.RST)
    
    def set_frequency(self, frequency):
        """Set output frequency in Hz"""
        if self.simulation_mode:
            print(f"[PowerSupply] Set Frequency: {frequency}Hz")
        self.write(self.cmd.format_command(self.cmd.SOURCE_FREQUENCY, frequency))

    def set_voltage_rise(self, rate):
        """Set voltage rise rate (V/ms)"""
        self.write(self.cmd.format_command("SOURce:VOLTage:RISE", rate))

    def set_voltage_fall(self, rate):
        """Set voltage fall rate (V/ms)"""
        self.write(self.cmd.format_command("SOURce:VOLTage:FALL", rate))

    def clear_protection(self):
        """Clear protection status"""
        self.write("SOURce:PROTect:CLEar")

    def measure_frequency(self):
        """Measure output frequency"""
        if self.simulation_mode:
            self.query("MEASure:FREQuency?")
            return 50.0 + random.uniform(-0.1, 0.1)
        else:
            return float(self.query("MEASure:FREQuency?"))

    def measure_apparent_power(self):
        """Measure apparent power"""
        if self.simulation_mode:
            self.query("MEASure:POWer:APParent?")
            return (self._target_voltage * self._current_limit * 0.8) * 1.1 
        else:
            return float(self.query("MEASure:POWer:APParent?"))

    def measure_pf(self):
        """Measure power factor"""
        if self.simulation_mode:
            self.query("MEASure:POWer:PF?")
            return 0.95 + random.uniform(-0.01, 0.01)
        else:
            return float(self.query("MEASure:POWer:PF?"))

class ChromaElectronicLoad(Instrument):
    def __init__(self, resource_name, simulation_mode=True, logger=None, on_error=None):
        super().__init__(resource_name, simulation_mode, logger=logger, on_error=on_error)
        self._mode = "CC"
        self._value = 0.0
        self._load_on = False

    def query_idn(self):
        if self.simulation_mode:
            self.query("*IDN?")
            return "Chroma,6310A,SN67890,FW2.0"
        else:
            return super().query_idn()

    def set_mode(self, mode):
        self._mode = mode
        print(f"[E-Load] Set Mode: {mode}")
        # Basic mapping, might need specific commands per model
        mode_map = {"CC": "CURR", "CV": "VOLT", "CR": "RES", "CP": "POW"}
        cmd_str = mode_map.get(mode, "CURR")
        self.write(f"MODE {cmd_str}")
        
    def set_current(self, current):
        self._value = float(current)
        print(f"[E-Load] Set Current: {self._value}A")
        if self._mode == "CC":
             self.write(f"CURR:STAT:L1 {current}")

    def set_voltage(self, voltage):
        self._value = float(voltage)
        print(f"[E-Load] Set Voltage: {self._value}V")
        if self._mode == "CV":
             self.write(f"VOLT:STAT:L1 {voltage}")

    def set_power(self, power):
        self._value = float(power)
        print(f"[E-Load] Set Power: {self._value}W")
        if self._mode == "CP":
             self.write(f"POW:STAT:L1 {power}")
    
    def set_resistance(self, resistance):
        self._value = float(resistance)
        print(f"[E-Load] Set Resistance: {self._value}Ohm")
        if self._mode == "CR":
             self.write(f"RES:STAT:L1 {resistance}")
        
    def set_current_limit(self, current):
        print(f"[E-Load] Limit Current: {current}A")
        
    def load_on(self):
        self._load_on = True
        print("[E-Load] Load ON")
        self.write("LOAD ON")
        
    def load_off(self):
        self._load_on = False
        print("[E-Load] Load OFF")
        self.write("LOAD OFF")

    def set_slew_rate(self, rate):
        print(f"[E-Load] Set Slew Rate: {rate}A/us")
        self.write(f"CURR:DYN:RISE {rate}")
        self.write(f"CURR:DYN:FALL {rate}")

    def set_dynamic_mode(self, enable):
        state = "ON" if enable else "OFF"
        print(f"[E-Load] Dynamic Mode: {state}")
        self.write(f"CURR:DYN {state}")

    def clear_protection(self):
        print("[E-Load] Clear Protection")
        self.write("PROT:CLE")

    def set_ocp(self, current):
         print(f"[E-Load] Set OCP: {current}A")
         self.write(f"CURR:PROT {current}")

    def set_ovp(self, voltage):
         print(f"[E-Load] Set OVP: {voltage}V")
         self.write(f"VOLT:PROT {voltage}")

    def set_opp(self, power):
         print(f"[E-Load] Set OPP: {power}W")
         self.write(f"POW:PROT {power}")
        
    def measure_voltage(self):
        # In simulation, we need to know what the Source is doing
        try:
            from instruments.manager import InstrumentManager
            mgr = InstrumentManager()
            srcs = mgr.get_instruments_by_role("Source")
            if srcs:
                pass
        except:
            pass
        
        if self.simulation_mode:
             self.query("MEAS:VOLT?")
             return 24.0 + random.uniform(-0.1, 0.1)
        else:
             return float(self.query("MEAS:VOLT?"))
    
    def measure_current(self):
        if self.simulation_mode:
             self.query("MEAS:CURR?")
             if not self._load_on: return 0.0
             return self._value + random.uniform(-0.01, 0.01)
        else:
             return float(self.query("MEAS:CURR?"))

    def measure_resistance(self):
        if self.simulation_mode:
            self.query("MEAS:RES?")
            return 10.0 + random.uniform(-0.1, 0.1)
        else:
            return float(self.query("MEAS:RES?"))

class TektronixScope(Instrument):
    def connect(self):
        """Connect to Tektronix Scope and set specific termination settings."""
        if self.simulation_mode:
            return super().connect()
            
        # Call standard connect to open resource
        result = super().connect()
        
        if result and self.instr:
            # ROBUST INITIALIZATION FOR MSO44B
            try:
                # 1. Clear the interface to remove any stale data in buffers
                self.instr.clear()
                
                # 2. Set termination - Critical for MSO44B SCPI
                self.instr.write_termination = '\n'
                self.instr.read_termination = '\n'
                
                # 3. Increase timeout for slow operations
                self.instr.timeout = 20000 
                
                # 4. Optimized chunk size
                self.instr.chunk_size = 102400
                
                print(f"[Scope] Connected with robust settings (Term: \\n, Timeout: 20s)")
            except Exception as e:
                print(f"[Scope] Warning during post-connect setup: {e}")
                
        return result

    def disconnect(self):
        """Disconnect from the instrument."""
        # Standard disconnect is sufficient for PyVISA
        super().disconnect()
        # Ensure specific flags are cleared if any
        pass

    def run(self):
        print("[Scope] RUN")
        self.write("ACQ:STATE RUN")

    def stop(self):
        print("[Scope] STOP")
        self.write("ACQ:STATE STOP")
    
    def single(self):
        print("[Scope] SINGLE")
        self.write("ACQ:STOPA SEQ")

    def set_vertical_scale(self, channel, scale):
        print(f"[Scope] Ch{channel} Vertical Scale: {scale}V/div")
        self.write(f"CH{channel}:SCALE {scale}")

    def set_vertical_offset(self, channel, offset):
        print(f"[Scope] Ch{channel} Offset: {offset}V")
        self.write(f"CH{channel}:OFFSET {offset}")
             
    def set_coupling(self, channel, coupling):
        print(f"[Scope] Ch{channel} Coupling: {coupling}")
        self.write(f"CH{channel}:COUP {coupling}")

    def set_bandwidth(self, channel, limit):
        # Limit is typically '20E6' or 'FULL'
        print(f"[Scope] Ch{channel} Bandwidth: {limit}")
        self.write(f"CH{channel}:BANDWIDTH {limit}")

    def set_time_scale(self, scale):
        print(f"[Scope] Horizontal Scale: {scale}s/div")
        self.write(f"HOR:SCALE {scale}")

    def set_delay(self, delay):
        print(f"[Scope] Horizontal Delay: {delay}s")
        self.write(f"HOR:DELAY:TIME {delay}")

    def enable_channel(self, channel, state):
        state_str = "ON" if state else "OFF"
        print(f"[Scope] Ch{channel} Enable: {state_str}")
        self.write(f"SELect:CH{channel} {state_str}")

    def set_trigger(self, channel, level, slope):
        print(f"[Scope] Trigger on Ch{channel}, Level: {level}, Slope: {slope}")
        self.write("TRIG:A:TYPE EDGE")
        self.write(f"TRIG:A:EDGE:SOUR CH{channel}")
        self.write(f"TRIG:A:LEVEL {level}")
        self.write(f"TRIG:A:EDGE:SLOPE {slope}")

    def single_acquire(self):
        print("[Scope] Single Acquisition Armed") # Kept for backward compat
        self.write("ACQ:STOPA SEQ") # Same as single()

    def auto_set(self):
        """Perform Autoset"""
        print("[Scope] Autoset Executing...")
        self.write("AUTOSet EXECute")
        if not self.simulation_mode:
            time.sleep(2) # Wait for autoset to complete
        else:
            time.sleep(0.5) # Faster simulation

    def configure_measurement(self, meas_num, meas_type, channel):
        """Configure a measurement. meas_num: 1-8"""
        print(f"[Scope] Config Meas{meas_num}: {meas_type} on Ch{channel}")
        self.write(f"MEASU:MEAS{meas_num}:TYPE {meas_type}")
        self.write(f"MEASU:MEAS{meas_num}:SOUR CH{channel}")
        self.write(f"MEASU:MEAS{meas_num}:STATE ON")

    def get_measurement(self, meas_num):
        """Get measurement value"""
        if self.simulation_mode:
            self.query(f"MEASU:MEAS{meas_num}:VAL?")
            return random.uniform(0, 100)
        else:
            return float(self.query(f"MEASU:MEAS{meas_num}:VAL?"))

    def save_screenshot(self, filename):
        print(f"[Scope] Request to save screenshot to {filename}")
        
        # Ensure directory exists locally
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
        if self.simulation_mode:
            # Create a dummy image
            print("[Scope] Simulation mode: Generating mock image.")
            self.write(f'SAVE:IMAGe "{filename}"') # Log intended command
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (800, 600), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((10,10), f"Mock Scope Screenshot\n{filename}", fill=(255,255,0))
            points = []
            for x in range(0, 800, 10):
                y = 300 + 100 * np.sin(x/50)
                points.append((x, y))
            d.line(points, fill=(0, 255, 0), width=3)
            img.save(filename)
            return

        # Real instrument screenshot capture - ROBUST MANUAL SEQUENCING
        try:
            print("[Scope] Starting screenshot capture (Robust PyVISA Method)...")
            
            # 1. Use internal Tek path (C: maps to internal storage on Linux scopes)
            # Simple filename to avoid path issues
            scope_temp_file = "C:/temp.png"
            
            # 2. Cleanup previous
            try:
                self.write(f'FILESystem:DELEte "{scope_temp_file}"')
                time.sleep(0.5)
            except:
                pass

            # 3. Configure
            try:
                self.write("HEADER OFF")
                self.write("SAVE:IMAG:FILEF PNG")
            except:
                pass

            # 4. Save to internal storage
            print(f"[Scope] Saving to internal path: {scope_temp_file}")
            self.write(f'SAVE:IMAGe "{scope_temp_file}"')
            
            # 5. Wait for operation (Non-blocking sleep is safer than *OPC? on busy scope)
            time.sleep(5.0) 
            
            # 6. Check error queue
            try:
               err = self.query("SYSTem:ERRor?")
               if "No error" not in err and "0," not in err:
                   print(f"[Scope] Warning after save: {err}")
            except:
                pass
                
            # 7. Transfer file
            print(f"[Scope] Transferring file...")
            # Use query_binary_values which handles the #<header> logic automatically
            raw_data_list = self.instr.query_binary_values(
                f'FILESystem:READFile "{scope_temp_file}"', 
                datatype='B', 
                header_fmt='ieee',
                is_big_endian=False,
                chunk_size=102400
            )
            
            raw_data = bytes(raw_data_list)
            
            if not raw_data:
                 # Try traditional read_raw fallback if above fails? 
                 # Usually query_binary_values is safest for Tek.
                 raise Exception("No data received from scope file read")

            # 8. Save locally
            with open(filename, "wb") as f:
                f.write(raw_data)
                
            print(f"[Scope] Screenshot saved to {filename}: {len(raw_data)} bytes")
            
            # 9. Cleanup
            self.write(f'FILESystem:DELEte "{scope_temp_file}"')
                
        except Exception as e:
            print(f"[Scope] CRITICAL FAILURE in save_screenshot: {e}")
            raise

            

    def setup_channel(self, channel, scale, coupling="DC"):
        print(f"[Scope] Setup {channel}: {scale}V/div, {coupling}")
        
    def set_timebase(self, scale):
        print(f"[Scope] Set Timebase: {scale}s/div")
        
    def capture_waveform(self, channel="CH1"):
        t = np.linspace(0, 0.02, 1000)
        freq = 50
        noise = np.random.normal(0, 0.5, t.shape)
        voltage = 24 + 5 * np.sin(2 * np.pi * freq * t) + noise
        return t, voltage
