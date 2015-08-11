import asyncio
from .protocol.factory import parse, build


class Board:
    def __init__(self, serial_device=None, wait=2):
        """ Exposes the Firmata API

        :param serial_device: Serial device to use, or None
        :param wait: Time to wait for board to reset.  Uno=2, Leo=0
        """
        self.serial_device = serial_device
        self.sleep_time_until_ready = wait
        self.digital_pin_ports = [0] * 8  # move to autoconfig
        self.started = False

        self.packet_parser = parse(self.handle_packet)
        self.packet_factory = build

    def start(self):
        if self.started:
            raise RuntimeError

        yield from asyncio.sleep(self.sleep_time_until_ready)
        self.started = True

    def handle_packet(self, packet):
        if packet.name == 'digital_io_message':
            port_value = self.digital_pin_ports[packet.port]
             # TODO

    def send_packet(self, name, **kwargs):
        packet = self.packet_factory(name, **kwargs)
        self.send_bytes(packet)

    def send_bytes(self, command):
        command = bytes(command)
        print('sending', " ".join("{:02x}".format(c) for c in command))
        self.serial_device.write(command)

    @asyncio.coroutine
    def wait_for_command(self, command):
        pass

    def analog_read(self, pin):
        """ Retrieve the last data update for the specified analog pin
        """
        raise NotImplementedError

    def analog_write(self, pin, value):
        """ Set the selected pin to the specified value
        """
        self.send_packet('analog_io_message', pin=pin, value=value)

    def digital_read(self, pin):
        """ Retrieve the last data update for the specified digital pin
        """
        raise NotImplementedError

    def digital_write(self, pin, value):
        """ Set the specified pin to the specified value.
        """
        port_no = int(pin // 8)
        port_value = self.digital_pin_ports[port_no]

        mask = 1 << (pin % 8)

        if value:
            port_value |= mask
        else:
            port_value &= ~mask

        self.digital_pin_ports[port_no] = port_value

        self.send_packet('digital_io_message', port=port_no, value=port_value)

    def extended_analog(self, pin, data):
        """ This method will send an extended-data analog write command to the selected pin.
        """
        # analog_data = [pin, data & 0x7f, (data >> 7) & 0x7f, data >> 14]
        # yield from self.send_sysex(protocol.EXTENDED_ANALOG, analog_data)
        raise NotImplementedError

    def request_analog_map(self):
        self.send_packet('analog_mapping_query')

    def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """ Configure a pin as a servo pin. Set pulse min, max in ms.

        Use this method (not set_pin_mode) to configure a pin for servo operation.
        """
        self.send_packet('servo_config', pin=pin, min_pulse=min_pulse, max_pulse=max_pulse)

    def set_pin_mode(self, pin_number, pin_mode):
        """This method sets the pin PinMode for the specified pin.
        For Servo, use servo_config() instead.
        """
        self.send_packet('set_pin_mode', pin=pin_number, mode=pin_mode)

    def set_sampling_interval(self, interval):
        """ This method sends the desired sampling interval

        Note: Firmata will ignore any interval less than 10 milliseconds

        :param interval: sampling interval in ms
        :return: None
        """
        self.send_packet('sampling_interval', interval=interval)

