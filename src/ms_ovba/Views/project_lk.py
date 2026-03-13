import struct
from ms_ovba.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='ProjectLk')


class ProjectLk:
    """
    The ProjectLK data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self.project = project
        self._license_records = []

    def to_bytes(self: T) -> bytes:
        output = struct.pack("<HI", 1, len(project._license_records))
        for record in project._license_records:
            output += (
                struct.pack("<16sI", record.guid, len(record.key)) +
                record.key + steict.pack("<I", record.required)
            )
        return output

    def write_file(self: T) -> None:
        bin_f = open("projectlk.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()
