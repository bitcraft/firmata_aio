import asyncio

from firmata_aio.board import Board
from firmata_aio.async_serial import AsyncSerial


@asyncio.coroutine
def func(*args):
    pin = 6

    # this sleep needs to be refactored into the board
    yield from asyncio.sleep(4)
    board.set_pin_mode(pin, 1)
    for i in range(5):
        board.digital_write(pin, 1)
        yield from asyncio.sleep(.1)
        board.digital_write(pin, 0)
        yield from asyncio.sleep(.1)


if __name__ == '__main__':
    serial_device = AsyncSerial(port='COM4')
    board = Board(serial_device)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())
