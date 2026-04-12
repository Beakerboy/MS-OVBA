from __future__ import annotations
import struct
from ms_ovba.Models.Entities.reference_control import ReferenceControl
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.libid_reference import LibidReference
from typing import TypeVar


T = TypeVar('T', bound='ReferenceOriginal')


class ReferenceOriginal(ReferenceRecord):
    """
    2.3.4.2.2.5
    Specifies a reference to an Automation type library.
    """
    def __init__(self: T,
                 libid_ref: LibidReference,
                 ref_cntl: ReferenceControl) -> None:
        self._libid_ref = libid_ref
        self._ref_cntl = ref_cntl

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        strlen = len(self._libid_ref)
        format = endien_symbol + "HI"
        lib_str = str(self._libid_ref).encode(cp_name)
        ref_str = self._ref_cntl.pack(endien, cp_name)
        return struct.pack(format, 0x0033, strlen) + lib_str + ref_str

    @staticmethod
    def unpack(data: bytes, endien: str) -> ReferenceOriginal:
        endien_symbol = '<' if endien == 'little' else '>'
        offset = 0
        id, = struct.unpack_from(endien_symbol + "H", data, offset)
        offset += 2
        if id != 0x33:
            msg = "Incorrect id in data. Received " + id + ", expected 0x0033"
            raise ValueError(msg)

        format = endien_symbol + "I"
        libidsize, = struct.unpack_from(format, data, offset)
        offset += 4

        libid_ref_bytes = data[offset:offset + libidsize]
        offset += libidsize

        ref_cntl = ReferenceControl.unpack(data[offset:], endien)

        libid_ref = LibidReference.unpack(libid_ref_bytes)
        return ReferenceOriginal(libid_ref, ref_cntl)
