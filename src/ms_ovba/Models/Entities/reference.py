from __future__ import annotations
import struct
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from typing import TypeVar


T = TypeVar('T', bound='Reference')


class Reference():
    """
    2.3.4.2.2.1 REFERENCE Record
    """
    def __init__(self: T, ref: ReferenceRecord,
                 name: str = '') -> None:
        self._ref = ref
        self._refname = name

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        name_pack = b''
        if self._refname is not None:
            name_de = DoubleEncodedString([0x0016, 0x003E], self._refname)
            name_pack = name_de.pack(endien, cp_name)

        return name_pack + self._ref.pack(endien, cp_name)

    @staticmethod
    def unpack(data: bytes, endien: str) -> Reference:
        endien_symbol = '<' if endien == 'little' else '>'
        name = ''
        offset = 0
        id = struct.unpack_from(endien_symbol + "H", data, offset)
        if id == 0x0016:
            offset += 2
            size1, = struct.unpack_from(endien_symbol + "I", data, offset)
            offset += 4
            format = endien_symbol + size1 + "s"
            name = struct.unpack_from(format, data, offset)
            offset += size1
            size2 = struct.unpack_from(endien_symbol + "I", data, offset)
            offset += 4
            if size2 != size1 * 2:
                # raise warning
                pass
            # format = endien_symbol + size2 + "s"
            # name2 = struct.unpack_from(format, data, offset)
            offset += size2
            # if name2 != unicode version on name1:
            #     raise warning

        bytestring = data[offset:]
        ref = ReferenceRecord.unpack(bytestring, endien)
        return Reference("cp", ref, name)
