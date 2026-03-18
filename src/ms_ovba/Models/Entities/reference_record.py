import struct
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRecord')


class ReferenceRecord:

    @staticmethod
    def unpack(bytestring: bytes, endien: str) -> T:
        from ms_ovba.Models.Entities.reference_control import ReferenceControl
        from ms_ovba.Models.Entities.reference_project import ReferenceProject
        from ms_ovba.Models.Entities.reference_registered import (
            ReferenceRegistered
        )
        endien_symbol = '<' if endien == 'little' else '>'
        id = struct.unpack(endien_symbol + "H", bytestring)
        if id == 0x000D:
            ref = ReferenceRegistered.unpack(bytestring, endien)
        elif id == 0x000E:
            ref = ReferenceProject.unpack(bytestring, endien)
        elif id == 0x002F:
            # ref = ReferenceControl.unpack(bytestring, endien)
            pass
        elif id == 0x0033:
            # ref = ReferenceOriginal.unpack(bytestring, endien)
            pass
        else:
            # raise warning
            return None
        return ref
