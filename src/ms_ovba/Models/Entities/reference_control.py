import struct
import uuid
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.project_reference import ProjectReference
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from typing import TypeVar


T = TypeVar('T', bound='ReferenceControl')


class ReferenceControl(ReferenceRecord):
    """
    2.3.4.2.2.3 REFERENCECONTROL Record
    """
    def __init__(self: T, ref: ProjectReference,
                 ref2: ProjectReference,
                 guid: uuid.UUID, cookie: int,
                 name: str = None,) -> None:
        self._libid_twiddled = ref
        self._libid_extended = ref2
        self._name_record_extended = name
        self._guid = guid
        self._cookie = cookie

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        ref_str = str(self._libid_twiddled).encode(cp_name)
        size_of_libid_twiddled = len(ref_str)
        size_twiddled = 10 + size_of_libid_twiddled
        ref2_str = str(self._libid_extended).encode(cp_name)
        size_of_libid_extended = len(ref2_str)
        size_extended = 30 + size_of_libid_extended
        name_pack = b''
        endien_symbol = '<' if endien == 'little' else '>'
        format = (
            endien_symbol + "HII" + str(size_of_libid_twiddled) +
            "sIH")
        if self._name_record_extended is not None:
            name_de = DoubleEncodedString([0x0016, 0x003E],
                                          self._name_record_extended)
            name_pack = name_de.pack(endien, cp_name)

        return (
            struct.pack(
                format, 0x2F, size_twiddled, size_of_libid_twiddled,
                ref_str, 0, 0
            ) + name_pack +
            struct.pack(
                endien_symbol + "HII", 0x30, size_extended,
                size_of_libid_extended
            ) +
            ref2_str +
            struct.pack(
                endien_symbol + "IH16sI", 0, 0,
                self._guid.bytes, self._cookie
            )
        )
