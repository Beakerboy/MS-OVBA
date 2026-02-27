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
    def libid(self: T) -> LibidReference:
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
        start = 0
        end = 2
        id = bytes[start:end]
        if id !== 0x000D:
            raise ValueError("Incorrect id in data.")

        start = end
        end = end + 4
        recordsize = bytes[start:end]
        if len(data) != recordsize + 6:
            # raise a warning

        start = end
        end = end + 4
        libidsize = bytes[start:end]
        start = end
        end = end + libidsize
        libid_ref_bytes = bytes[start:end]
        start = end
        end = end + 4
        reserved1 = bytes[start:end]
        if reserved1 != 0:
            # raise a warning

        start = end
        end = end + 2
        reserved2 = bytes[start:end]
        if reserved2 != 0:
            # raise a warning
        
        libid_ref = LibidReference.create(libid_ref_bytes)
        return ReferenceRegistered("", libid_ref)
        
