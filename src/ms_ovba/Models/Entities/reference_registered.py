from ms_ovba.Models.Entities.reference_type import ReferenceType
from ms_ovba.Models.Fields.libid_reference import LibidReference
from ms_ovba.Models.Fields.packed_data import PackedData
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRegistered')


class ReferenceRegistered(ReferenceType):
    """
    2.3.4.2.2.5
    Specifies a reference to an Automation type library.
    """
    def __init__(self: T, codepage_name: str,
                 libid_ref: LibidReference) -> None:
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._libid_ref = libid_ref

    @property
    def libid(self: T): LibidReference
        return self._libid_ref

    def pack(self: T, cp_name: str, endien: str) -> bytes:
        strlen = len(self._libid_ref)
        format = "HII" + str(strlen) + "sIH"
        lib_str = str(self._libid_ref).encode(cp_name)
        ref_registered = PackedData(format, 0x000D, strlen + 10,
                                    strlen, lib_str, 0, 0)

        return ref_registered.pack(cp_name, endien)

    @staticmethod
    def unpack(data: bytes) -> T:
        # Read two bytes into ID
        # if id !== 0x000D throw exception
        # Read 4 bytes into recordsize
        # If size(data) !== recordsize + 6 throw notice
        # Read 4 bytes into libidsize
        # Read libidsize bytes into libid_ref_bytes
        # Read 4 bytes into reserved1
        # If reserved1 !== 0 throw notice
        # Read 2 bytes into reserved2
        # If reserved2 !== 0 throw notice
        # libid_ref = LibidReference.create(libid_ref_bytes)
        # return ReferenceRegistered("", libid_ref)
        
