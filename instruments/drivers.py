
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

    # --- Load Interface Aliases for Bidirectional Use ---
    def set_mode(self, mode):
        """Alias for load compatibility. Switches Bidirectional supply to LOAD mode."""
        self._is_load_mode = True
        if self.simulation_mode:
            print(f"[PowerSupply] Set Mode (Bidirectional): {mode}")
        self.write(self.cmd.format_command(self.cmd.SYSTEM_MODE, "LOAD"))

    def set_current(self, current):
        """Alias for set_current_limit when used as a load"""
        if getattr(self, '_is_load_mode', False):
            self._current_limit = float(current)
            if self.simulation_mode:
                print(f"[PowerSupply] Set Load Current: {self._current_limit}A")
            self.write(self.cmd.format_command(self.cmd.LOAD_CURRENT, self._current_limit))
        else:
            self.set_current_limit(current)

    def set_power(self, power):
        """Alias for set_power_limit when used as a load"""
        if getattr(self, '_is_load_mode', False):
            if self.simulation_mode:
                print(f"[PowerSupply] Set Load Power: {power}W")
            self.write(self.cmd.format_command(self.cmd.LOAD_POWER, power))
        else:
            self.set_power_limit(power)

    def load_on(self):
        """Alias for output_on"""
        self.output_on()

    def load_off(self):
        """Alias for output_off"""
        self.output_off()
    
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


class ChromaAcSource(Instrument):
    """Driver for Chroma 61500 Series AC Power Source (61501/61505/61507/61509/61512).

    Maps to mgr.ac_source when the instrument type is 'AC Source'.
    SCPI reference: Chroma 61500 Series Programming Manual.
    """

    def __init__(self, resource_name, simulation_mode=True, model="61509", logger=None, on_error=None):
        super().__init__(resource_name, simulation_mode, logger=logger, on_error=on_error)
        self.model = model

        from instruments.chroma import get_command_set
        self.cmd = get_command_set(model)
        if self.cmd is None:
            raise ValueError(f"Unknown Chroma AC source model: {model}")

        # Simulation state
        self._voltage  = 0.0
        self._freq     = 50.0
        self._current_limit = 0.0
        self._output_on = False
        self._waveform = "SINE"
        self._phase    = 0.0

    # ── Output Control ────────────────────────────────────────────
    def output_on(self):
        """Enable AC output — SCPI: OUTPut:STATe ON"""
        self._output_on = True
        self.write(self.cmd.format_command(self.cmd.OUTPUT_STATE, "ON"))

    def output_off(self):
        """Disable AC output — SCPI: OUTPut:STATe OFF"""
        self._output_on = False
        self.write(self.cmd.format_command(self.cmd.OUTPUT_STATE, "OFF"))

    # ── Voltage ───────────────────────────────────────────────────
    def set_voltage(self, voltage):
        """Set RMS output voltage — SCPI: SOURce:VOLTage:LEVel <V>"""
        self._voltage = float(voltage)
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE_LEVEL, self._voltage))

    def set_voltage_range(self, range_str):
        """Set voltage range — SCPI: SOURce:VOLTage:RANGe LOW|HIGH"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE_RANGE, range_str.upper()))

    def set_voltage_slew(self, rate):
        """Set voltage slew rate (V/s) — SCPI: SOURce:VOLTage:SLEW <rate>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_VOLTAGE_SLEW, rate))

    def set_ovp(self, voltage):
        """Set OVP threshold — SCPI: SOURce:VOLTage:PROTect:LEVel <V>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_OVP, voltage))

    # ── Frequency ─────────────────────────────────────────────────
    def set_frequency(self, freq):
        """Set output frequency (Hz) — SCPI: SOURce:FREQuency:LEVel <Hz>"""
        self._freq = float(freq)
        self.write(self.cmd.format_command(self.cmd.SOURCE_FREQUENCY_LEVEL, self._freq))

    def set_frequency_slew(self, rate):
        """Set frequency slew rate (Hz/s) — SCPI: SOURce:FREQuency:SLEW <rate>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_FREQUENCY_SLEW, rate))

    # ── Current / Protection ──────────────────────────────────────
    def set_current_limit(self, current):
        """Set RMS current limit — SCPI: SOURce:CURRent:LIMit <A>"""
        self._current_limit = float(current)
        self.write(self.cmd.format_command(self.cmd.SOURCE_CURRENT_LIMIT, self._current_limit))

    def set_ocp(self, current):
        """Set OCP threshold — SCPI: SOURce:CURRent:PROTect:LEVel <A>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_OCP, current))

    def clear_protection(self):
        """Clear latched protection — SCPI: SOURce:PROTect:CLEar"""
        self.write(self.cmd.SOURCE_PROTECT_CLEAR)

    # ── Phase ─────────────────────────────────────────────────────
    def set_phase(self, angle):
        """Set output phase angle (0–360 deg) — SCPI: SOURce:PHASe:ANGLe <deg>"""
        self._phase = float(angle)
        self.write(self.cmd.format_command(self.cmd.SOURCE_PHASE_ANGLE, self._phase))

    def set_phase_on(self, angle):
        """Set phase at output-on — SCPI: SOURce:PHASe:STARt <deg>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_PHASE_START, angle))

    def set_phase_off(self, angle):
        """Set phase at output-off — SCPI: SOURce:PHASe:STOP <deg>"""
        self.write(self.cmd.format_command(self.cmd.SOURCE_PHASE_STOP, angle))

    # ── Waveform ──────────────────────────────────────────────────
    def set_waveform(self, shape):
        """Set output waveform shape — SCPI: SOURce:WAVeform:SHAPe SINE|SQUare|USER<n>"""
        self._waveform = shape.upper()
        self.write(self.cmd.format_command(self.cmd.SOURCE_WAVEFORM_SHAPE, self._waveform))

    # ── Measurements ──────────────────────────────────────────────
    def measure_voltage(self):
        """Measure RMS output voltage — SCPI: MEASure:VOLTage:RMS?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_VOLTAGE_RMS)
            return self._voltage + random.uniform(-0.2, 0.2)
        return float(self.query(self.cmd.MEASURE_VOLTAGE_RMS))

    def measure_current(self):
        """Measure RMS output current — SCPI: MEASure:CURRent:RMS?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_CURRENT_RMS)
            return (self._current_limit * 0.7 + random.uniform(-0.05, 0.05)) if self._output_on else 0.0
        return float(self.query(self.cmd.MEASURE_CURRENT_RMS))

    def measure_current_peak(self):
        """Measure peak output current — SCPI: MEASure:CURRent:PEAK?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_CURRENT_PEAK)
            return self.measure_current() * 1.414
        return float(self.query(self.cmd.MEASURE_CURRENT_PEAK))

    def measure_power(self):
        """Measure real (active) power (W) — SCPI: MEASure:POWer:REAL?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_POWER_REAL)
            return self._voltage * self.measure_current() * 0.95
        return float(self.query(self.cmd.MEASURE_POWER_REAL))

    def measure_apparent_power(self):
        """Measure apparent power (VA) — SCPI: MEASure:POWer:APParent?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_POWER_APPARENT)
            return self._voltage * self.measure_current()
        return float(self.query(self.cmd.MEASURE_POWER_APPARENT))

    def measure_pf(self):
        """Measure power factor — SCPI: MEASure:POWer:PFACtor?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_POWER_FACTOR)
            return 0.95 + random.uniform(-0.02, 0.02)
        return float(self.query(self.cmd.MEASURE_POWER_FACTOR))

    def measure_frequency(self):
        """Measure actual output frequency — SCPI: MEASure:FREQuency?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_FREQUENCY)
            return self._freq + random.uniform(-0.01, 0.01)
        return float(self.query(self.cmd.MEASURE_FREQUENCY))

    def measure_crest_factor(self):
        """Measure current crest factor — SCPI: MEASure:CURRent:CREStfactor?"""
        if self.simulation_mode:
            self.query(self.cmd.MEASURE_CREST_FACTOR)
            return 1.414 + random.uniform(-0.05, 0.05)
        return float(self.query(self.cmd.MEASURE_CREST_FACTOR))

    def get_status(self):
        """Query error queue — SCPI: SYSTem:ERRor?"""
        if self.simulation_mode:
            self.query(self.cmd.SYSTEM_ERROR)
            return "0,No error"
        return self.query(self.cmd.SYSTEM_ERROR)

    def reset(self):
        """Reset to factory defaults — SCPI: *RST"""
        self.write(self.cmd.RST)


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
        self.write(f"CONF:MODE {mode}")
        
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
        self.write(f"CURR:STAT:RISE {rate}")
        self.write(f"CURR:STAT:FALL {rate}")
        self.write(f"CURR:DYN:RISE {rate}")
        self.write(f"CURR:DYN:FALL {rate}")

    def set_dynamic_mode(self, enable):
        print(f"[E-Load] Dynamic Mode: {'ON' if enable else 'OFF'}")
        if self._mode == "CC":
            mode_str = "CCD" if enable else "CC"
            self.write(f"CONF:MODE {mode_str}")
        elif self._mode == "CR":
            mode_str = "CRD" if enable else "CR"
            self.write(f"CONF:MODE {mode_str}")
        else:
            print(f"[E-Load] Dynamic Mode not supported for {self._mode}")

    def clear_protection(self):
        print("[E-Load] Clear Protection")
        self.write("PROT:CLE")

    def set_ocp(self, current):
         print(f"[E-Load] Set OCP: {current}A")
         self.write(f"CONF:CURR:PROT {current}")

    def set_ovp(self, voltage):
         print(f"[E-Load] Set OVP: {voltage}V")
         self.write(f"CONF:VOLT:PROT {voltage}")

    def set_opp(self, power):
         print(f"[E-Load] Set OPP: {power}W")
         self.write(f"CONF:POW:PROT {power}")
        
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
        """Capture a scope screenshot and save it to a local file.

        Strategy (Tektronix MSO/DPO series):
          1. Primary: HARDCopy — scope streams PNG binary directly over USB.
             The response is an IEEE 488.2 definite-length block (#<N><len><bytes>)
             or raw PNG bytes; we handle both cases.
          2. Fallback: SAVE:IMAGe to scope internal C:/temp.png, wait, then
             FILESystem:READFile with manual IEEE-header stripping.

        The image is always saved to `filename` on the local PC.
        """
        import os
        print(f"[Scope] Screenshot requested → {filename}")
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

        # ── Simulation mode ──────────────────────────────────────────────────
        if self.simulation_mode:
            print("[Scope] Simulation: generating mock screenshot.")
            self.write('SAVE:IMAGe "C:/temp.png"')   # log command only
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (800, 600), color=(30, 40, 60))
                d = ImageDraw.Draw(img)
                d.text((10, 10), f"[SIM] Scope Screenshot\n{filename}", fill=(0, 255, 128))
                pts = [(x, 300 + int(100 * np.sin(x / 50))) for x in range(0, 800, 5)]
                d.line(pts, fill=(0, 255, 0), width=2)
                img.save(filename)
                print(f"[Scope] Simulation screenshot saved: {filename}")
            except ImportError:
                # PIL not available — write a 1x1 blank PNG
                _blank_png = (
                    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
                    b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
                    b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
                    b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
                )
                with open(filename, 'wb') as f:
                    f.write(_blank_png)
            return

        # ── Real instrument ───────────────────────────────────────────────────
        raw_data = None

        # ── Method 1: HARDCopy direct streaming ──────────────────────────────
        try:
            print("[Scope] Method 1: HARDCopy direct stream…")
            instr = self.instr

            # Configure image format
            self.write("HARDCopy:PORT USB")
            self.write("SAVE:IMAG:FILEF PNG")
            self.write("HARDCOPY INKSAVER, OFF")
            time.sleep(0.3)

            # Initiate and read the binary response
            instr.write("HARDCopy STARt")

            # Use read_raw with a generous timeout and disable termination for binary transfer
            old_timeout = instr.timeout
            old_term = instr.read_termination
            instr.timeout = 30000   # 30 s — scope needs time to render
            instr.read_termination = None
            try:
                raw_bytes = instr.read_raw()
            finally:
                instr.timeout = old_timeout
                instr.read_termination = old_term

            if raw_bytes:
                raw_data = self._strip_ieee_header(raw_bytes)
                if raw_data and raw_data[:4] == b'\x89PNG':
                    print(f"[Scope] HARDCopy stream OK: {len(raw_data)} bytes")
                else:
                    print("[Scope] HARDCopy data did not look like PNG — trying fallback")
                    raw_data = None
        except Exception as hc_err:
            print(f"[Scope] HARDCopy method failed: {hc_err} — trying fallback")
            raw_data = None

        # ── Method 2: SAVE:IMAGe → FILESystem:READFile ──────────────────────
        if raw_data is None:
            try:
                print("[Scope] Method 2: SAVE:IMAGe + FILESystem:READFile…")
                scope_path = "C:/temp_cap.png"
                instr = self.instr

                # Delete any stale file
                try:
                    self.write(f'FILESystem:DELEte "{scope_path}"')
                    time.sleep(0.3)
                except Exception:
                    pass

                self.write("HEADER OFF")
                self.write("SAVE:IMAG:FILEF PNG")
                self.write(f'SAVE:IMAGe "{scope_path}"')

                # Wait for the file to be written — use *OPC? with a long timeout
                old_timeout = instr.timeout
                instr.timeout = 30000
                try:
                    instr.query("*OPC?")
                except Exception:
                    time.sleep(5)   # fallback if OPC? not supported
                finally:
                    instr.timeout = old_timeout

                # Read the file — use read_raw to get IEEE block, then strip header
                old_timeout = instr.timeout
                old_term = instr.read_termination
                instr.timeout = 30000
                instr.read_termination = None
                try:
                    instr.write(f'FILESystem:READFile "{scope_path}"')
                    raw_bytes = instr.read_raw()
                finally:
                    instr.timeout = old_timeout
                    instr.read_termination = old_term

                raw_data = self._strip_ieee_header(raw_bytes)

                if raw_data and raw_data[:4] == b'\x89PNG':
                    print(f"[Scope] FILESystem:READFile OK: {len(raw_data)} bytes")
                else:
                    raise Exception(
                        f"Received {len(raw_bytes)} bytes but PNG header not found. "
                        f"First bytes: {raw_bytes[:16]!r}"
                    )

                # Cleanup scope-side file
                try:
                    self.write(f'FILESystem:DELEte "{scope_path}"')
                except Exception:
                    pass

            except Exception as fb_err:
                raise RuntimeError(
                    f"All screenshot methods failed.\n"
                    f"Last error: {fb_err}"
                ) from fb_err

        # ── Write to local PC ─────────────────────────────────────────────────
        with open(filename, "wb") as fh:
            fh.write(raw_data)
        print(f"[Scope] Screenshot saved: {filename}  ({len(raw_data):,} bytes)")

    @staticmethod
    def _strip_ieee_header(data: bytes) -> bytes:
        """Strip an IEEE 488.2 definite-length block header from binary data.

        A definite-length block starts with '#' followed by one digit (N)
        indicating how many digits describe the byte count, followed by N
        digits giving the byte count, followed by the actual data.
        Example:  #7 0004096 <bytes...>
        If no '#' header is present, the raw data is returned as-is.
        """
        if not data:
            return data
        # Find '#' — it should be at the very beginning (allow a few bytes for stray whitespace)
        idx = data.find(b'#')
        if idx == -1 or idx > 5:
            return data   # no IEEE header at start — return raw
        try:
            n_digits = int(chr(data[idx + 1]))
            byte_count = int(data[idx + 2: idx + 2 + n_digits])
            payload_start = idx + 2 + n_digits
            return data[payload_start: payload_start + byte_count]
        except Exception:
            return data   # can't parse header — return everything



            

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
