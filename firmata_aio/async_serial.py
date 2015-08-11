import asyncio

import serial


class AsyncSerial:
    """polling, yuck!...works on windows though
    """

    def __init__(self, *, loop=None, port='/dev/ttyACM0', speed=57600):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

        self._incoming_buffer = bytearray()
        self._outgoing_buffer = bytearray()
        self._serial_device = serial.Serial(port, speed, timeout=.1)

        self.loop.call_soon(self.process_buffers)

    def process_buffers(self, *args):
        self.data_received()
        self.ready_to_write()
        self.loop.call_soon(self.process_buffers)

    def read(self):
        data = bytes(self._incoming_buffer)
        del self._incoming_buffer[:]
        return data

    def write(self, data):
        self._outgoing_buffer.extend(data)

    def data_received(self):
        self._incoming_buffer += self._serial_device.read()

    def ready_to_write(self):
        result = self._serial_device.write(bytes(self._outgoing_buffer))
        del self._outgoing_buffer[:]

    @asyncio.coroutine
    def close(self):
        self._serial_device.close()
        self._serial_device = None


class SelectSerial:
    """
    Only works on unix/linux...no windows!
    ...and no way to make it work either :(
    """

    def __init__(self, *, loop=None, port='/dev/ttyACM0', speed=57600):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

        self._incoming_buffer = bytearray()
        self._outgoing_buffer = bytearray()
        self._serial_device = serial.Serial(port, speed, timeout=0)

        loop.add_reader(self._serial_device, self.data_received)
        # loop.add_writer(self._serial_device, self.ready_to_write)

    def read(self):
        data = bytes(self._incoming_buffer)
        del self._incoming_buffer[:]
        return data

    def write(self, data):
        self._outgoing_buffer.extend(data)

    def data_received(self):
        self._incoming_buffer += self._serial_device.read()

    def ready_to_write(self, data):
        result = self._serial_device.write(self._outgoing_buffer)
        del self._outgoing_buffer[:]

    @asyncio.coroutine
    def close(self):
        loop = self.loop
        if loop is None:
            loop = asyncio.get_event_loop()

        loop.remove_reader(self._serial_device)
        # loop.remove_writer(self._serial_device)

        self._serial_device.close()
        self._serial_device = None
