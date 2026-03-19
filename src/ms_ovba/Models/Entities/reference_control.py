import struct
import uuid
from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.libid_reference import LibidReference
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from typing import TypeVar


T = TypeVar('T', bound='ReferenceControl')


class ReferenceControl(ReferenceRecord):
    """
    2.3.4.2.2.3 REFERENCECONTROL Record
    """
    def __init__(self: T, ref: LibidReference,
                 ref2: LibidReference,
                 guid: uuid.UUID, cookie: int,
                 name: str = None) -> None:
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
            ref2_str + b'\00' * 6 + self._guid.bytes +
            struct.pack(endien_symbol + "I", self._cookie)
        )

    @staticmethod
    def unpack(data: bytes, endien: str) -> T:
        endien_symbol = '<' if endien == 'little' else '>'
        offset = 0
        id, size_twiddled, size_of_libid_twiddled = (
            struct.unpack_from(endien_symbol + "HII", data, offset)
        )
        offset += 10
        if id != 0x002F:
            msg = "Incorrect id in data. Received " + id + ", expected 0x002F"
            raise ValueError(msg)
        if size_twiddled != size_of_libid_twiddled + 10:
            pass

        libid_twid_bytes = data[offset:offset + size_of_libid_twiddled]
        libid_twid = LibidReference.unpack(libid_twid_bytes)
        offset += size_of_libid_twiddled
        zero1, zero2, id = (
            struct.unpack_from(endien_symbol + "IHH", data, offset)
        )
        if zero1 != 0 or zero2 != 0:
            pass
        offset += 8
        if id == 0x16:
            # ReferenceName Record
            name_size, = struct.unpack_from(endien_symbol + "I", data, offset)
            offset += 4
            name = data[offset:offset + name_size].decode('ascii')
            offset += name_size
            # Verify Reserved is 0x3e
            offset += 2
            # Read size1
            offset += 4
            # Verify size1 = 2 * size
            # Read Name1
            offset += name_size * 2
            # Verify name2 is unicode version of name
            id, = struct.unpack_from(endien_symbol + "H", data, offset)
            offset += 2
        else:
            name = None
        if id != 0x30:
            # Unknown Data
            pass
        size_ext, size_of_libid_ext = (
            struct.unpack_from(endien_symbol + "II", data, offset)
        )
        offset += 8
        if size_ext != size_of_libid_ext + 30:
            pass
        libid_ext_bytes = data[offset:offset + size_of_libid_ext]
        libid_ext = LibidReference.unpack(libid_ext_bytes)
        offset += size_of_libid_ext
        zero1, zero2 = struct.unpack_from(endien_symbol + "IH", data, offset)
        if zero1 != 0 or zero2 != 0:
            pass
        offset += 6
        original_type_lib_bytes = data[offset:offset + 16]
        guid = uuid.UUID(bytes=original_type_lib_bytes)
        offset += 16
        cookie = struct.unpack_from(endien_symbol + "I", data, offset)
        offset += 4
        if len(data) != offset
            pass
        return ReferenceControl(libid_twid, libid_ext, guid, cookie, name)
