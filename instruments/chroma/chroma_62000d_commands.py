"""
Chroma 62000D Series DC Bidirectional Power Supply
Remote Control Commands

This module contains all SCPI commands for the Chroma 62000D series.
Based on the user manual remote command reference.
"""

class Chroma62000DCommands:
    """SCPI command set for Chroma 62000D DC Bidirectional Power Supply"""
    
    # ==================== GENERAL COMMANDS ====================
    
    # Standard SCPI Commands
    CLS = "*CLS"                    # Clear status command
    ESE = "*ESE"                    # Standard event status enable
    ESR = "*ESR?"                   # Standard event status register
    IDN = "*IDN?"                   # Identification query
    OPC = "*OPC"                    # Operation complete command
    OPC_QUERY = "*OPC?"             # Operation complete query
    RCL = "*RCL"                    # Recall instrument state command
    RST = "*RST"                    # Reset command
    SAV = "*SAV"                    # Save command
    SRE = "*SRE"                    # Service request enable command/query
    STB = "*STB?"                   # Read status byte query
    
    # Abort and Configuration
    ABORT = "ABORt"                 # Sets all output state to "OFF"
    
    # ==================== SYSTEM COMMANDS ====================
    
    SYSTEM_ERROR = "SYSTem:ERRor?"                      # Returns error message and code
    SYSTEM_MODE = "SYSTem:MODE"                         # Sets Source/Load output mode
    SYSTEM_VERSION_INTERNAL = "SYSTem:VERSion:INTernal?" # Queries Host version
    SYSTEM_VERSION_MODULE = "SYSTem:VERSion:MODule:VERSion?" # Queries Module version
    SYSTEM_DATE = "SYSTem:DATE"                         # Sets system date
    SYSTEM_TIME = "SYSTem:TIME"                         # Sets system time
    
    # Communication Settings
    SYSTEM_COMMUNICATE_CAN_CYCLIC_TIME = "SYSTem:COMMunicate:CAN:CYClic:TIME"
    SYSTEM_COMMUNICATE_CAN_CYCLIC_ID = "SYSTem:COMMunicate:CAN:CYClic:ID"
    SYSTEM_COMMUNICATE_CAN_BAUD = "SYSTem:COMMunicate:CAN:BAUD"
    SYSTEM_COMMUNICATE_CAN_ID = "SYSTem:COMMunicate:CAN:ID"
    SYSTEM_COMMUNICATE_CAN_MASK = "SYSTem:COMMunicate:CAN:MASK"
    SYSTEM_COMMUNICATE_CAN_MODE = "SYSTem:COMMunicate:CAN:MODE"
    SYSTEM_COMMUNICATE_CAN_PADDING = "SYSTem:COMMunicate:CAN:PADding"
    SYSTEM_COMMUNICATE_CAN_SCPI_ID = "SYSTem:COMMunicate:CAN:SCPI:ID"
    SYSTEM_COMMUNICATE_CAN_APPLY = "SYSTem:COMMunicate:CAN:APPly"
    SYSTEM_COMMUNICATE_GPIB_ADDRESS = "SYSTem:COMMunicate:GPIB:ADDress"
    SYSTEM_COMMUNICATE_SOCK_DHCP = "SYSTem:COMMunicate:SOCK:DHCP"
    SYSTEM_COMMUNICATE_SOCK_GATEWAY = "SYSTem:COMMunicate:SOCK:GATeway"
    SYSTEM_COMMUNICATE_SOCK_IP = "SYSTem:COMMunicate:SOCK:IP"
    SYSTEM_COMMUNICATE_SOCK_MASK = "SYSTem:COMMunicate:SOCK:MASK"
    SYSTEM_COMMUNICATE_SOCK_APPLY = "SYSTem:COMMunicate:SOCK:APPLY"
    
    # Instrument Status
    INSTRUMENT_STATUS_AD = "INSTrument:STATus:AD?"      # Returns AD module status
    INSTRUMENT_STATUS_DD = "INSTrument:STATus:DD?"      # Returns DD module status
    
    # ==================== MEASUREMENT COMMANDS ====================
    
    FETCH_CURRENT = "FETCh:CURRent?"        # Measures output current (with sign)
    FETCH_POWER = "FETCh:POWer?"            # Measures output power (with sign)
    FETCH_STATUS = "FETCh:STATus?"          # Returns status code
    
    MEASURE_VOLTAGE = "MEASure:VOLTage?"    # Returns voltage at output
    MEASURE_CURRENT = "MEASure:CURRent?"    # Returns current at output (with sign)
    MEASURE_POWER = "MEASure:POWer?"        # Returns power at output (with sign)
    
    # ==================== PROGRAM COMMANDS ====================
    
    PROGRAM_MODE = "PROGram:MODE"                       # Sets program output mode
    PROGRAM_RUN = "PROGram:RUN"                         # Executes the program
    PROGRAM_SAVE = "PROGram:SAVE"                       # Saves the program
    PROGRAM_SELECTED = "PROGram:SELected"               # Sets executed program no. in List
    PROGRAM_LINK = "PROGram:LINK"                       # Links program to another
    PROGRAM_COUNT = "PROGram:COUNT"                     # Sets no. of times for program
    PROGRAM_PULL = "PROGram:PULL"                       # Executes PROGRAM TRIGGER
    
    # Program Sequence Commands
    PROGRAM_SEQUENCE_SELECTED = "PROGram:SEQuence:SELected"
    PROGRAM_SEQUENCE_TYPE = "PROGram:SEQuence:TYPE"
    PROGRAM_SEQUENCE_VOLTAGE = "PROGram:SEQuence:VOLTage"
    PROGRAM_SEQUENCE_VOLTAGE_SLEW = "PROGram:SEQuence:VOLTage:SLEW"
    PROGRAM_SEQUENCE_CURRENT = "PROGram:SEQuence:CURRent"
    PROGRAM_SEQUENCE_CURRENT_SLEW = "PROGram:SEQuence:CURRent:SLEW"
    PROGRAM_SEQUENCE_CURRENT_LOAD = "PROGram:SEQuence:CURRent:LOAD"
    PROGRAM_SEQUENCE_TIME = "PROGram:SEQuence:TIME"
    
    PROGRAM_CLEAR = "PROGram:CLEAR"                     # Clears all sequences
    PROGRAM_ADD = "PROGram:ADD"                         # Adds sequences to program
    PROGRAM_MAX = "PROGram:MAX?"                        # Queries sequence amount
    PROGRAM_SEQUENCE = "PROGram:SEQuence"               # Sets parameters of sequence
    
    # Program Step Commands
    PROGRAM_STEP_START_V = "PROGram:STEP:STARTV"        # Sets Step Mode start voltage
    PROGRAM_STEP_END_V = "PROGram:STEP:ENDV"            # Sets Step Mode end voltage
    PROGRAM_STEP_TIME = "PROGram:STEP:TIME"             # Sets execution time for Step Mode
    
    # ==================== CONFIGURATION COMMANDS ====================
    
    CONFIGURE_APG_VMEAS = "CONFigure:APGVMeas"          # Sets action type of APG VMEAS
    CONFIGURE_APG_ISET = "CONFigure:APGISet"            # Sets action type of APG SOURCE/LOAD ISET
    CONFIGURE_APG_IMEAS = "CONFigure:APGIMeas"          # Sets action type of APG IMEAS
    CONFIGURE_AVG_TIMES = "CONFigure:AVG:TIMES"         # Sets average times for measuring V/I
    CONFIGURE_AVG_METHOD = "CONFigure:AVG:METHod"       # Sets average method for measuring V/I
    CONFIGURE_BRIGHTNESS = "CONFigure:BRIGhtness"       # Sets display brightness
    CONFIGURE_DISPLAY_VID = "CONFigure:DISPlay:VID"     # Sets device ID Master
    CONFIGURE_MSTSLV_PARSER = "CONFigure:MSTSLV:PARSER" # Sets series or parallel mode
    CONFIGURE_MSTSLV_NUMSLY = "CONFigure:MSTSLV:NUMSLY" # Sets number of SLAVE
    CONFIGURE_MSTSLV_READY = "CONFigure:MSTSLV:READY?"  # Queries Master/Slave connection
    CONFIGURE_MSTSLV = "CONFigure:MSTSLV"               # Executes Master/Slave control
    CONFIGURE_INHIBIT = "CONFigure:INHibit"             # Executes Remote Inhibit control
    CONFIGURE_INHIBIT_PULL = "CONFigure:INHibit:PULL"   # Executes Remote Inhibit input signal
    CONFIGURE_INTERLOCK = "CONFigure:INTERLOCK"         # Executes Safety Interlock control
    CONFIGURE_INTERLOCK_PULL = "CONFigure:INTERLOCK:PULL" # Executes Safety Interlock input
    CONFIGURE_EXTON = "CONFigure:EXTON"                 # Executes External ON/OFF control
    CONFIGURE_EXTON_PULL = "CONFigure:EXTON:PULL"       # Executes External ON/OFF input
    
    CONFIGURE_BEEPER = "CONFigure:BEEPer"               # Sets beeper ON or OFF
    CONFIGURE_OUTPUT = "CONFigure:OUTPut"               # Sets voltage/current output
    CONFIGURE_FOLDBACK = "CONFigure:FOLDback"           # Sets type of FOLDBACK PROTECT
    CONFIGURE_FOLDT = "CONFigure:FOLDT"                 # Sets delay time of FOLDBACK PROTECT
    CONFIGURE_APGVSET = "CONFigure:APGVSet"             # Sets action type of APG VSET
    
    # ==================== SOURCE MODE COMMANDS ====================
    
    SOURCE_VOLTAGE = "SOURce:VOLTage"                   # Sets output voltage
    SOURCE_VOLTAGE_LIMIT_HIGH = "SOURce:VOLTage:LIMit:HIGH"  # Sets high voltage range
    SOURCE_VOLTAGE_LIMIT_LOW = "SOURce:VOLTage:LIMit:LOW"    # Sets low voltage range
    SOURCE_VOLTAGE_PROTECT_HIGH = "SOURce:VOLTage:PROTect:HIGH" # Sets voltage range for over voltage
    SOURCE_VOLTAGE_SLEW = "SOURce:VOLTage:SLEW"         # Sets rising/falling slew rate (V/ms)
    
    SOURCE_CURRENT = "SOURce:CURRent"                   # Sets output current (ampere)
    SOURCE_CURRENT_LIMIT_HIGH = "SOURce:CURRent:LIMit:HIGH"  # Sets output current range
    SOURCE_CURRENT_LIMIT_LOW = "SOURce:CURRent:LIMit:LOW"    # Sets output current range
    SOURCE_CURRENT_PROTECT_HIGH = "SOURce:CURRent:PROTect:HIGH" # Sets current range for OCP
    SOURCE_CURRENT_SLEW = "SOURce:CURRent:SLEW"         # Sets rising/falling slew rate (A/ms)
    
    SOURCE_POWER = "SOURce:POWer"                       # Sets output power
    SOURCE_POWER_LIMIT_HIGH = "SOURce:POWer:LIMit:HIGH" # Sets output power range
    SOURCE_POWER_LIMIT_LOW = "SOURce:POWer:LIMit:LOW"   # Sets output power range
    SOURCE_POWER_PROTECT_HIGH = "SOURce:POWer:PROTect:HIGH" # Sets power range for OPP
    
    SOURCE_FREQUENCY = "SOURce:FREQuency"               # Sets output frequency
    SOURCE_FREQUENCY_LIMIT_HIGH = "SOURce:FREQuency:LIMit:HIGH" # Sets frequency limit high
    SOURCE_FREQUENCY_LIMIT_LOW = "SOURce:FREQuency:LIMit:LOW"   # Sets frequency limit low
    
    SOURCE_DCON_RISE = "SOURce:DCON:RISE"               # Sets DC_ON signal active point (RISE)
    SOURCE_DCON_FALL = "SOURce:DCON:FALL"               # Sets DC_ON signal active point (FALL)
    
    # ==================== LOAD MODE COMMANDS ====================
    
    LOAD_CURRENT = "LOAD:CURRent"                       # Sets Load output current
    LOAD_CURRENT_PROTECT_HIGH = "LOAD:CURRent:PROTect:HIGH" # Sets current range for Load OCP
    LOAD_POWER = "LOAD:POWer"                           # Sets Load power output
    LOAD_POWER_PROTECT_HIGH = "LOAD:POWer:PROTect:HIGH" # Sets power range for Load OPP
    
    # ==================== FETCH VOLTAGE (Additional) ====================
    
    FETCH_VOLTAGE = "FETCh:VOLTage?"                    # Measures output voltage
    
    @staticmethod
    def format_command(command, value=None):
        """
        Format a command with optional value
        
        Args:
            command: SCPI command string
            value: Optional value to append
            
        Returns:
            Formatted command string
        """
        if value is not None:
            return f"{command} {value}"
        return command
