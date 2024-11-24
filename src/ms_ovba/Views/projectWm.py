from vbaproject_compiler.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='ProjectWm')


class ProjectWm:
    """
    The ProjectWM data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self.project = project

    def to_bytes(self: T) -> bytes:
        output = b''
        for module in self.project.modules:
            output += (bytes(module.modName.value, 'ascii')
                       + b'\x00'
                       + bytes(module.modName.value, 'utf_16_le')
                       + b'\x00\x00')
        output += b'\x00\x00'
        return output

    def write_file(self: T) -> None:
        bin_f = open("projectwm.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
