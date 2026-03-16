import struct
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.project_reference import ProjectReference
from typing import TypeVar


T = TypeVar('T', bound='ReferenceControl')


class ReferenceControl(ReferenceRecord):
    """
    2.3.4.2.2.3 REFERENCECONTROL Record
    """
    def __init__(self: T, ref: ProjectReference, name: str = None) -> None:
        self._libid_twiddled = ref
        name_record_extended = name

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        ref_str = str(self._libid_twiddled).encode(cp_name)
        size_of_libid_twiddled = len(ref_str)
        size_twiddled = 10 + size_of_libid_twiddled
        endien_symbol = '<' if endien == 'little' else '>'
        format = (
            endien_symbol + "HII" + str(size_of_libid_twiddled) +
            "sIH" + str(libid_rel_size) + "sIH")
        
        return struct.pack(
            format, 0x2F, size_twiddled, size_of_libid_twiddled
                           ref_str, 0, 0, ref_str_rel, 0x30, 0x0017)
