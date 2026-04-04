from __future__ import annotations
import struct
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRecord')


class ReferenceRecord:

    def pack(self: T, endien: str, cp_name: str) -> bytes:
        return b''

    @staticmethod
    def unpack(bytestring: bytes, endien: str) -> ReferenceRecord:
        from ms_ovba.Models.Entities.reference_control import ReferenceControl
        from ms_ovba.Models.Entities.reference_project import ReferenceProject
        from ms_ovba.Models.Entities.reference_registered import (
            ReferenceRegistered
        )
        from ms_ovba.Models.Entities.reference_original import (
            ReferenceOriginal
        )
        endien_symbol = '<' if endien == 'little' else '>'
        id = struct.unpack(f"{endien_symbol}H", bytestring)
        ref: ReferenceRecord
        if id == 0x000D:
            ref = ReferenceRegistered.unpack(bytestring, endien)
        elif id == 0x000E:
            ref = ReferenceProject.unpack(bytestring, endien)
        elif id == 0x002F:
            ref = ReferenceControl.unpack(bytestring, endien)
        elif id == 0x0033:
            ref = ReferenceOriginal.unpack(bytestring, endien)
        else:
            raise Exception("Unknown Reference Type")
        return ref
