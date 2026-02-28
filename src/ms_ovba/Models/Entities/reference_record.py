import struct
from typing import TypeVar


T = TypeVar('T', bound='ReferenceRecord')


class ReferenceRecord:

    @staticmethod
    def unpack(bytestring: bytes, endien: str) -> T:
        endien_symbol = '<' if endien == 'little' else '>'
        id = struct.unpack(endien_symbol + "H", bytestring)
        if id == 0x000D:
            ref = ReferenceRegistered.unpack(bytestring, endien)
        else if id == 0x000E:
            ref = ReferenceProject.unpack(bytestring, endien)
        else if id == 0x002F:
            ref = ReferenceControl.unpack(bytestring, endien)
        else if id == 0x0033:
            ref = ReferenceOriginal.unpack(bytestring, endien)
        else:
            # raise warning
            return None
        return ref
