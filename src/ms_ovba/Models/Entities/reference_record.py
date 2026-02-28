from typing import TypeVar


T = TypeVar('T', bound='ReferenceRecord')


class ReferenceRecord:

    def pack(self: T, codepage_name: str, endien: str) -> bytes:
        return b''
