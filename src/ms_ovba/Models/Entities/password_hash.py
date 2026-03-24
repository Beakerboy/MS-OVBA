from typing import TypeVar


T = TypeVar('T', bound='PasswordHash)')


class PasswordHash:
    def __init__(self, password: str) -> None:
        self._password = password

    def to_bytes(self: T) -> bytes:
        grbit = struct.pack(">I", GrbitKey | GrbitHashNull)[1:]
        key_no_nulls = self._remove_nulls(self._key)
        output = b'\xff' + grbit

    def _remove_nulls(self: T) -> bytes:
        pass
