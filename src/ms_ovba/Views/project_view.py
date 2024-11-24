import struct
from vbaproject_compiler.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='ProjectView')


class ProjectView:
    """
    The _VBA_PROJECT data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self.project = project
        self._reserved3 = 0x0003

    def set_reserved3(self: T, value: int) -> None:
        self._reserved3 = value

    def to_bytes(self: T) -> bytes:
        endien_symbol = '<' if self.project.endien == 'little' else '>'
        format = endien_symbol + "HHBH"
        output = b''
        reserved1 = 0x61CC
        reserved2 = 0x00
        cache_version = self.project.get_performance_cache_version()

        output += struct.pack(format, reserved1, cache_version,
                              reserved2, self._reserved3)
        return output + self.project.get_performance_cache()

    def write_file(self: T) -> None:
        bin_f = open("vba_project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
