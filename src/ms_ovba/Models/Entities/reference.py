from ms_ovba.Models.Entities.reference_name import ReferenceName
from ms_ovba.Models.Entities.reference_type import ReferenceType
from typing import TypeVar


T = TypeVar('T', bound='Reference')


class Reference():
    """
    2.3.4.2.2.1 REFERENCE Record
    """
    def __init__(self: T, codepage_name: str,
                 ref: ReferenceType, name: ReferenceName = None) -> None:
        # is self._codepage_name even needed?
        self._codepage_name = codepage_name
        self._ref = ref
        self._name = name

    def pack(self: T, cp_name: str, endien: str) -> bytes:
        name = self._name
        pack_name = name.pack(cp_name, endien) if is not name is None else ""
        return pack_name + self._ref.pack(cp_name, endien)
