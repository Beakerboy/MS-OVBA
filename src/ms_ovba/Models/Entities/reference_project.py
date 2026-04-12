import struct
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.project_reference import ProjectReference
from typing import TypeVar


T = TypeVar('T', bound='ReferenceProject')


class ReferenceProject(ReferenceRecord):

    def __init__(self: T, ref: ProjectReference) -> None:
        self._ref = ref

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        endien_symbol = '<' if endien == 'little' else '>'
        lib_rel = self._ref.relative()
        libid_abs_size = len(self._ref)
        libid_rel_size = len(lib_rel)
        format = (endien_symbol + "HII" + str(libid_abs_size) + "sI" +
                  str(libid_rel_size) + "sIH")
        ref_str = str(self._ref).encode(cp_name)
        ref_str_rel = str(lib_rel).encode(cp_name)
        return struct.pack(format, 0x000E,
                           libid_abs_size + libid_rel_size + 14,
                           libid_abs_size, ref_str, libid_rel_size,
                           ref_str_rel, 0x65BE0257, 0x0017)
