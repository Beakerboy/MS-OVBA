import struct
import uuid
from typing import TypeVar


T = TypeVar('T', bound='LicenseInfo')


class LicenseInfo:
    def __init__(self: T, guid: uuid.UUID, key: bytes) -> None:
        self._guid = guid
        self._key = key
        self._required = len(key) > 0

    def not_required(self: T) -> None:
        self._required = False

    def to_bytes(self: T) -> bytes:
        return (
            self._guid.bytes +
            struct.pack("<I", len(self._key)) +
            self._key +
            struct.pack("<I", 1 if self._required else 0)
        )
