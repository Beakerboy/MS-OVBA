from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from ms_ovba.Models.Fields.project_reference import ProjectReference
from ms_ovba.Models.Fields.packed_data import PackedData
from typing import TypeVar


T = TypeVar('T', bound='ReferenceProject')


class ReferenceProject():

    def __init__(self: T, codepage_name: str,
                 ref: ProjectReference) -> None:
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._ref = ref

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        size_of_libid_absolute = len(self._ref)
        size_of_libid_relative = len(self._ref.relative_to(""))
        format = "HII" + str(size_of_libid_absolute) + "sI" + str(size_of_libid_relative) + "sIH"
        ref_str = str(self._ref).encode(self._codepage_name)
        ref_str_rel = str(self._ref.relative_to("")).encode(self._codepage_name)
        ref_project = PackedData(format, 0x000E, size_of_libid_absolute + size_of_libid_relative + 20,
                                    size_of_libid_absolute, ref_str, size_of_libid_relative, ref_str_rel, 0x65BE0257, 0x0017)

        return (ref_project.pack(codepage_name, endien))
