import io
import struct
from typing import TypeVar


T = TypeVar('T', bound='StructIO')


class StructIO:

    def __init__(self: T, data: bytes, endian: str = 'little') -> None:
        self._stream = io.BytesIO(data)
        self._sym = '<' if endian == 'little' else '>'

    def read_big_h(self: T) -> int:
        val, = self._read_fmt('H', 2)
        return val

    def read_big_i(self: T) -> int:
        val, = self._read_fmt('I', 4)
        return val

    def read_id_size_val(self: T) -> tuple[int, int, bytes]:
        id, size = self._read_fmt('HI', 6)
        val = self._stream.read(size)
        return (id, size, val)

    def _read_fmt(self: T, fmt: str, size: int) -> tuple:
        """Helper to read exactly 'size' bytes and unpack them."""
        chunk = self._stream.read(size)
        if len(chunk) < size:
            raise EOFError(f"Expected {size} bytes, but only got {len(chunk)}")
        return struct.unpack(f"{self._sym}{fmt}", chunk)
