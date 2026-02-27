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
        cp_name = self._codepage_name
        libid_abs_size = len(self._ref)
        libid_rel_size = len(self._ref.relative_to(""))
        format = ("HII" + str(libid_abs_size) + "sI" +
                  str(libid_rel_size) + "sIH")
        ref_str = str(self._ref).encode(cp_name)
        ref_str_rel = str(self._ref.relative_to("")).encode(cp_name)
        ref_project = PackedData(format, 0x000E,
                                 libid_abs_size + libid_rel_size + 20,
                                 libid_abs_size, ref_str, libid_rel_size, 
                                 ref_str_rel, 0x65BE0257, 0x0017)

        return (ref_project.pack(cp_name, endien))
