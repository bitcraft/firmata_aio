import asyncio

from firmata_aio.board import Board
from firmata_aio.async_serial import AsyncSerial


@asyncio.coroutine
def func(*args):
    pin = 2

    # this sleep needs to be refactored into the board
    yield from asyncio.sleep(4)

    # set board to digital input
    board.set_pin_mode(pin, 0)

    # enable pullup resistor
    board.send_packet('set_digital_pin_value', pin=pin, value=0)

    # enable reporting on this port
    board.send_packet('report_digital_port', port=0, value=1)

    # test pull resistor for button
    board.send_packet('pin_state_query')

    # yield from board.wait_for_command()
    yield from asyncio.sleep(10)
    print('ok!')


if __name__ == '__main__':
    serial_device = AsyncSerial()
    board = Board(serial_device)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
