// custom_blocks.js
// Contains definitions and Python generators for custom blocks
// Organized by Instrument Type
// Version: 20260806 — Full SCPI Block Set (Source + Load + Scope)

console.log("Loading custom_blocks.js (v20260806)...");

// Ensure pythonGenerator is available. It is defined in editor.html
var pythonGenerator = window.pythonGenerator || Blockly.Python;

if (!pythonGenerator) {
    console.error("CRITICAL: Blockly.Python is not loaded!");
} else {
    pythonGenerator.forBlock = pythonGenerator.forBlock || {};
}

console.log("Using pythonGenerator instance:", !!pythonGenerator);


// =============================================================================
// SOURCE BLOCKS  (maps to mgr.ac_source — ChromaPowerSupply)
// SCPI Reference: SOURce / MEASure subsystems
// =============================================================================

// --- Set Voltage ---
Blockly.Blocks['inst_set_voltage'] = {
    init: function () {
        this.appendValueInput("VOLTAGE")
            .setCheck("Number")
            .appendField("Set Source Voltage to");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:VOLTage <value>  — Sets the AC/DC source output voltage.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_set_voltage'] = function (block, generator) {
    var v = generator.valueToCode(block, 'VOLTAGE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage(' + v + ')\n';
};

// --- Set Current Limit ---
Blockly.Blocks['inst_set_current_limit'] = {
    init: function () {
        this.appendValueInput("CURRENT")
            .setCheck("Number")
            .appendField("Set Source Current Limit to");
        this.appendDummyInput()
            .appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:CURRent <value>  — Sets the source current limit.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_set_current_limit'] = function (block, generator) {
    var v = generator.valueToCode(block, 'CURRENT', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_current_limit(' + v + ')\n';
};

// --- Set Frequency ---
Blockly.Blocks['inst_set_frequency'] = {
    init: function () {
        this.appendValueInput("FREQUENCY")
            .setCheck("Number")
            .appendField("Set Source Frequency to");
        this.appendDummyInput()
            .appendField("Hz");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:FREQuency <value>  — Sets the AC source output frequency.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_set_frequency'] = function (block, generator) {
    var v = generator.valueToCode(block, 'FREQUENCY', generator.ORDER_ATOMIC) || '50';
    return 'mgr.ac_source.set_frequency(' + v + ')\n';
};

// --- Set Power Limit ---
Blockly.Blocks['inst_set_power_limit'] = {
    init: function () {
        this.appendValueInput("POWER")
            .setCheck("Number")
            .appendField("Set Source Power Limit to");
        this.appendDummyInput()
            .appendField("W");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:POWer <value>  — Sets the source power limit.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_set_power_limit'] = function (block, generator) {
    var v = generator.valueToCode(block, 'POWER', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_power_limit(' + v + ')\n';
};

// --- Set Voltage Slew Rate ---
Blockly.Blocks['inst_source_slew_rate'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Source Voltage Slew Rate to");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:VOLTage:SLEW <value>  — Sets voltage slew rate.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_slew_rate'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage_slew_rate(' + v + ')\n';
};

// --- Set Current Slew Rate ---
Blockly.Blocks['inst_source_current_slew'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Source Current Slew Rate to");
        this.appendDummyInput()
            .appendField("A/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:CURRent:SLEW <value>  — Sets current slew rate.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_current_slew'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_current_slew_rate(' + v + ')\n';
};

// --- Voltage Rise Rate ---
Blockly.Blocks['inst_source_voltage_rise'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Source Voltage Rise Rate to");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:VOLTage:RISE <value>  — Sets the voltage rise ramp rate.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_voltage_rise'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage_rise(' + v + ')\n';
};

// --- Voltage Fall Rate ---
Blockly.Blocks['inst_source_voltage_fall'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Source Voltage Fall Rate to");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:VOLTage:FALL <value>  — Sets the voltage fall ramp rate.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_voltage_fall'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage_fall(' + v + ')\n';
};

// --- Set OVP ---
Blockly.Blocks['inst_source_set_ovp'] = {
    init: function () {
        this.appendValueInput("OVP")
            .setCheck("Number")
            .appendField("Set Source OVP to");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:VOLTage:PROTect:HIGH <value>  — Sets over-voltage protection threshold.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_set_ovp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_ovp(' + v + ')\n';
};

// --- Set OCP ---
Blockly.Blocks['inst_source_set_ocp'] = {
    init: function () {
        this.appendValueInput("OCP")
            .setCheck("Number")
            .appendField("Set Source OCP to");
        this.appendDummyInput()
            .appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:CURRent:PROTect:HIGH <value>  — Sets over-current protection threshold.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_set_ocp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_ocp(' + v + ')\n';
};

// --- Grouped Protections Block ---
Blockly.Blocks['inst_source_protections'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Source Protections");
        this.appendValueInput("OVP")
            .setCheck("Number")
            .appendField("OVP (V)");
        this.appendValueInput("OCP")
            .setCheck("Number")
            .appendField("OCP (A)");
        this.appendValueInput("OPP")
            .setCheck("Number")
            .appendField("OPP (W)");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("Sets OVP, OCP, and OPP in one block. Leave inputs disconnected to skip.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_protections'] = function (block, generator) {
    var ovp = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC);
    var ocp = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC);
    var opp = generator.valueToCode(block, 'OPP', generator.ORDER_ATOMIC);
    var code = "";
    if (ovp) code += 'mgr.ac_source.set_ovp(' + ovp + ')\n';
    if (ocp) code += 'mgr.ac_source.set_ocp(' + ocp + ')\n';
    if (opp) code += 'log_callback("OPP not directly supported on source; set power limit instead.")\n';
    return code;
};

// --- Output ON ---
Blockly.Blocks['inst_output_on'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Source Output ON");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: OUTPut ON  — Enables the source output.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_output_on'] = function (block, generator) {
    return 'mgr.ac_source.output_on()\n';
};

// --- Output OFF ---
Blockly.Blocks['inst_output_off'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Source Output OFF");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: OUTPut OFF  — Disables the source output.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_output_off'] = function (block, generator) {
    return 'mgr.ac_source.output_off()\n';
};

// --- Source Reset ---
Blockly.Blocks['inst_source_reset'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Reset Source Instrument");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: *RST  — Resets the source to factory defaults.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_reset'] = function (block, generator) {
    return 'mgr.ac_source.reset()\n';
};

// --- Clear Protection ---
Blockly.Blocks['inst_source_clear_protection'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Clear Source Protection");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("SCPI: SOURce:PROTect:CLEar  — Clears latched protection faults.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_clear_protection'] = function (block, generator) {
    return 'mgr.ac_source.clear_protection()\n';
};

// --- Measure Source Voltage ---
Blockly.Blocks['inst_source_measure_voltage'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Voltage");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:VOLTage?  — Returns measured source output voltage in V.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_voltage'] = function (block, generator) {
    return ['mgr.ac_source.measure_voltage()', generator.ORDER_NONE];
};

// --- Measure Source Current ---
Blockly.Blocks['inst_source_measure_current'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Current");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:CURRent?  — Returns measured source output current in A.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_current'] = function (block, generator) {
    return ['mgr.ac_source.measure_current()', generator.ORDER_NONE];
};

// --- Measure Source Power ---
Blockly.Blocks['inst_source_measure_power'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Power");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:POWer?  — Returns measured source output power in W.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_power'] = function (block, generator) {
    return ['mgr.ac_source.measure_power()', generator.ORDER_NONE];
};

// --- Measure Source Frequency ---
Blockly.Blocks['inst_source_measure_freq'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Frequency");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:FREQuency?  — Returns measured source output frequency in Hz.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_freq'] = function (block, generator) {
    return ['mgr.ac_source.measure_frequency()', generator.ORDER_NONE];
};

// --- Measure Apparent Power ---
Blockly.Blocks['inst_source_measure_apparent'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Apparent Power");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:POWer:APParent?  — Returns apparent power (VA).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_apparent'] = function (block, generator) {
    return ['mgr.ac_source.measure_apparent_power()', generator.ORDER_NONE];
};

// --- Measure Power Factor ---
Blockly.Blocks['inst_source_measure_pf'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Power Factor");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("SCPI: MEASure:POWer:PF?  — Returns power factor (0.0–1.0).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_source_measure_pf'] = function (block, generator) {
    return ['mgr.ac_source.measure_pf()', generator.ORDER_NONE];
};


// =============================================================================
// LOAD BLOCKS  (maps to mgr.dc_load — ChromaElectronicLoad)
// SCPI Reference: Chroma 63200A / 6310A electronic load commands
// =============================================================================

// --- Set Load Mode ---
Blockly.Blocks['inst_load_mode'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Load Mode to")
            .appendField(new Blockly.FieldDropdown([
                ["CC — Constant Current", "CC"],
                ["CV — Constant Voltage", "CV"],
                ["CR — Constant Resistance", "CR"],
                ["CP — Constant Power", "CP"]
            ]), "MODE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CONF:MODE <mode>  — Sets the electronic load operating mode.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_mode'] = function (block, generator) {
    var mode = block.getFieldValue('MODE');
    return 'mgr.dc_load.set_mode("' + mode + '")\n';
};

// --- Set Load Current (CC mode) ---
Blockly.Blocks['inst_load_set_current'] = {
    init: function () {
        this.appendValueInput("CURRENT")
            .setCheck("Number")
            .appendField("Set Load Current to");
        this.appendDummyInput()
            .appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CURR:STAT:L1 <value>  — Sets the CC mode current setpoint.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_current'] = function (block, generator) {
    var v = generator.valueToCode(block, 'CURRENT', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_current(' + v + ')\n';
};

// --- Set Load Voltage (CV mode) ---
Blockly.Blocks['inst_load_set_voltage'] = {
    init: function () {
        this.appendValueInput("VOLTAGE")
            .setCheck("Number")
            .appendField("Set Load Voltage to");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: VOLT:STAT:L1 <value>  — Sets the CV mode voltage setpoint.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_voltage'] = function (block, generator) {
    var v = generator.valueToCode(block, 'VOLTAGE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_voltage(' + v + ')\n';
};

// --- Set Load Power (CP mode) ---
Blockly.Blocks['inst_load_set_power'] = {
    init: function () {
        this.appendValueInput("POWER")
            .setCheck("Number")
            .appendField("Set Load Power to");
        this.appendDummyInput()
            .appendField("W");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: POW:STAT:L1 <value>  — Sets the CP mode power setpoint.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_power'] = function (block, generator) {
    var v = generator.valueToCode(block, 'POWER', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_power(' + v + ')\n';
};

// --- Set Load Resistance (CR mode) ---
Blockly.Blocks['inst_load_set_resistance'] = {
    init: function () {
        this.appendValueInput("RESISTANCE")
            .setCheck("Number")
            .appendField("Set Load Resistance to");
        this.appendDummyInput()
            .appendField("Ω");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: RES:STAT:L1 <value>  — Sets the CR mode resistance setpoint.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_resistance'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RESISTANCE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_resistance(' + v + ')\n';
};

// --- Load ON ---
Blockly.Blocks['inst_load_output_on'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Load ON");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: LOAD ON  — Enables the electronic load input.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_output_on'] = function (block, generator) {
    return 'mgr.dc_load.load_on()\n';
};

// --- Load OFF ---
Blockly.Blocks['inst_load_output_off'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Load OFF");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: LOAD OFF  — Disables the electronic load input.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_output_off'] = function (block, generator) {
    return 'mgr.dc_load.load_off()\n';
};

// --- Load Slew Rate ---
Blockly.Blocks['inst_load_slew_rate'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Load Slew Rate to");
        this.appendDummyInput()
            .appendField("A/μs");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CURR:STAT:RISE / CURR:DYN:RISE <value>  — Sets static and dynamic current slew rate.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_slew_rate'] = function (block, generator) {
    var v = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_slew_rate(' + v + ')\n';
};

// --- Dynamic Mode ---
Blockly.Blocks['inst_load_dynamic'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Load Dynamic Mode")
            .appendField(new Blockly.FieldDropdown([["ON", "ON"], ["OFF", "OFF"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CONF:MODE CCD|CRD  — Enables/disables dynamic (transient) load mode.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_dynamic'] = function (block, generator) {
    var state = block.getFieldValue('STATE');
    var bool_state = (state === "ON") ? "True" : "False";
    return 'mgr.dc_load.set_dynamic_mode(' + bool_state + ')\n';
};

// --- Load OCP ---
Blockly.Blocks['inst_load_set_ocp'] = {
    init: function () {
        this.appendValueInput("OCP")
            .setCheck("Number")
            .appendField("Set Load OCP to");
        this.appendDummyInput()
            .appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CONF:CURR:PROT <value>  — Sets over-current protection on the load.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_ocp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_ocp(' + v + ')\n';
};

// --- Load OVP ---
Blockly.Blocks['inst_load_set_ovp'] = {
    init: function () {
        this.appendValueInput("OVP")
            .setCheck("Number")
            .appendField("Set Load OVP to");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CONF:VOLT:PROT <value>  — Sets over-voltage protection on the load.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_ovp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_ovp(' + v + ')\n';
};

// --- Load OPP ---
Blockly.Blocks['inst_load_set_opp'] = {
    init: function () {
        this.appendValueInput("OPP")
            .setCheck("Number")
            .appendField("Set Load OPP to");
        this.appendDummyInput()
            .appendField("W");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: CONF:POW:PROT <value>  — Sets over-power protection on the load.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_set_opp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OPP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.dc_load.set_opp(' + v + ')\n';
};

// --- Load Grouped Protections ---
Blockly.Blocks['inst_load_protections'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Load Protections");
        this.appendValueInput("OVP")
            .setCheck("Number")
            .appendField("OVP (V)");
        this.appendValueInput("OCP")
            .setCheck("Number")
            .appendField("OCP (A)");
        this.appendValueInput("OPP")
            .setCheck("Number")
            .appendField("OPP (W)");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("Sets OVP, OCP, and OPP on the load. Leave inputs disconnected to skip.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_protections'] = function (block, generator) {
    var ovp = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC);
    var ocp = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC);
    var opp = generator.valueToCode(block, 'OPP', generator.ORDER_ATOMIC);
    var code = "";
    if (ovp) code += 'mgr.dc_load.set_ovp(' + ovp + ')\n';
    if (ocp) code += 'mgr.dc_load.set_ocp(' + ocp + ')\n';
    if (opp) code += 'mgr.dc_load.set_opp(' + opp + ')\n';
    return code;
};

// --- Clear Load Protection ---
Blockly.Blocks['inst_load_clear_protection'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Clear Load Protection");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("SCPI: PROT:CLE  — Clears latched protection faults on the load.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_clear_protection'] = function (block, generator) {
    return 'mgr.dc_load.clear_protection()\n';
};

// --- Measure Load Voltage ---
Blockly.Blocks['inst_load_measure_voltage'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Voltage");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("SCPI: MEAS:VOLT?  — Returns measured voltage at load terminals in V.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_measure_voltage'] = function (block, generator) {
    return ['mgr.dc_load.measure_voltage()', generator.ORDER_NONE];
};

// --- Measure Load Current ---
Blockly.Blocks['inst_load_measure_current'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Current");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("SCPI: MEAS:CURR?  — Returns measured current drawn by load in A.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_measure_current'] = function (block, generator) {
    return ['mgr.dc_load.measure_current()', generator.ORDER_NONE];
};

// --- Measure Load Resistance ---
Blockly.Blocks['inst_load_measure_resistance'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Resistance");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("SCPI: MEAS:RES?  — Returns measured resistance at load terminals in Ω.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_load_measure_resistance'] = function (block, generator) {
    return ['mgr.dc_load.measure_resistance()', generator.ORDER_NONE];
};


// =============================================================================
// SCOPE BLOCKS  (maps to mgr.scope — TektronixScope MSO44B)
// SCPI Reference: Tektronix MSO/DPO series SCPI command set
// =============================================================================

// --- Autoscale (Autoset) ---
Blockly.Blocks['inst_scope_autoscale'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Scope Autoset");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: AUTOSet EXECute  — Performs automatic scale/trigger adjustment.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_autoscale'] = function (block, generator) {
    return 'mgr.scope.auto_set()\n';
};

// --- Acquisition Control ---
Blockly.Blocks['inst_scope_run_stop'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Scope Acquisition")
            .appendField(new Blockly.FieldDropdown([
                ["RUN — Continuous", "RUN"],
                ["STOP — Freeze", "STOP"],
                ["SINGLE — One Shot", "SINGLE"]
            ]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: ACQ:STATE RUN|STOP / ACQ:STOPA SEQ  — Controls acquisition state.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_run_stop'] = function (block, generator) {
    var state = block.getFieldValue('STATE');
    if (state === "RUN")    return 'mgr.scope.run()\n';
    if (state === "STOP")   return 'mgr.scope.stop()\n';
    if (state === "SINGLE") return 'mgr.scope.single()\n';
    return '';
};

// --- Set Timebase (Horizontal Scale) ---
Blockly.Blocks['inst_scope_timebase'] = {
    init: function () {
        this.appendValueInput("SCALE")
            .setCheck("Number")
            .appendField("Set Scope Timebase to");
        this.appendDummyInput()
            .appendField("ms/div");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: HOR:SCALE <value>  — Sets horizontal time/div (value in ms, converted to s).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_timebase'] = function (block, generator) {
    var v = generator.valueToCode(block, 'SCALE', generator.ORDER_ATOMIC) || '10';
    // Convert ms to seconds for the driver
    return 'mgr.scope.set_time_scale((' + v + ') / 1000.0)\n';
};

// --- Set Horizontal Delay ---
Blockly.Blocks['inst_scope_delay'] = {
    init: function () {
        this.appendValueInput("DELAY")
            .setCheck("Number")
            .appendField("Set Scope Horizontal Delay to");
        this.appendDummyInput()
            .appendField("s");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: HOR:DELAY:TIME <value>  — Sets horizontal position/delay.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_delay'] = function (block, generator) {
    var v = generator.valueToCode(block, 'DELAY', generator.ORDER_ATOMIC) || '0';
    return 'mgr.scope.set_delay(' + v + ')\n';
};

// --- Enable / Disable Channel ---
Blockly.Blocks['inst_scope_channel_enable'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Scope Channel")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL")
            .appendField(new Blockly.FieldDropdown([["ON","ON"],["OFF","OFF"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: SELect:CH<n> ON|OFF  — Enables or disables a scope channel display.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_channel_enable'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var state = block.getFieldValue('STATE');
    var bool_state = (state === "ON") ? "True" : "False";
    return 'mgr.scope.enable_channel(' + ch + ', ' + bool_state + ')\n';
};

// --- Set Vertical Scale ---
Blockly.Blocks['inst_scope_vertical'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL")
            .appendField("Vertical Scale to");
        this.appendValueInput("SCALE")
            .setCheck("Number");
        this.appendDummyInput()
            .appendField("V/div");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: CH<n>:SCALE <value>  — Sets vertical V/div for a channel.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_vertical'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var v = generator.valueToCode(block, 'SCALE', generator.ORDER_ATOMIC) || '1';
    return 'mgr.scope.set_vertical_scale(' + ch + ', ' + v + ')\n';
};

// --- Set Vertical Offset ---
Blockly.Blocks['inst_scope_offset'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL")
            .appendField("Offset to");
        this.appendValueInput("OFFSET")
            .setCheck("Number");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: CH<n>:OFFSET <value>  — Sets vertical offset for a channel.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_offset'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var v = generator.valueToCode(block, 'OFFSET', generator.ORDER_ATOMIC) || '0';
    return 'mgr.scope.set_vertical_offset(' + ch + ', ' + v + ')\n';
};

// --- Set Coupling ---
Blockly.Blocks['inst_scope_coupling'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL")
            .appendField("Coupling")
            .appendField(new Blockly.FieldDropdown([["DC","DC"],["AC","AC"],["GND","GND"]]), "COUP");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: CH<n>:COUP DC|AC|GND  — Sets input coupling mode.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_coupling'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var coup = block.getFieldValue('COUP');
    return 'mgr.scope.set_coupling(' + ch + ', "' + coup + '")\n';
};

// --- Set Bandwidth Limit ---
Blockly.Blocks['inst_scope_bandwidth'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL")
            .appendField("Bandwidth")
            .appendField(new Blockly.FieldDropdown([
                ["Full","FULL"],
                ["20 MHz","20E6"],
                ["250 MHz","250E6"]
            ]), "BW");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: CH<n>:BANDWIDTH FULL|20E6|250E6  — Sets channel bandwidth limit.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_bandwidth'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var bw = block.getFieldValue('BW');
    return 'mgr.scope.set_bandwidth(' + ch + ', "' + bw + '")\n';
};

// --- Set Trigger ---
Blockly.Blocks['inst_scope_trigger'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope Trigger: CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL");
        this.appendValueInput("LEVEL")
            .setCheck("Number")
            .appendField("Level (V)");
        this.appendDummyInput()
            .appendField("Slope")
            .appendField(new Blockly.FieldDropdown([["RISE","RISE"],["FALL","FALL"]]), "SLOPE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: TRIG:A:TYPE EDGE; TRIG:A:EDGE:SOUR CH<n>; TRIG:A:LEVEL <v>; TRIG:A:EDGE:SLOPE RISE|FALL");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_trigger'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var slope = block.getFieldValue('SLOPE');
    var level = generator.valueToCode(block, 'LEVEL', generator.ORDER_ATOMIC) || '0';
    return 'mgr.scope.set_trigger(' + ch + ', ' + level + ', "' + slope + '")\n';
};

// --- Configure Measurement ---
Blockly.Blocks['inst_scope_configure_meas'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Config Meas Slot")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"],["5","5"],["6","6"],["7","7"],["8","8"]]), "SLOT")
            .appendField("Type")
            .appendField(new Blockly.FieldDropdown([
                ["Pk-Pk","PK2PK"],
                ["RMS","RMS"],
                ["Frequency","FREQ"],
                ["Period","PERIOD"],
                ["Maximum","MAX"],
                ["Minimum","MIN"],
                ["Mean","MEAN"],
                ["Rise Time","RISE"],
                ["Fall Time","FALL"]
            ]), "TYPE")
            .appendField("on CH")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"]]), "CHANNEL");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: MEASU:MEAS<n>:TYPE <type>; :SOUR CH<c>; :STATE ON  — Configures a measurement slot.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_configure_meas'] = function (block, generator) {
    var slot = block.getFieldValue('SLOT');
    var type = block.getFieldValue('TYPE');
    var ch = block.getFieldValue('CHANNEL');
    return 'mgr.scope.configure_measurement(' + slot + ', "' + type + '", ' + ch + ')\n';
};

// --- Get Measurement Value ---
Blockly.Blocks['inst_scope_get_meas'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Get Measurement from Slot")
            .appendField(new Blockly.FieldDropdown([["1","1"],["2","2"],["3","3"],["4","4"],["5","5"],["6","6"],["7","7"],["8","8"]]), "SLOT");
        this.setOutput(true, "Number");
        this.setColour(200);
        this.setTooltip("SCPI: MEASU:MEAS<n>:VAL?  — Returns the current value of a configured measurement.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_get_meas'] = function (block, generator) {
    var slot = block.getFieldValue('SLOT');
    return ['mgr.scope.get_measurement(' + slot + ')', generator.ORDER_NONE];
};

// --- Save Screenshot ---
Blockly.Blocks['inst_scope_save_screenshot'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Save Scope Screenshot");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(200);
        this.setTooltip("SCPI: SAVE:IMAGe — Captures scope display screenshot and saves to report folder.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_scope_save_screenshot'] = function (block, generator) {
    var code = 'import datetime\n';
    code += 'import os\n';
    code += '_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")\n';
    code += '_fname = os.path.abspath(f"reports/captures/{_ts}_scope.png")\n';
    code += 'os.makedirs(os.path.dirname(_fname), exist_ok=True)\n';
    code += 'mgr.scope.save_screenshot(_fname)\n';
    code += 'images.append({"name": "Scope Capture", "path": _fname})\n';
    return code;
};


// =============================================================================
// SYSTEM / UTILITY BLOCKS
// =============================================================================

// --- Wait / Sleep ---
Blockly.Blocks['inst_wait'] = {
    init: function () {
        this.appendValueInput("SECONDS")
            .setCheck("Number")
            .appendField("Wait");
        this.appendDummyInput()
            .appendField("seconds");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(290);
        this.setTooltip("Python: time.sleep(<value>)  — Pauses execution for specified seconds.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_wait'] = function (block, generator) {
    var v = generator.valueToCode(block, 'SECONDS', generator.ORDER_ATOMIC) || '1';
    return 'time.sleep(' + v + ')\n';
};

// --- Get Test Parameter ---
Blockly.Blocks['inst_get_param'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Get Parameter")
            .appendField(new Blockly.FieldDropdown(function () {
                return typeof AVAILABLE_PARAMS !== 'undefined' ? AVAILABLE_PARAMS : [["No Params", "NONE"]];
            }), "PARAM_NAME");
        this.setOutput(true, null);
        this.setColour(290);
        this.setTooltip("Reads a test parameter value from the test configuration (e.g., input voltage, load step).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_get_param'] = function (block, generator) {
    var param = block.getFieldValue('PARAM_NAME');
    return ["test_params.get('" + param + "', 0)", generator.ORDER_ATOMIC];
};

// --- Log Message ---
Blockly.Blocks['inst_log'] = {
    init: function () {
        this.appendValueInput("MESSAGE")
            .setCheck(null)
            .appendField("Log Message");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(290);
        this.setTooltip("Writes a message to the test log panel.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['inst_log'] = function (block, generator) {
    var msg = generator.valueToCode(block, 'MESSAGE', generator.ORDER_ATOMIC) || '""';
    return 'log_callback(str(' + msg + '))\n';
};


// =============================================================================
// AC SOURCE BLOCKS  (maps to mgr.ac_source — ChromaAcSource / Chroma 61500 series)
// SCPI Reference: Chroma 61500 Series Programming Manual
// Colour: 195 (teal-blue — distinct from DC source orange and load green)
// =============================================================================

// --- AC Output ON ---
Blockly.Blocks['ac_output_on'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("AC Source Output ON");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: OUTPut:STATe ON  — Enables the AC source output.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_output_on'] = function (block, generator) {
    return 'mgr.ac_source.output_on()\n';
};

// --- AC Output OFF ---
Blockly.Blocks['ac_output_off'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("AC Source Output OFF");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: OUTPut:STATe OFF  — Disables the AC source output.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_output_off'] = function (block, generator) {
    return 'mgr.ac_source.output_off()\n';
};

// --- Set AC Voltage ---
Blockly.Blocks['ac_set_voltage'] = {
    init: function () {
        this.appendValueInput("VOLTAGE")
            .setCheck("Number")
            .appendField("Set AC Voltage (Vrms) to");
        this.appendDummyInput().appendField("Vrms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:VOLTage:LEVel <V>  — Sets AC output RMS voltage.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_voltage'] = function (block, generator) {
    var v = generator.valueToCode(block, 'VOLTAGE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage(' + v + ')\n';
};

// --- Set AC Voltage Range ---
Blockly.Blocks['ac_set_voltage_range'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set AC Voltage Range")
            .appendField(new Blockly.FieldDropdown([
                ["Low (0–155 Vrms)", "LOW"],
                ["High (0–310 Vrms)", "HIGH"]
            ]), "RANGE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:VOLTage:RANGe LOW|HIGH  — Selects low or high voltage range.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_voltage_range'] = function (block, generator) {
    var r = block.getFieldValue('RANGE');
    return 'mgr.ac_source.set_voltage_range("' + r + '")\n';
};

// --- Set AC Frequency ---
Blockly.Blocks['ac_set_frequency'] = {
    init: function () {
        this.appendValueInput("FREQ")
            .setCheck("Number")
            .appendField("Set AC Frequency to");
        this.appendDummyInput().appendField("Hz");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:FREQuency:LEVel <Hz>  — Sets AC output frequency (e.g. 50 or 60 Hz).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_frequency'] = function (block, generator) {
    var f = generator.valueToCode(block, 'FREQ', generator.ORDER_ATOMIC) || '50';
    return 'mgr.ac_source.set_frequency(' + f + ')\n';
};

// --- Set AC Current Limit ---
Blockly.Blocks['ac_set_current_limit'] = {
    init: function () {
        this.appendValueInput("CURRENT")
            .setCheck("Number")
            .appendField("Set AC Current Limit to");
        this.appendDummyInput().appendField("A rms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:CURRent:LIMit <A>  — Sets RMS current limit.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_current_limit'] = function (block, generator) {
    var i = generator.valueToCode(block, 'CURRENT', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_current_limit(' + i + ')\n';
};

// --- Set AC Phase Angle ---
Blockly.Blocks['ac_set_phase'] = {
    init: function () {
        this.appendValueInput("ANGLE")
            .setCheck("Number")
            .appendField("Set AC Phase Angle to");
        this.appendDummyInput().appendField("°");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:PHASe:ANGLe <deg>  — Sets output phase (0–360°).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_phase'] = function (block, generator) {
    var a = generator.valueToCode(block, 'ANGLE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_phase(' + a + ')\n';
};

// --- Set AC Phase On/Off ---
Blockly.Blocks['ac_set_phase_on_off'] = {
    init: function () {
        this.appendValueInput("ANGLE_ON")
            .setCheck("Number")
            .appendField("AC Phase at Output-ON");
        this.appendDummyInput().appendField("°");
        this.appendValueInput("ANGLE_OFF")
            .setCheck("Number")
            .appendField("AC Phase at Output-OFF");
        this.appendDummyInput().appendField("°");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:PHASe:STARt / STOP  — Sets the phase at which output turns on/off.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_phase_on_off'] = function (block, generator) {
    var on  = generator.valueToCode(block, 'ANGLE_ON',  generator.ORDER_ATOMIC) || '0';
    var off = generator.valueToCode(block, 'ANGLE_OFF', generator.ORDER_ATOMIC) || '0';
    var code = 'mgr.ac_source.set_phase_on(' + on + ')\n';
    code    += 'mgr.ac_source.set_phase_off(' + off + ')\n';
    return code;
};

// --- Set AC Waveform Shape ---
Blockly.Blocks['ac_set_waveform'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set AC Waveform")
            .appendField(new Blockly.FieldDropdown([
                ["Sine",   "SINE"],
                ["Square", "SQUare"],
                ["User 1", "USER1"],
                ["User 2", "USER2"],
                ["User 3", "USER3"]
            ]), "SHAPE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:WAVeform:SHAPe SINE|SQUare|USER<n>  — Selects output waveform.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_waveform'] = function (block, generator) {
    var s = block.getFieldValue('SHAPE');
    return 'mgr.ac_source.set_waveform("' + s + '")\n';
};

// --- Set AC Voltage Slew Rate ---
Blockly.Blocks['ac_set_voltage_slew'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set AC Voltage Slew Rate to");
        this.appendDummyInput().appendField("V/s");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:VOLTage:SLEW <V/s>  — Sets how fast voltage changes.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_voltage_slew'] = function (block, generator) {
    var r = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_voltage_slew(' + r + ')\n';
};

// --- Set AC Frequency Slew Rate ---
Blockly.Blocks['ac_set_frequency_slew'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set AC Frequency Slew Rate to");
        this.appendDummyInput().appendField("Hz/s");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:FREQuency:SLEW <Hz/s>  — Sets how fast frequency ramps.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_frequency_slew'] = function (block, generator) {
    var r = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_frequency_slew(' + r + ')\n';
};

// --- Set AC OVP ---
Blockly.Blocks['ac_set_ovp'] = {
    init: function () {
        this.appendValueInput("OVP")
            .setCheck("Number")
            .appendField("Set AC OVP to");
        this.appendDummyInput().appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:VOLTage:PROTect:LEVel <V>  — Over-voltage protection threshold.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_ovp'] = function (block, generator) {
    var v = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_ovp(' + v + ')\n';
};

// --- Set AC OCP ---
Blockly.Blocks['ac_set_ocp'] = {
    init: function () {
        this.appendValueInput("OCP")
            .setCheck("Number")
            .appendField("Set AC OCP to");
        this.appendDummyInput().appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:CURRent:PROTect:LEVel <A>  — Over-current protection threshold.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_set_ocp'] = function (block, generator) {
    var i = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC) || '0';
    return 'mgr.ac_source.set_ocp(' + i + ')\n';
};

// --- Clear AC Protection ---
Blockly.Blocks['ac_clear_protection'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Clear AC Source Protection");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: SOURce:PROTect:CLEar  — Clears latched OVP/OCP fault.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_clear_protection'] = function (block, generator) {
    return 'mgr.ac_source.clear_protection()\n';
};

// --- Measure AC Voltage ---
Blockly.Blocks['ac_measure_voltage'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Voltage (Vrms)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:VOLTage:RMS?  — Returns measured RMS output voltage.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_voltage'] = function (block, generator) {
    return ['mgr.ac_source.measure_voltage()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Current ---
Blockly.Blocks['ac_measure_current'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Current (Arms)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:CURRent:RMS?  — Returns measured RMS output current.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_current'] = function (block, generator) {
    return ['mgr.ac_source.measure_current()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Power (Real) ---
Blockly.Blocks['ac_measure_power'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Real Power (W)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:POWer:REAL?  — Returns active (real) power in Watts.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_power'] = function (block, generator) {
    return ['mgr.ac_source.measure_power()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Apparent Power ---
Blockly.Blocks['ac_measure_apparent_power'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Apparent Power (VA)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:POWer:APParent?  — Returns apparent power in VA.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_apparent_power'] = function (block, generator) {
    return ['mgr.ac_source.measure_apparent_power()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Power Factor ---
Blockly.Blocks['ac_measure_pf'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Power Factor");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:POWer:PFACtor?  — Returns power factor (0.0–1.0).");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_pf'] = function (block, generator) {
    return ['mgr.ac_source.measure_pf()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Frequency ---
Blockly.Blocks['ac_measure_frequency'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Output Frequency (Hz)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:FREQuency?  — Returns actual output frequency in Hz.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_frequency'] = function (block, generator) {
    return ['mgr.ac_source.measure_frequency()', generator.ORDER_FUNCTION_CALL];
};

// --- Measure AC Crest Factor ---
Blockly.Blocks['ac_measure_crest_factor'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Crest Factor");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:CURRent:CREStfactor?  — Returns the current crest factor.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_crest_factor'] = function (block, generator) {
    return ['mgr.ac_source.measure_crest_factor()', generator.ORDER_FUNCTION_CALL];
};

// --- AC Peak Current ---
Blockly.Blocks['ac_measure_current_peak'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure AC Peak Current (A)");
        this.setOutput(true, "Number");
        this.setColour(195);
        this.setTooltip("SCPI: MEASure:CURRent:PEAK?  — Returns peak current.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_measure_current_peak'] = function (block, generator) {
    return ['mgr.ac_source.measure_current_peak()', generator.ORDER_FUNCTION_CALL];
};

// --- AC Source Reset ---
Blockly.Blocks['ac_reset'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("AC Source Reset (*RST)");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("SCPI: *RST  — Resets the AC source to factory defaults.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_reset'] = function (block, generator) {
    return 'mgr.ac_source.reset()\n';
};

// --- AC Configure (all-in-one) ---
Blockly.Blocks['ac_configure'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Configure AC Source");
        this.appendValueInput("VOLTAGE")
            .setCheck("Number")
            .appendField("Voltage (Vrms)");
        this.appendValueInput("FREQ")
            .setCheck("Number")
            .appendField("Frequency (Hz)");
        this.appendValueInput("CURRENT")
            .setCheck("Number")
            .appendField("Current Limit (A)");
        this.appendDummyInput()
            .appendField("Waveform")
            .appendField(new Blockly.FieldDropdown([
                ["Sine",   "SINE"],
                ["Square", "SQUare"],
                ["User 1", "USER1"]
            ]), "SHAPE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(195);
        this.setTooltip("Sets AC voltage, frequency, current limit, and waveform in one block.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_configure'] = function (block, generator) {
    var v = generator.valueToCode(block, 'VOLTAGE', generator.ORDER_ATOMIC) || '0';
    var f = generator.valueToCode(block, 'FREQ',    generator.ORDER_ATOMIC) || '50';
    var i = generator.valueToCode(block, 'CURRENT', generator.ORDER_ATOMIC) || '0';
    var s = block.getFieldValue('SHAPE');
    var code  = 'mgr.ac_source.set_voltage(' + v + ')\n';
    code     += 'mgr.ac_source.set_frequency(' + f + ')\n';
    code     += 'mgr.ac_source.set_current_limit(' + i + ')\n';
    code     += 'mgr.ac_source.set_waveform("' + s + '")\n';
    return code;
};

// --- AC Source Status ---
Blockly.Blocks['ac_get_status'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("AC Source Error Status");
        this.setOutput(true, "String");
        this.setColour(195);
        this.setTooltip("SCPI: SYSTem:ERRor?  — Returns error code and message from AC source.");
        this.setHelpUrl("");
    }
};
pythonGenerator.forBlock['ac_get_status'] = function (block, generator) {
    return ['mgr.ac_source.get_status()', generator.ORDER_FUNCTION_CALL];
};


console.log("custom_blocks.js loaded successfully. Total block categories: Source (DC), Load, Scope, System, AC Source.");


