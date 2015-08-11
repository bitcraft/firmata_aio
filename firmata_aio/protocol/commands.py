"""
Define command names and prove command/code mappings
"""
from collections import ChainMap

__all__ = [
    'nibble_commands',
    'byte_commands',
    'sysex_commands',
    'command_lookup',
    'command_names',
]

INPUT, OUTPUT, ANALOG, \
PWM, SERVO, I2C, ONEWIRE, \
STEPPER, ENCODER = range(0, 9)

# do not combine names and packet structure:
# packets sometimes share same name and code, but have different
# structure depending on the origin (firmata or client)

# do not combine them: their membership to a particular
# group defines the packet structure that builds them
nibble_commands = {
    0xE0: ('analog_io_message', ('pin', 'value')),
    0x90: ('digital_io_message', ('port', 'value')),
    0xC0: ('report_analog_pin', ('pin', 'value')),
    0xD0: ('report_digital_port', ('port', 'value')),
}
byte_commands = {
    0xF0: ('start_sysex', ()),
    0xF4: ('set_pin_mode', ('pin', 'mode')),
    0xF5: ('set_digital_pin_value', ('pin', 'value')),
    0xF7: ('stop_sysex', ()),
    0xF9: ('protocol_version', ('major', 'minor'))
}
sysex_commands = {
    0x61: ('encoder_data', ()),
    0x69: ('analog_mapping_query', ()),
    0x6A: ('analog_mapping_response', ()),
    0x6B: ('capability_query', ()),
    0x6C: ('capability_response', ()),
    0x6D: ('pin_state_query', ()),
    0x6E: ('pin_state_response', ()),
    0x6F: ('extended_analog', ()),
    0x70: ('servo_config', ()),
    0x71: ('string_data', ()),
    0x72: ('stepper_data', ()),
    0x73: ('onewire_data', ()),
    0x75: ('shift_data', ()),
    0x76: ('i2c_request', ()),
    0x77: ('i2c_reply', ()),
    0x78: ('i2c_config', ()),
    0x79: ('report_firmware', ()),
    0x7A: ('sampling_interval', ()),
    0x7B: ('scheduler_data', ()),
    0x7E: ('sysex_non_realtime', ()),
    0x7F: ('sysex_realtime', ()),
}

# Code => Name mapping for all types
command_names = ChainMap(nibble_commands, byte_commands, sysex_commands)

# Name => Code mapping for all types
command_lookup = {v[0]: k for k, v in command_names.items()}
