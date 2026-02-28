from ms_ovba.Models.Entities.reference_record import ReferenceRecord
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from typing import TypeVar


T = TypeVar('T', bound='Reference')


class Reference():
    """
    2.3.4.2.2.1 REFERENCE Record
    """
    def __init__(self: T, codepage_name: str,
                 ref: ReferenceRecord,
                 name: str = None) -> None:
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._ref = ref
        self._refname = name

    def pack(self: T, cp_name: str, endien: str) -> bytes:
        name_pack = b''
        if self._refname is not None:
            name_de = DoubleEncodedString([0x0016, 0x003E], self._refname)
            name_pack = name_de.pack(cp_name, endien)

        return name_pack + self._ref.pack(cp_name, endien)

    @staticmethod
    def unpack(data: bytes, endien: str) -> T:
        # name = None
        # Read 2 bytes into id
        # if id == 0x0016:
        #     Read 4 bytes into size1
        #     Read size1 bytes into name
        #     Read 4 bytes into size2
        #     if size2 != size1 * 2:
        #         raise warning
        #     read size2 bytes into name2
        #     if name2 != unicode version on name1:
        #         raise warning
        #     read 2 bytes into id
        #
        # if id == 0x0000D:
        #     ref = ReferenceRegistered.unpack(bytestring, endien)
        # else if id == 0x0000E:
        #     ref = ReferenceProject.unpack(bytestring, endien)
        # else if id == 0x0002F:
        #     ref = ReferenceControl.unpack(bytestring, endien)
        # else if id == 0x00033:
        #     ref = ReferenceOriginal.unpack(bytestring, endien)
        # else:
        #     raise warning
        #     return None
        # return Record("cp", ref, name)
        pass
        
        
        
        
        
