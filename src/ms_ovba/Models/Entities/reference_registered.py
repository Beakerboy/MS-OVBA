import struct
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.libid_reference import LibidReference
from ms_ovba.Models.Fields.packed_data import PackedData
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRegistered')


class ReferenceRegistered(ReferenceRecord):
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
    def unpack(data: bytes, endien: str) -> T:
        endien_symbol = '<' if endien == 'little' else '>'
        offset = 0
        id, = struct.unpack_from(endien_symbol + "H", data, offset)
        offset += 2
        if id != 0x000D:
            msg = "Incorrect id in data. Received " + id + ", expected 0x000D"
            raise ValueError(msg)

        recordsize, = struct.unpack_from(endien_symbol + "I", data, offset)
        if len(data) != recordsize + 6:
            # raise a warning
            pass

        offset += 4
        libidsize, = struct.unpack_from(endien_symbol + "I", data, offset)
        offset += 4

        libid_ref_bytes = data[offset:offset + libidsize]
        offset += libidsize

        format = endien_symbol + "IH"
        reserved1, reserved2 = struct.unpack_from(format, data, offset)
        offset += 6

        if reserved1 != 0:
            # raise a warning
            pass

        if reserved2 != 0:
            # raise a warning
            pass

        libid_ref = LibidReference.create(libid_ref_bytes, endien)
        return ReferenceRegistered("", libid_ref)
