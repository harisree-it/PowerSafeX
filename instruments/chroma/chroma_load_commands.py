"""
Chroma Electronic Load Command Library
Placeholder for Chroma 6280 and other electronic load models
"""

class ChromaElectronicLoadCommands:
    """Base command set for Chroma Electronic Loads"""
    
    # Common SCPI Commands
    IDN = "*IDN?"
    RST = "*RST"
    CLS = "*CLS"
    
    # Load Mode Commands (to be expanded based on specific model)
    LOAD_ON = "LOAD ON"
    LOAD_OFF = "LOAD OFF"
    
    # Mode Selection
    MODE_CC = "MODE CC"      # Constant Current
    MODE_CV = "MODE CV"      # Constant Voltage
    MODE_CP = "MODE CP"      # Constant Power
    MODE_CR = "MODE CR"      # Constant Resistance
    
    # Current Settings
    CURR_SET = "CURR"        # Set current
    CURR_MEAS = "MEAS:CURR?" # Measure current
    
    # Voltage Settings
    VOLT_SET = "VOLT"        # Set voltage
    VOLT_MEAS = "MEAS:VOLT?" # Measure voltage
    
    # Power Settings
    POW_SET = "POW"          # Set power
    POW_MEAS = "MEAS:POW?"   # Measure power
    
    # Resistance Settings
    RES_SET = "RES"          # Set resistance
    
    @staticmethod
    def format_command(command, value=None):
        """Format command with optional value"""
        if value is not None:
            return f"{command} {value}"
        return command
