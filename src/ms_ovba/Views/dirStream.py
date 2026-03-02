import struct
from ms_ovba_compression.ms_ovba import MsOvba
from ms_ovba.vbaProject import VbaProject
from ms_ovba.Models.Fields.idSizeField import IdSizeField
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from ms_ovba.Models.Fields.packed_data import PackedData
from typing import List, TypeVar


T = TypeVar('T', bound='DirStream')


class DirStream():
    """
    The dir stream is compressed on write
    """

    def __init__(self: T, project: VbaProject) -> None:
        self.project = project
        self._include_compat = False

    def to_bytes(self: T) -> bytes:
        information = self._load_information()
        endien = self.project.endien
        cp_name = self.project.get_codepage_name()
        pack_symbol = '<' if endien == 'little' else '>'
        # should be 0xFFFF
        cookie_value = self.project.get_project_cookie()
        self.project_cookie = IdSizeField(19, 2, cookie_value)
        references = self.project.references
        modules = self.project.modules
        output = b''
        for record in information:
            output += record.pack(endien, cp_name)
        for record in references:
            output += record.pack(endien, cp_name)

        modules_header = IdSizeField(0x000F, 2, len(modules))

        output += (modules_header.pack(cp_name, endien)
                   + self.project_cookie.pack(cp_name, endien))
        for record in modules:
            output += record.pack(cp_name, endien)
        output += struct.pack(pack_symbol + "HI", 16, 0)
        return output

    def include_compat(self: T) -> None:
        self._include_compat = True

    def write_file(self: T) -> None:
        bin_f = open("dir.bin", "wb")
        ms_ovba = MsOvba()
        compressed = ms_ovba.compress(self.to_bytes())
        bin_f.write(compressed)
        bin_f.close()

    def _load_information(self: T) -> List:
        codepage = 0x04E4
        # 0=16bit, 1=32bit, 2=mac, 3=64bit
        syskind = IdSizeField(1, 4, 3)
        compat_version = IdSizeField(74, 4, 3)
        lcid = IdSizeField(2, 4, 0x0409)
        lcid_invoke = IdSizeField(20, 4, 0x0409)
        codepage_record = IdSizeField(3, 2, codepage)
        project_name = IdSizeField(4, 10, "VBAProject")
        docstring = DoubleEncodedString([5, 0x0040], "")
        helpfile = DoubleEncodedString([6, 0x003D], "")
        help_context = IdSizeField(7, 4, 0)
        lib_flags = IdSizeField(8, 4, 0)
        version = IdSizeField(9, 4, 0x65BE0257)
        minor_version = PackedData("H", 17)
        constants = DoubleEncodedString([12, 0x003C], "")

        information = [syskind]
        if self._include_compat:
            information.append(compat_version)
        information.extend([
            lcid,
            lcid_invoke,
            codepage_record,
            project_name,
            docstring,
            helpfile,
            help_context,
            lib_flags,
            version,
            minor_version,
            constants
        ])
        return information
