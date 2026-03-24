from typing import TypeVar


T = TypeVar('T', bound='PasswordHash')


class PasswordHash:
    def __init__(self, password: str) -> None:
        self._password = password
        # The top 4 bits only
        self._grbit_key = 0x000000
        # The low 20 bits
        self._grbit_hash_null = 0x000000

    def to_bytes(self: T) -> bytes:
        grbit = self._grbit_key | self._grbit_hash_null
        grbit_bytes = struct.pack(">I", grbit)[1:]
        key_no_nulls = self._remove_nulls(self._key)
        output = (
            b'\xff' + grbit_bytes + key_no_nulls +
            b'\x00'
        )
        return output

    def _remove_nulls(self: T) -> bytes:
        pass
