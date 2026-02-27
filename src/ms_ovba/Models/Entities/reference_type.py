from typing import TypeVar


T = TypeVar('T', bound='ReferenceType')


class ReferenceType:

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        return b''
