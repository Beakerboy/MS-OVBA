from vbaproject_compiler.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from vbaproject_compiler.Models.Fields.libid_reference import LibidReference
from vbaproject_compiler.Models.Fields.packed_data import PackedData
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRecord')


class ReferenceRecord():

    def __init__(self: T, codepage_name: str,
                 name: str, libid_ref: LibidReference) -> None:
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._refname = DoubleEncodedString([0x0016, 0x003E], name)
        self._libid_ref = libid_ref

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        strlen = len(self._libid_ref)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self._libid_ref).encode(self._codepage_name)
        ref_registered = PackedData(format, 0x000D, strlen + 10,
                                    strlen, lib_str, 0, 0)

        return (self._refname.pack(codepage_name, endien)
                + ref_registered.pack(codepage_name, endien))
