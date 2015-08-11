"""
Provide Factory class to generate and parse packet data
"""
from .commands import nibble_commands, byte_commands, sysex_commands
from .commands import command_names, command_lookup


class UnhandledPacketType(Exception):
    pass


class Container(dict):
    """
    A generic container of attributes.
    Containers are the common way to express parsed data.
    """
    __slots__ = ["__keys_order__"]

    def __init__(self, **kw):
        object.__setattr__(self, "__keys_order__", [])
        for k, v in list(kw.items()):
            self[k] = v

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setitem__(self, key, val):
        if key not in self:
            self.__keys_order__.append(key)
        dict.__setitem__(self, key, val)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.__keys_order__.remove(key)

    __delattr__ = __delitem__
    __setattr__ = __setitem__

    def clear(self):
        dict.clear(self)
        del self.__keys_order__[:]

    def pop(self, key, *default):
        val = dict.pop(self, key, *default)
        self.__keys_order__.remove(key)
        return val

    def popitem(self):
        k, v = dict.popitem(self)
        self.__keys_order__.remove(k)
        return k, v

    def update(self, seq, **kw):

        if hasattr(seq, "keys"):
            for k in list(seq.keys()):
                self[k] = seq[k]
        else:
            for k, v in seq:
                self[k] = v
        dict.update(self, kw)

    def copy(self):
        inst = self.__class__()
        inst.update(iter(self.items()))
        return inst

    __update__ = update
    __copy__ = copy

    def __iter__(self):
        return iter(self.__keys_order__)

    iterkeys = __iter__

    def itervalues(self):
        return (self[k] for k in self.__keys_order__)

    def iteritems(self):
        return ((k, self[k]) for k in self.__keys_order__)

    def keys(self):
        return self.__keys_order__

    def values(self):
        return list(self.values())

    def items(self):
        return list(self.items())

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))


def mappp(list, dict):
    return [dict[i] for i in list]


def mapppp(values, sig):
    return {k: values[i] for i, k in enumerate(sig)}


def make_container(name, sig, values):
    return Container(name=name, **mapppp(values, sig))


# generator
def parse(handler):
    start_sysex = command_lookup['start_sysex']
    stop_sysex = command_lookup['stop_sysex']

    while 1:
        byte = yield

        nibble = byte & 0xF0
        if nibble in nibble_commands:
            name, sig = nibble_commands[nibble]
            value0 = byte & 0x0F
            if nibble in (0xD0, 0xC0):
                value1 = yield
                yield  # this byte doesn't matter
            else:
                lsb = yield
                msb = yield
                value1 = (msb << 7) + lsb
            c = make_container(name, sig, (value0, value1))
            handler(c)

        elif byte in byte_commands:
            if byte == start_sysex:
                msg = bytearray()
                byte = yield
                command = sysex_commands[byte]
                while 1:
                    byte = yield
                    if byte == stop_sysex:
                        break
                    msg.append(byte)
                handler(command, bytes(msg))

            elif byte in (0xF4, 0xF5, 0xF9):
                name, sig = byte_commands[byte]
                value0 = yield
                value1 = yield
                c = make_container(name, sig, (value0, value1))
                handler(c)

            else:
                raise UnhandledPacketType

        else:
            raise UnhandledPacketType


def build(name, **kwargs):
    command = command_lookup[name]
    name, sig = command_names[command]

    if command in nibble_commands:
        args = mappp(sig, kwargs)
        header = command + (args[0] & 0x0F)
        if command in (0xD0, 0xC0):
            return bytearray([header, args[1], 0x00])
        else:
            raise UnhandledPacketType

    elif command in byte_commands:
        pass

    elif command in sysex_commands:
        start_sysex = command_lookup['start_sysex']
        stop_sysex = command_lookup['stop_sysex']

        msg = bytearray()
        msg.append(start_sysex)
        msg.append(command)
        msg.append(stop_sysex)
        return msg

    else:
        raise Exception
