import struct
from typing import Any, TypeVar


T = TypeVar('T', bound='IdSizeField')


class IdSizeField():
    """
    Many Records have the same format, a two bye ID, a four byte size and an
    int value formatted to the defined size.
    """

    def __init__(self: T, id: int, size: int, value: Any) -> None:
        self._id = id
        self._size = size
        self._value = value

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        format = endien_symbol + "HI"
        if isinstance(self._value, str):
            self.stringValue = self._value
            self._value = bytes(self._value, encoding="ascii")
            format += str(self._size) + "s"
        elif isinstance(self._value, bytes):
            format += str(self._size) + "s"
        elif self._size == 2:
            format += "H"
        elif self._size == 4:
            format += "I"
        else:
            msg = "Received data of type " + type(self._value).__name__
            raise Exception(msg)
        return struct.pack(format, self._id, self._size, self._value)
