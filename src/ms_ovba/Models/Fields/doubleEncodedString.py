from ms_ovba.Models.Fields.idSizeField import IdSizeField
from typing import TypeVar


T = TypeVar('T', bound='DoubleEncodedString')


class DoubleEncodedString():
    """
    A union of two IdSizeFields
    The strings are encoded differently in each.
    """
    def __init__(self: T, ids: list, text: str) -> None:
        self.ids = ids
        self._value = text

    @property
    def value(self: T) -> str:
        return self._value

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        encoded = self._value.encode(cp_name)
        self.mod_name1 = IdSizeField(self.ids[0], len(encoded), encoded)
        format = "utf_16_le" if endien == 'little' else "utf_16_be"
        encoded = self._value.encode(format)
        self.mod_name2 = IdSizeField(self.ids[1], len(encoded), encoded)
        return (self.mod_name1.pack(endien)
                + self.mod_name2.pack(endien))
