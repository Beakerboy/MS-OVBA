import struct
from typing import Any, TypeVar


T = TypeVar('T', bound='PackedData')


class PackedData():
    """
    Multivalue field with a packing format
    """
    def __init__(self: T, format: str, *values: Any) -> None:
        self.values = values
        self.format = format

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        return struct.pack(endien_symbol + self.format, *self.values)
