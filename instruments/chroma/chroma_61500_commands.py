"""
Chroma 61500 Series AC Power Source
Remote Control SCPI Command Reference

Models covered: 61501, 61505, 61507, 61509, 61512 (same SCPI command set)

Based on Chroma 61500 Series Programming Manual.
"""


class Chroma61500Commands:
    """SCPI command set for Chroma 61500 Series AC Power Source"""

    # ==================== STANDARD IEEE 488.2 COMMANDS ====================
    CLS          = "*CLS"       # Clear status registers
    ESE          = "*ESE"       # Standard event status enable
    ESR          = "*ESR?"      # Standard event status register query
    IDN          = "*IDN?"      # Identification query
    OPC          = "*OPC"       # Operation complete
    OPC_QUERY    = "*OPC?"      # Operation complete query
    RST          = "*RST"       # Reset to factory defaults
    SRE          = "*SRE"       # Service request enable
    STB          = "*STB?"      # Status byte query
    TRG          = "*TRG"       # Trigger (same as :TRIGger:IMMediate)

    # ==================== OUTPUT COMMANDS ====================
    OUTPUT_STATE        = "OUTPut:STATe"        # ON | OFF — Enable/disable AC output
    OUTPUT_ON_DELAY     = "OUTPut:ON:DELay"     # <sec> — Delay before output turns on
    OUTPUT_OFF_DELAY    = "OUTPut:OFF:DELay"    # <sec> — Delay before output turns off
    OUTPUT_RELAY        = "OUTPut:RELay"        # ON | OFF — Control output relay

    # ==================== SOURCE VOLTAGE COMMANDS ====================
    SOURCE_VOLTAGE_LEVEL        = "SOURce:VOLTage:LEVel"           # <V rms> — Set AC output voltage (rms)
    SOURCE_VOLTAGE_LEVEL_QUERY  = "SOURce:VOLTage:LEVel?"          # Query set voltage
    SOURCE_VOLTAGE_RANGE        = "SOURce:VOLTage:RANGe"           # LOW | HIGH  (e.g. 0–155Vrms / 0–310Vrms)
    SOURCE_VOLTAGE_RANGE_QUERY  = "SOURce:VOLTage:RANGe?"          # Query range
    SOURCE_VOLTAGE_SLEW         = "SOURce:VOLTage:SLEW"            # <V/s> — Voltage slew rate
    SOURCE_VOLTAGE_SLEW_QUERY   = "SOURce:VOLTage:SLEW?"
    SOURCE_VOLTAGE_RAMP         = "SOURce:VOLTage:RAMP"            # ON | OFF — Ramped output change
    SOURCE_VOLTAGE_LIMIT_HIGH   = "SOURce:VOLTage:LIMit:HIGH"      # <V> — Voltage high limit
    SOURCE_VOLTAGE_LIMIT_LOW    = "SOURce:VOLTage:LIMit:LOW"       # <V> — Voltage low limit

    # Peak / waveform level for non-sine
    SOURCE_VOLTAGE_PEAK         = "SOURce:VOLTage:PEAKamp"         # <V peak> — for non-sine modes

    # ==================== SOURCE FREQUENCY COMMANDS ====================
    SOURCE_FREQUENCY_LEVEL       = "SOURce:FREQuency:LEVel"        # <Hz> — Set output frequency
    SOURCE_FREQUENCY_LEVEL_QUERY = "SOURce:FREQuency:LEVel?"       # Query frequency
    SOURCE_FREQUENCY_SLEW        = "SOURce:FREQuency:SLEW"         # <Hz/s> — Frequency slew rate
    SOURCE_FREQUENCY_LIMIT_HIGH  = "SOURce:FREQuency:LIMit:HIGH"   # <Hz>
    SOURCE_FREQUENCY_LIMIT_LOW   = "SOURce:FREQuency:LIMit:LOW"    # <Hz>

    # ==================== SOURCE CURRENT / PROTECTION ====================
    SOURCE_CURRENT_LIMIT         = "SOURce:CURRent:LIMit"          # <A rms> — Current limit
    SOURCE_CURRENT_LIMIT_QUERY   = "SOURce:CURRent:LIMit?"
    SOURCE_CURRENT_PEAK_LIMIT    = "SOURce:CURRent:PEAKlimit"      # <A peak> — Peak current clamp

    # ==================== SOURCE PROTECTION ====================
    SOURCE_PROTECT_CLEAR         = "SOURce:PROTect:CLEar"          # Clear latched protection
    SOURCE_PROTECT_DELAY         = "SOURce:PROTect:DELay"          # <ms> — OCP delay
    SOURCE_OCP                   = "SOURce:CURRent:PROTect:LEVel"  # <A> — OCP threshold
    SOURCE_OVP                   = "SOURce:VOLTage:PROTect:LEVel"  # <V> — OVP threshold

    # ==================== SOURCE PHASE COMMANDS ====================
    SOURCE_PHASE_ANGLE           = "SOURce:PHASe:ANGLe"            # <deg> — Output phase angle
    SOURCE_PHASE_START           = "SOURce:PHASe:STARt"            # <deg> — Phase at output-on
    SOURCE_PHASE_STOP            = "SOURce:PHASe:STOP"             # <deg> — Phase at output-off

    # ==================== SOURCE WAVEFORM COMMANDS ====================
    SOURCE_WAVEFORM_SHAPE        = "SOURce:WAVeform:SHAPe"         # SINE | SQUare | USER<n>
    SOURCE_WAVEFORM_SHAPE_QUERY  = "SOURce:WAVeform:SHAPe?"
    SOURCE_WAVEFORM_USER         = "SOURce:WAVeform:USER"          # <n> 1-50 — Select user waveform slot
    SOURCE_WAVEFORM_DATA         = "TRACe"                         # TRACE US(X) n1,n2,... — Upload waveform

    # ==================== MEASUREMENT COMMANDS ====================
    MEASURE_VOLTAGE_RMS          = "MEASure:VOLTage:RMS?"          # V rms actual output
    MEASURE_VOLTAGE_PEAK         = "MEASure:VOLTage:PEAK?"         # V peak
    MEASURE_CURRENT_RMS          = "MEASure:CURRent:RMS?"          # A rms
    MEASURE_CURRENT_PEAK         = "MEASure:CURRent:PEAK?"         # A peak
    MEASURE_POWER_REAL           = "MEASure:POWer:REAL?"           # W  (active power)
    MEASURE_POWER_APPARENT       = "MEASure:POWer:APParent?"       # VA (apparent power)
    MEASURE_POWER_REACTIVE       = "MEASure:POWer:REACtive?"       # VAR (reactive power)
    MEASURE_POWER_FACTOR         = "MEASure:POWer:PFACtor?"        # Power factor (0–1)
    MEASURE_FREQUENCY            = "MEASure:FREQuency?"            # Hz  actual output freq
    MEASURE_CREST_FACTOR         = "MEASure:CURRent:CREStfactor?"  # Crest factor

    # ==================== LIST / SEQUENCE COMMANDS ====================
    # PLD (Power Line Disturbance) / LIST mode
    LIST_COUNT                   = "LIST:COUNt"                    # <n> — Repeat count (0=inf)
    LIST_DWELL                   = "LIST:DWELl"                    # <index>, <sec>
    LIST_FREQUENCY               = "LIST:FREQuency"               # <index>, <Hz>
    LIST_VOLTAGE                 = "LIST:VOLTage"                  # <index>, <V>
    LIST_POINTS                  = "LIST:POINts?"                  # Query number of list points
    LIST_STEP_AUTO               = "LIST:STEP"                     # AUTO | ONCE
    LIST_TRIGGER_SOURCE          = "LIST:TRIGger:SOURce"           # IMMediate | BUS | EXTernal

    # ==================== TRIGGER COMMANDS ====================
    TRIGGER_SOURCE               = "TRIGger:SOURce"               # IMMediate | BUS | EXTernal
    TRIGGER_IMMEDIATE            = "TRIGger:IMMediate"             # Force trigger
    TRIGGER_DELAY                = "TRIGger:DELay"                 # <sec>

    # ==================== INITIATE COMMANDS ====================
    INITIATE_IMMEDIATE           = "INITiate:IMMediate"            # Arm trigger system
    INITIATE_CONTINUOUS          = "INITiate:CONTinuous"           # ON | OFF

    # ==================== STATUS / SYSTEM COMMANDS ====================
    SYSTEM_ERROR                 = "SYSTem:ERRor?"                 # Query error queue
    SYSTEM_VERSION               = "SYSTem:VERSion?"               # SCPI version
    SYSTEM_LOCAL                 = "SYSTem:LOCal"                  # Return to local
    SYSTEM_REMOTE                = "SYSTem:REMote"                 # Force remote
    STATUS_OPERATION             = "STATus:OPERation:CONDition?"   # Operation status register
    STATUS_QUESTIONABLE          = "STATus:QUEStionable:CONDition?" # Questionable register

    # ==================== SENSE COMMANDS ====================
    SENSE_CURRENT_RANGE          = "SENSe:CURRent:RANGe"          # AUTO | <value>

    @staticmethod
    def format_command(cmd, *args):
        """Format a command with optional arguments.
        e.g. format_command(SOURCE_VOLTAGE_LEVEL, 120) -> 'SOURce:VOLTage:LEVel 120'
        """
        if args:
            return cmd + " " + " ".join(str(a) for a in args)
        return cmd
