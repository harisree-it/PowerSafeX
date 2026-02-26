
import json
import os
from instruments.drivers import ChromaPowerSupply, ChromaElectronicLoad, TektronixScope, Instrument

CONFIG_FILE = "instruments.json"

class InstrumentManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InstrumentManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.instruments = []
        self.simulation_mode = False
        self.logger = None
        self.error_handler = None
        self.force_comm_error_debug = False # For testing popups
        self.load_config()
        
        # Helper map for driver classes
        self.driver_map = {
            "ChromaPowerSupply": ChromaPowerSupply,
            "ChromaElectronicLoad": ChromaElectronicLoad,
            "TektronixScope": TektronixScope,
            "Instrument": Instrument
        }
        
        # Store persistent driver instances
        self._driver_instances = {}
        
        self.initialized = True

    def set_logger(self, logger_func):
        """Set a callback function for logging (e.g., self.log_message.emit)"""
        self.logger = logger_func
        # Update existing instances
        for driver in self._driver_instances.values():
            if hasattr(driver, 'logger'):
                driver.logger = logger_func

    def set_error_handler(self, handler_func):
        """Set a callback for communication errors (e.g., self.handle_comm_error)"""
        self.error_handler = handler_func
        # Update existing instances
        for driver in self._driver_instances.values():
            if hasattr(driver, 'on_error'):
                driver.on_error = handler_func
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.instruments = data.get("instruments", [])
                        self.simulation_mode = data.get("simulation_mode", False)
                    else:
                        self.instruments = data
            except Exception as e:
                print(f"Failed to load config: {e}")
                self.set_defaults()
        else:
            self.set_defaults()
            
    def set_defaults(self):
        self.instruments = [
            {
                "name": "Primary Source",
                "type": "Source",
                "driver": "ChromaPowerSupply",
                "address": "GPIB0::1::INSTR",
                "limits": {"V": 80.0, "I": 60.0, "P": 1200.0}
            },
            {
                "name": "Primary Load",
                "type": "Load",
                "driver": "ChromaElectronicLoad",
                "address": "GPIB0::2::INSTR",
                "limits": {"V": 80.0, "I": 60.0, "P": 300.0}
            },
            {
                "name": "Main Scope",
                "type": "Scope",
                "driver": "TektronixScope",
                "address": "USB0::0x0699::0x03::INSTR",
                "limits": {"V": 0, "I": 0, "P": 0}
            }
        ]
        self.save_config()

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                data = {
                    "simulation_mode": self.simulation_mode,
                    "instruments": self.instruments
                }
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def get_instruments_by_role(self, role):
        """role: 'Source', 'Load', 'Scope', etc."""
        return [inst for inst in self.instruments if inst["type"] == role]
        
    def get_instrument_by_name(self, name):
        for inst in self.instruments:
            if inst["name"] == name:
                return inst
        return None

    def get_driver_instance(self, name):
        """Get or create a persistent driver instance for the named instrument."""
        # Return existing instance if already created
        if name in self._driver_instances:
            return self._driver_instances[name]
        
        config = self.get_instrument_by_name(name)
        if not config: return None
        
        driver_cls_name = config.get("driver", "Instrument")
        driver_cls = self.driver_map.get(driver_cls_name, Instrument)
        
        # Create new instance and store it
        driver = driver_cls(config["address"], simulation_mode=self.simulation_mode, 
                            logger=self.logger, on_error=self.error_handler)
        
        if self.force_comm_error_debug and hasattr(driver, 'force_comm_error'):
            driver.force_comm_error = True
            
        self._driver_instances[name] = driver
        return driver

    # Backward compatibility properties (return first found)
    @property
    def ac_source(self):
        # Try multiple type names for source
        source_types = ["Source", "AC Source", "Bidirectional DC Supply", "DC Supply", "DC Source"]
        for src_type in source_types:
            srcs = self.get_instruments_by_role(src_type)
            if srcs:
                return self.get_driver_instance(srcs[0]["name"])
        # Fallback - Use a safer default and respect simulation mode
        return ChromaPowerSupply("GPIB0::1::INSTR", simulation_mode=self.simulation_mode)
        
    @property
    def dc_load(self):
        loads = self.get_instruments_by_role("Load")
        if loads:
            return self.get_driver_instance(loads[0]["name"])
        return ChromaElectronicLoad("GPIB0::2::INSTR", simulation_mode=self.simulation_mode)

    @property
    def scope(self):
        scopes = self.get_instruments_by_role("Scope")
        if scopes:
            return self.get_driver_instance(scopes[0]["name"])
        # Fallback - Use the user's MSO44B address if possible, otherwise generic default
        # But crucially, pass simulation_mode correctly.
        return TektronixScope("USB0::0x0699::0x0527::SGVJ010571::INSTR", simulation_mode=self.simulation_mode)

    # Limits properties for backward compatibility
    @property
    def ac_source_limits(self):
        srcs = self.get_instruments_by_role("Source")
        if srcs: return srcs[0]["limits"]
        return {"V": 80, "I": 60, "P": 1200}

    @property
    def dc_load_limits(self):
        loads = self.get_instruments_by_role("Load")
        if loads: return loads[0]["limits"]
        return {"V": 80, "I": 60, "P": 300}

    def update_instrument(self, idx, data):
        if 0 <= idx < len(self.instruments):
            self.instruments[idx] = data
            self.save_config()
            
    def add_instrument(self, data):
        self.instruments.append(data)
        self.save_config()

    def remove_instrument(self, idx):
        if 0 <= idx < len(self.instruments):
            self.instruments.pop(idx)
            self.save_config()

    def connect_all(self):
        """Connect to all configured instruments."""
        success = True
        for inst in self.instruments:
            try:
                driver = self.get_driver_instance(inst["name"])
                if driver and not driver.connected:
                    driver.connect()
                    print(f"Connected to {inst['name']}")
            except Exception as e:
                print(f"Failed to connect to {inst['name']}: {e}")
                success = False
        return success
    
    def disconnect_all(self):
        """Disconnect from all instruments."""
        for name, driver in self._driver_instances.items():
            try:
                if driver.connected:
                    driver.disconnect()
                    print(f"Disconnected from {name}")
            except Exception as e:
                print(f"Error disconnecting {name}: {e}")
