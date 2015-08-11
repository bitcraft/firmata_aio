import unittest
from firmata_aio.protocol.commands import command_names, command_lookup, sysex_commands
from firmata_aio.protocol.factory import parse, build, Container


class ProtocolTest(unittest.TestCase):
    def setUp(self):
        pass


outgoing_test_data = {
    0x69: (b'\xF0\x69\xF7', None),
    0x6B: (b'\xF0\x6B\xF7', None),
    0x6D: (b'\xF0\x6D\xF7', None),
    0x6F: (b'\xF0\x6F\x0C\x01\x01\xF7', Container(pin=12, value=129)),
    0x70: (b'\xF0\x70\x0C\x00\x00\x01\x01\xF7', Container(pin=12, min_pulse=0, max_pulse=129)),
    0x79: (b'\xF0\x79\xF7', None),
    0x7A: (b'\xF0\x7A\x00\x00\xF7', Container(interval=0)),
    0x90: (b'\x92\x02\x01', Container(pin=2, value=130)),
    0xC0: (b'\xC3\x01\x02', Container(pin=3, toggle=1)),
    0xD0: (b'\xD4\x00\x02', Container(pin=4, toggle=0)),
    0xE0: (b'\xE1\x01\x02', Container(pin=1, value=130)),
    0xF0: (b'\xF0', None),
    0xF4: (b'\xF4\x0D\x01', Container(pin=13, mode=1)),
    0xF5: (b'\xF5\x00\x00', Container(pin=0, value=0)),
    # 0xF7: (b'\xF7', None),  # not tested b/c not normally found in use
}

incoming_test_data = {
    # 0x61: 'encoder_data',
    0x6A: (b'\xF0\x6A\x01\xF7', Container(channel=1)),
    # 0x6C: 'capability_response',
    # 0x6E: (Byte('pin'), Byte('pin_mode')),  # pin state/mode response
    # 0x6F: 'extended_analog',
    # 0x70: 'servo_config',
    # 0x71: 'string_data',
    # 0x72: 'stepper_data',
    # 0x73: 'onewire_data',
    # 0x75: 'shift_data',
    # 0x76: 'i2c_request',
    # 0x77: 'i2c_reply',
    # 0x78: 'i2c_config',
    # 0x79: (Byte('major_version'), Byte('minor_version')),
    # 0x7A: 'sampling_interval',
    # 0x7B: 'scheduler_data',
    # 0x7E: 'sysex_non_realtime',
    # 0x7F: 'sysex_realtime',
}


# self-test
test_groups = (incoming_test_data, outgoing_test_data)
for test_group in test_groups:
    for command, test_data in test_group.items():
        packet_data, expected_value = test_data
        name = command_names[command]

        parser = parse(lambda *i: print(i))
        parser.send(None)

        for byte in packet_data:
            parser.send(byte)

print(build('report_analog_pin', pin=4, value=1))
print(build('report_digital_port', port=2, value=1))
print(build('set_pin_mode', pin=2, mode=1))
print(build('set_digital_pin_value', pin=2, value=0))
print(build('digital_io_message', port=3, value=2))
