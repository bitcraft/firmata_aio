import unittest
from construct import Container
from firmata_aio.protocol.commands import command_names, command_lookup, sysex_commands
from firmata_aio.protocol.packets import incoming_packet_structure, outgoing_packet_structure
from firmata_aio.protocol.factory import generate_packet_mapping


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
    0xC0: (b'\xC3\x01\x02', Container(pin=3, toggle=1, noop=2)),
    0xD0: (b'\xD4\x01\x02', Container(pin=4, toggle=1, noop=2)),
    0xE0: (b'\xE1\x02\x01', Container(pin=1, value=130)),
    0xF0: (b'\xF0', None),
    0xF4: (b'\xF4\x0D\x01', Container(pin=13, mode=1)),
    0xF5: (b'\xF5\x00\x00', Container(pin=0, value=0)),
    0xF7: (b'\xF7', None),
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
packet_mapping = generate_packet_mapping(outgoing_packet_structure)
test_groups = (incoming_test_data, outgoing_test_data)
for test_group in test_groups:
    for command, test_data in test_group.items():
        packet_data, expected_value = test_data
        name = command_names[command]
        try:
            factory = packet_mapping[name]
        except KeyError:
            print('missing structure for', name)
            continue

        print('testing {:#x} {}...'.format(command, name))

        if expected_value is None:
            expected_value = Container()

        # add the command to the container to check
        expected_value['command'] = command

        # we add the start and end sysex values to make the test a bit cleaner
        if command in sysex_commands:
            expected_value['start_sysex'] = command_lookup['start_sysex']
            expected_value['stop_sysex'] = command_lookup['stop_sysex']

        # test parse from data
        value = factory.parse(packet_data)
        try:
            assert (value == expected_value)
        except AssertionError:
            print(name)
            print(value, '\n', expected_value)

        # test build from container
        value = factory.build(expected_value)
        try:
            assert (packet_data == value)
        except AssertionError:
            print(name)
            print(packet_data, '\n', value)
