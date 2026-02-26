// custom_blocks.js
// Contains definitions and Python generators for custom blocks
// Organized by Instrument Type

console.log("Loading custom_blocks.js (v20260210_1610)...");
console.log("DEBUG: This version uses 'generator.valueToCode' exclusively.");

// Ensure pythonGenerator is available. It should be defined in editor.html
// We explicitly use window.pythonGenerator or Blockly.Python to ensure it's the instance.
var pythonGenerator = window.pythonGenerator || Blockly.Python;

if (!pythonGenerator) {
    console.error("CRITICAL: Blockly.Python is not loaded!");
} else {
    // Compatibility for newer Blockly versions (v10+)
    // Block generators should be on .forBlock
    pythonGenerator.forBlock = pythonGenerator.forBlock || {};
}

console.log("Using pythonGenerator instance:", !!pythonGenerator);

// =============================================================================
// Source Blocks (Chroma 61501 / 61602)
// =============================================================================

Blockly.Blocks['inst_set_voltage'] = {
    init: function () {
        this.appendValueInput("VOLTAGE")
            .setCheck("Number")
            .appendField("Set Source Voltage to");
        this.appendDummyInput()
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20); // Source Color
        this.setTooltip("Sets the AC Source Voltage");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_set_voltage'] = function (block, generator) {
    var value_voltage = generator.valueToCode(block, 'VOLTAGE', generator.ORDER_ATOMIC);
    var code = 'mgr.ac_source.set_voltage(' + value_voltage + ')\n';
    return code;
};

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
        this.setTooltip("Sets the AC Source Frequency");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_set_frequency'] = function (block, generator) {
    var value_freq = generator.valueToCode(block, 'FREQUENCY', generator.ORDER_ATOMIC);
    var code = 'mgr.ac_source.set_frequency(' + value_freq + ')\n';
    return code;
};

Blockly.Blocks['inst_source_measure_voltage'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Voltage");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_measure_voltage'] = function (block, generator) {
    var code = 'mgr.ac_source.measure_voltage()';
    return [code, generator.ORDER_NONE];
};

Blockly.Blocks['inst_source_measure_current'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Current");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_measure_current'] = function (block, generator) {
    var code = 'mgr.ac_source.measure_current()';
    return [code, generator.ORDER_NONE];
};

Blockly.Blocks['inst_source_slew_rate'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Source Slew Rate");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_slew_rate'] = function (block, generator) {
    var val = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC);
    var code = 'mgr.ac_source.set_voltage_slew_rate(' + val + ')\n';
    return code;
};

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
        this.setTooltip("Set Over Voltage/Current/Power Protections");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_protections'] = function (block, generator) {
    var ovp = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC) || "None";
    var ocp = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC) || "None";
    var opp = generator.valueToCode(block, 'OPP', generator.ORDER_ATOMIC) || "None";

    var code = "";
    if (ovp !== "None") code += 'mgr.ac_source.set_ovp(' + ovp + ')\n';
    if (ocp !== "None") code += 'mgr.ac_source.set_ocp(' + ocp + ')\n';
    if (opp !== "None") code += 'mgr.ac_source.set_opp(' + opp + ')\n';
    return code;
};

Blockly.Blocks['inst_output_on'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Source Output ON");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_output_on'] = function (block, generator) {
    return 'mgr.ac_source.output_on()\n';
};

Blockly.Blocks['inst_output_off'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Source Output OFF");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_output_off'] = function (block, generator) {
    return 'mgr.ac_source.output_off()\n';
};

// =============================================================================
// Load Blocks (Chroma 63200A / 63800)
// =============================================================================

Blockly.Blocks['inst_load_mode'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Load Mode to")
            .appendField(new Blockly.FieldDropdown([["CC", "CC"], ["CV", "CV"], ["CR", "CR"], ["CP", "CP"]]), "MODE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("Set Electronic Load Mode (Constant Current/Voltage/Resistance/Power)");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_mode'] = function (block, generator) {
    var dropdown_mode = block.getFieldValue('MODE');
    var code = 'mgr.dc_load.set_mode("' + dropdown_mode + '")\n';
    return code;
};

Blockly.Blocks['inst_set_current'] = {
    init: function () {
        this.appendValueInput("CURRENT")
            .setCheck("Number")
            .appendField("Set Load Current to");
        this.appendDummyInput()
            .appendField("A");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120); // Load Color
        this.setTooltip("Sets the DC Load Current");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_set_current'] = function (block, generator) {
    var value_current = generator.valueToCode(block, 'CURRENT', generator.ORDER_ATOMIC);
    var code = 'mgr.dc_load.set_current(' + value_current + ')\n';
    return code;
};

Blockly.Blocks['inst_load_output'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Turn Load Output")
            .appendField(new Blockly.FieldDropdown([["ON", "ON"], ["OFF", "OFF"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_output'] = function (block, generator) {
    var dropdown_state = block.getFieldValue('STATE');
    if (dropdown_state === "ON") return 'mgr.dc_load.load_on()\n';
    else return 'mgr.dc_load.load_off()\n';
};

Blockly.Blocks['inst_load_slew_rate'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Load Slew Rate");
        this.appendDummyInput()
            .appendField("A/us");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_slew_rate'] = function (block, generator) {
    var val = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC);
    var code = 'mgr.dc_load.set_slew_rate(' + val + ')\n';
    return code;
};

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
        this.setTooltip("Set Load Protections");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_protections'] = function (block, generator) {
    var ovp = generator.valueToCode(block, 'OVP', generator.ORDER_ATOMIC) || "None";
    var ocp = generator.valueToCode(block, 'OCP', generator.ORDER_ATOMIC) || "None";
    var opp = generator.valueToCode(block, 'OPP', generator.ORDER_ATOMIC) || "None";

    var code = "";
    if (ovp !== "None") code += 'mgr.dc_load.set_ovp(' + ovp + ')\n';
    if (ocp !== "None") code += 'mgr.dc_load.set_ocp(' + ocp + ')\n';
    if (opp !== "None") code += 'mgr.dc_load.set_opp(' + opp + ')\n';
    return code;
};

Blockly.Blocks['inst_measure_voltage'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Voltage");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_measure_voltage'] = function (block, generator) {
    var code = 'mgr.dc_load.measure_voltage()';
    return [code, generator.ORDER_NONE];
};

Blockly.Blocks['inst_measure_current'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Current");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_measure_current'] = function (block, generator) {
    var code = 'mgr.dc_load.measure_current()';
    return [code, generator.ORDER_NONE];
};

// =============================================================================
// Scope Blocks (Tektronix)
// =============================================================================

Blockly.Blocks['inst_scope_horizontal'] = {
    init: function () {
        this.appendValueInput("SCALE")
            .setCheck("Number")
            .appendField("Set Scope Time Base");
        this.appendDummyInput()
            .appendField("ms/div");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_horizontal'] = function (block, generator) {
    var val = generator.valueToCode(block, 'SCALE', generator.ORDER_ATOMIC);
    // Convert ms to s
    var code = 'mgr.scope.set_time_scale(' + val + ' / 1000.0)\n';
    return code;
};

Blockly.Blocks['inst_scope_vertical'] = {
    init: function () {
        this.appendValueInput("SCALE")
            .setCheck("Number")
            .appendField("Set Scope Vertical Scale for Ch");
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL")
            .appendField("to")
            .appendField("V/div");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_vertical'] = function (block, generator) {
    var channel = block.getFieldValue('CHANNEL');
    var val = generator.valueToCode(block, 'SCALE', generator.ORDER_ATOMIC);
    var code = 'mgr.scope.set_vertical_scale(' + channel + ', ' + val + ')\n';
    return code;
};

Blockly.Blocks['inst_scope_enable'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope Channel")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL")
            .appendField(new Blockly.FieldDropdown([["ON", "ON"], ["OFF", "OFF"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_enable'] = function (block, generator) {
    var channel = block.getFieldValue('CHANNEL');
    var state = block.getFieldValue('STATE');
    var bool_state = (state === "ON") ? "True" : "False";
    var code = 'mgr.scope.enable_channel(' + channel + ', ' + bool_state + ')\n';
    return code;
};

// =============================================================================
// Additional Source Blocks
// =============================================================================

Blockly.Blocks['inst_source_voltage_rise'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Voltage Rise Rate");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_voltage_rise'] = function (block, generator) {
    var val = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC);
    return 'mgr.ac_source.set_voltage_rise(' + val + ')\n';
};

Blockly.Blocks['inst_source_voltage_fall'] = {
    init: function () {
        this.appendValueInput("RATE")
            .setCheck("Number")
            .appendField("Set Voltage Fall Rate");
        this.appendDummyInput()
            .appendField("V/ms");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_voltage_fall'] = function (block, generator) {
    var val = generator.valueToCode(block, 'RATE', generator.ORDER_ATOMIC);
    return 'mgr.ac_source.set_voltage_fall(' + val + ')\n';
};

Blockly.Blocks['inst_source_clear_protection'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Clear Source Protection");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_clear_protection'] = function (block, generator) {
    return 'mgr.ac_source.clear_protection()\n';
};

Blockly.Blocks['inst_source_measure_freq'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Source Frequency");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_measure_freq'] = function (block, generator) {
    return ['mgr.ac_source.measure_frequency()', generator.ORDER_NONE];
};

Blockly.Blocks['inst_source_measure_apparent'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Apparent Power");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_measure_apparent'] = function (block, generator) {
    return ['mgr.ac_source.measure_apparent_power()', generator.ORDER_NONE];
};

Blockly.Blocks['inst_source_measure_pf'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Power Factor");
        this.setOutput(true, "Number");
        this.setColour(20);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_source_measure_pf'] = function (block, generator) {
    return ['mgr.ac_source.measure_pf()', generator.ORDER_NONE];
};

// =============================================================================
// Additional Load Blocks
// =============================================================================

Blockly.Blocks['inst_load_dynamic'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Load Dynamic Mode")
            .appendField(new Blockly.FieldDropdown([["ON", "ON"], ["OFF", "OFF"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_dynamic'] = function (block, generator) {
    var dropdown_state = block.getFieldValue('STATE');
    var bool_state = (dropdown_state === "ON") ? "True" : "False";
    return 'mgr.dc_load.set_dynamic_mode(' + bool_state + ')\n';
};

Blockly.Blocks['inst_load_clear_protection'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Clear Load Protection");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_clear_protection'] = function (block, generator) {
    return 'mgr.dc_load.clear_protection()\n';
};

Blockly.Blocks['inst_load_measure_resistance'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Measure Load Resistance");
        this.setOutput(true, "Number");
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_load_measure_resistance'] = function (block, generator) {
    return ['mgr.dc_load.measure_resistance()', generator.ORDER_NONE];
};


// =============================================================================
// Additional Scope Blocks
// =============================================================================

Blockly.Blocks['inst_scope_run_stop'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Scope Acquisition")
            .appendField(new Blockly.FieldDropdown([["RUN", "RUN"], ["STOP", "STOP"], ["SINGLE", "SINGLE"]]), "STATE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_run_stop'] = function (block, generator) {
    var state = block.getFieldValue('STATE');
    if (state === "RUN") return 'mgr.scope.run()\n';
    if (state === "STOP") return 'mgr.scope.stop()\n';
    if (state === "SINGLE") return 'mgr.scope.single()\n';
    return '';
};

Blockly.Blocks['inst_scope_delay'] = {
    init: function () {
        this.appendValueInput("DELAY")
            .setCheck("Number")
            .appendField("Set Scope Horizontal Delay");
        this.appendDummyInput()
            .appendField("s");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_delay'] = function (block, generator) {
    var val = generator.valueToCode(block, 'DELAY', generator.ORDER_ATOMIC);
    return 'mgr.scope.set_delay(' + val + ')\n';
};

Blockly.Blocks['inst_scope_offset'] = {
    init: function () {
        this.appendValueInput("OFFSET")
            .setCheck("Number")
            .appendField("Set Scope CH");
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL")
            .appendField("Offset to")
            .appendField("V");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_offset'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var val = generator.valueToCode(block, 'OFFSET', generator.ORDER_ATOMIC);
    return 'mgr.scope.set_vertical_offset(' + ch + ', ' + val + ')\n';
};

Blockly.Blocks['inst_scope_coupling'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL")
            .appendField("Coupling")
            .appendField(new Blockly.FieldDropdown([["DC", "DC"], ["AC", "AC"], ["GND", "GND"]]), "COUP");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_coupling'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var coup = block.getFieldValue('COUP');
    return 'mgr.scope.set_coupling(' + ch + ', "' + coup + '")\n';
};

Blockly.Blocks['inst_scope_bandwidth'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Scope CH")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL")
            .appendField("Bandwidth")
            .appendField(new Blockly.FieldDropdown([["FULL", "FULL"], ["20MHz", "20E6"], ["250MHz", "250E6"]]), "BW");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_bandwidth'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var bw = block.getFieldValue('BW');
    return 'mgr.scope.set_bandwidth(' + ch + ', "' + bw + '")\n';
};

Blockly.Blocks['inst_scope_trigger'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Set Trigger: CH")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL");
        this.appendValueInput("LEVEL")
            .setCheck("Number")
            .appendField("Level (V)");
        this.appendDummyInput()
            .appendField("Slope")
            .appendField(new Blockly.FieldDropdown([["RISE", "RISE"], ["FALL", "FALL"]]), "SLOPE");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_trigger'] = function (block, generator) {
    var ch = block.getFieldValue('CHANNEL');
    var slope = block.getFieldValue('SLOPE');
    var level = generator.valueToCode(block, 'LEVEL', generator.ORDER_ATOMIC);
    return 'mgr.scope.set_trigger(' + ch + ', ' + level + ', "' + slope + '")\n';
};

Blockly.Blocks['inst_scope_configure_meas'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Config Meas Slot")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "SLOT")
            .appendField("Type")
            .appendField(new Blockly.FieldDropdown([["Pk-Pk", "PK2PK"], ["RMS", "RMS"], ["Freq", "FREQ"], ["Max", "MAX"], ["Min", "MIN"]]), "TYPE")
            .appendField("on CH")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "CHANNEL");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_configure_meas'] = function (block, generator) {
    var slot = block.getFieldValue('SLOT');
    var type = block.getFieldValue('TYPE');
    var ch = block.getFieldValue('CHANNEL');
    return 'mgr.scope.configure_measurement(' + slot + ', "' + type + '", ' + ch + ')\n';
};

Blockly.Blocks['inst_scope_get_meas'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Get Measurement Value from Slot")
            .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"]]), "SLOT");
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_get_meas'] = function (block, generator) {
    var slot = block.getFieldValue('SLOT');
    return ['mgr.scope.get_measurement(' + slot + ')', generator.ORDER_NONE];
};

Blockly.Blocks['inst_scope_save_screenshot'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Save Scope Screenshot");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip("Captures and saves a screenshot from the oscilloscope");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_scope_save_screenshot'] = function (block, generator) {
    var code = 'import datetime\n';
    code += 'ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")\n';
    code += 'fname = os.path.abspath(f"reports/captures/{ts}_manual.png")\n';
    code += 'os.makedirs(os.path.dirname(fname), exist_ok=True)\n';
    code += 'mgr.scope.save_screenshot(fname)\n';
    code += 'images.append({"name": "Manual Capture", "path": fname})\n';
    return code;
};


// =============================================================================
// User / System Blocks
// =============================================================================

Blockly.Blocks['inst_wait'] = {
    init: function () {
        this.appendValueInput("SECONDS")
            .setCheck("Number")
            .appendField("Wait");
        this.appendDummyInput()
            .appendField("seconds");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(290); // User Color
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_wait'] = function (block, generator) {
    var value_seconds = generator.valueToCode(block, 'SECONDS', generator.ORDER_ATOMIC);
    return 'time.sleep(' + value_seconds + ')\n';
};

Blockly.Blocks['inst_get_param'] = {
    init: function () {
        this.appendDummyInput()
            .appendField("Get Parameter")
            .appendField(new Blockly.FieldDropdown(function () {
                // AVAILABLE_PARAMS is defined in editor.html
                return typeof AVAILABLE_PARAMS !== 'undefined' ? AVAILABLE_PARAMS : [["No Params", "NONE"]];
            }), "PARAM_NAME");
        this.setOutput(true, null); // Can return number or string
        this.setColour(290);
        this.setTooltip("Gets a value from the Test Configuration");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_get_param'] = function (block, generator) {
    var dropdown_param_name = block.getFieldValue('PARAM_NAME');
    var code = "test_params.get('" + dropdown_param_name + "', 0)";
    return [code, generator.ORDER_ATOMIC];
};

Blockly.Blocks['inst_log'] = {
    init: function () {
        this.appendValueInput("MESSAGE")
            .setCheck(null)
            .appendField("Log Message");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

pythonGenerator.forBlock['inst_log'] = function (block, generator) {
    var value_message = generator.valueToCode(block, 'MESSAGE', generator.ORDER_ATOMIC);
    return 'log_callback(str(' + value_message + '))\n';
};
