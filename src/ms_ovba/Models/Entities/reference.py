from ms_ovba.Models.Entities.reference_type import ReferenceType
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
                 ref: ReferenceType,
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
