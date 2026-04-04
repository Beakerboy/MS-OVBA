import struct
import warnings
from ms_ovba_compression.ms_ovba import MsOvba
from ms_ovba.vbaProject import VbaProject
from ms_ovba.Models.Entities.reference import Reference
from ms_ovba.Models.Fields.idSizeField import IdSizeField
from ms_ovba.Models.Fields.doubleEncodedString import (
    DoubleEncodedString
)
from ms_ovba.Models.Fields.packed_data import PackedData
from typing import List, TypedDict, TypeVar


T = TypeVar('T', bound='DirStream')


PackableData = DoubleEncodedString | IdSizeField | PackedData


class Parameters(TypedDict):
    references: list[Reference]
    modules: list
    help_context_id: int
    project_cookie: int
    codepage_name: str


class DirStream():
    """
    The dir stream is compressed on write
    """

    def __init__(self: T, project: VbaProject) -> None:
        self._project = project
        self._include_compat = project.compat

    def to_bytes(self: T) -> bytes:
        information = self._load_information()
        endien = self._project.endien
        cp_name = self._project.codepage_name
        pack_symbol = '<' if endien == 'little' else '>'
        # should be 0xFFFF
        cookie_value = self._project.project_cookie
        self.project_cookie = IdSizeField(19, 2, cookie_value)
        references = self._project.references
        modules = self._project.modules
        output = b''
        for record in information:
            output += record.pack(endien, cp_name)
        for record in references:
            output += record.pack(endien, cp_name)

        modules_header = IdSizeField(0x000F, 2, len(modules))

        output += (modules_header.pack(endien)
                   + self.project_cookie.pack(endien))
        for record in modules:
            output += record.pack(endien, cp_name)
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
        help_context = IdSizeField(7, 4, self._project.help_context_id)
        lib_flags = IdSizeField(8, 4, 0)
        version = IdSizeField(9, 4, 0x65BE0257)
        minor_version = PackedData("H", 17)
        constants = DoubleEncodedString([12, 0x003C], "")

        information: list[PackableData] = [syskind]
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

    @staticmethod
    def is_valid(data: bytes) -> bool:
        try:
            DirStream.from_bytes(data)
        except Exception as e:
            warnings.warn(str(e), SyntaxWarning)
            return False
        return True

    @staticmethod
    def from_bytes(data: bytes) -> Parameters:
        """
        Static validation: Checks if bytes follow the DirStream structure.
        Expects decompressed bytes.
        """
        project_data: Parameters = {
            "references": [],
            "modules": [],
            "help_context_id": 0,
            "project_cookie": 0,
            "codepage_name": "cp1252"
        }
        offset = 0

        # 1. Check PROJECTSYSKIND (Mandatory first record)
        # IdSizeField(1, 4, 3) -> ID=1 (2 bytes), Size=4 (4 bytes)
        record_id, size, value = struct.unpack_from("<HII", data, offset)
        if record_id != 1 or size != 4 or not (0 <= value <= 3):
            raise ValueError("Incorrect PROJECTSYSKIND")
        offset += 10

        record_id, size, value = struct.unpack_from("<HII", data, offset)
        if record_id == 0x4A:
            if size != 4:
                raise ValueError("Incorrect PROJECTCOMPATVERSION")
            offset += 10
            record_id, size, value = (struct.unpack_from("<HII", data, offset))
        if record_id != 2 or size != 4 or value != 0x409:
            raise ValueError("Incorrect PROJECTLCID")
        offset += 10

        record_id, size, value = struct.unpack_from("<HII", data, offset)
        if record_id != 0x14 or size != 4 or value != 0x409:
            raise ValueError("Incorrect PROJECTLCIDINVOKE")
        offset += 10

        record_id, size, value = struct.unpack_from("<HIH", data, offset)
        if record_id != 3 or size != 2:
            raise ValueError("Incorrect PROJECTCODEPAGE")
        offset += 8

        record_id, size = struct.unpack_from("<HI", data, offset)
        value, = struct.unpack_from(f"{size}s", data, offset + 6)
        if record_id != 4 or not (1 <= size <= 128):
            raise ValueError("Incorrect PROJECTNAME")
        offset += 6 + size

        record_id, size = struct.unpack_from("<HI", data, offset)
        value, r2, s2, v2 = struct.unpack_from(
            f"<{size}sHI{2*size}s", data, offset + 6)
        if record_id != 5 or size > 2000 or s2 != 2 * size:
            raise ValueError(
                f"Incorrect PROJECTDOCSTRING({record_id}, {size}, {r2}, {s2})")
        offset += 12 + size * 3

        record_id, size = struct.unpack_from("<HI", data, offset)
        value, r2, s2, v2 = struct.unpack_from(
            f"<{size}sHI{size}s", data, offset + 6)
        if record_id != 6 or size > 260 or s2 != size or value != v2:
            raise ValueError(
                f"Incorrect PROJECTHELPFILEPATH({record_id}, {size}, {s2})")
        offset += 12 + size * 2

        record_id, size, value = struct.unpack_from("<HII", data, offset)
        if record_id != 7 or size != 4:
            raise ValueError("Incorrect PROJECTHELPCONTEXT")
        offset += 10

        record_id, size, value = struct.unpack_from("<HII", data, offset)
        if record_id != 8 or size != 4 or value != 0:
            raise ValueError("Incorrect PROJECTLIBFLAGS")
        offset += 10

        record_id, size, value, v2 = struct.unpack_from("<HIIH", data, offset)
        if record_id != 9:
            raise ValueError("Incorrect PROJECTVERSION")
        offset += 12

        record_id, size = struct.unpack_from("<HI", data, offset)
        value, r2, s2, v2 = struct.unpack_from(
            f"<{size}sHI{size}s", data, offset + 6)
        if record_id != 0x0c or size > 2015 or s2 != 2 * size:
            raise ValueError("Incorrect PROJECTCONSTANTS")
        offset += 12 + size * 3

        record_id, size = struct.unpack_from("<HI", data, offset)
        found_one_reference = False
        while (record_id != 0x0f or not found_one_reference):
            found_one_reference = True
            record_size = 0
            if record_id == 0x16:
                record_size = 12 + size * 3
                record_id, size = struct.unpack_from(
                    "<HI", data, offset + record_size)
            match record_id:
                case 0x2f:
                    record_size += 6 + size
                    record_id, size = struct.unpack_from(
                        "<HI", data, offset + record_size)
                    if record_id == 0x16:
                        record_size = 12 + size * 3
                    record_id, size = struct.unpack_from(
                        "<HI", data, offset + record_size)
                    record_size += 6 + size
                case 0x33:
                    record_size += 6 + size
                    record_id, size = struct.unpack_from(
                        "<HI", data, offset + record_size)
                    record_size += 6 + size
                    record_id, size = struct.unpack_from(
                        "<HI", data, offset + record_size)
                    if record_id == 0x16:
                        record_size = 12 + size * 3
                        record_id, size = struct.unpack_from(
                            "<HI", data, offset + record_size)
                        record_size += 6 + size
                case 0x0d | 0x0e:
                    record_size += 6 + size
                case _:
                    raise ValueError(f"Unknown Reference Type: {record_id}")
            ref = Reference.unpack(
                data[offset:offset + record_size], "little")
            project_data["references"] += [ref]
            offset += record_size
            record_id, size = struct.unpack_from("<HI", data, offset)

        if record_id != 0x0f or size != 2:
            raise ValueError("Expected ModuleRecord")
        offset += 6
        count, record_id, size, cookie = struct.unpack_from(
            "<HHIH", data, offset)
        if record_id != 0x13 or size != 2:
            raise ValueError(f"Incorrect PROJECTCOOKIE({record_id}, {size})")
        project_data["project_cookie"] = cookie
        for _ in range(count):
            module_data = {}
            record_size = 0
            record_id, size = struct.unpack_from("<HI", data, offset)
            record_size += 6
            value, r2, s2, v2 = struct.unpack_from(
                f"<{size}sHI{size*2}s", data, offset + record_size)
            record_size += size * 3 + 6
            # validate sizes and that values match
            module_data["name"] = value
            record_id, size = struct.unpack_from(
                f"<{size}sHI", data, offset + record_size)
            record_size += 6
            value, record_id, size = struct.unpack_from(
                f"<{size}sHI", data, offset + record_size)
            module_data["stream_name"] = value
            record_size += size + 6
            value, record_id, size, value2 = struct.unpack_from(
                f"<{size}sHI{size*2}s", data, offset + record_size)
            module_data["docstring"] = value
            record_size += size * 3 + 6
            record_id, size, value = struct.unpack_from(
                "<HII", data, offset + record_size)
            if record_id != 0x31 or size != 4:
                raise ValueError("Incorrect MODULEOFFSET")
            offset += 10
            record_id, size, value = struct.unpack_from(
                "<HII", data, offset + record_size)
            if record_id != 0x1e or size != 4:
                raise ValueError("Incorrect MODULEHELPCONTEXT")
            offset += 10
            record_id, size, value = struct.unpack_from(
                "<HIH", data, offset + record_size)
            if record_id != 0x1e or size != 2:
                raise ValueError("Incorrect MODULEHELPCONTEXT")
            offset += 8
            project_data["modules"] += [module_data]
            offset += record_size
        return project_data

    @staticmethod
    def is_file_valid(file_path: str) -> bool:
        """Helper to validate a compressed .bin file on disk."""
        try:
            with open(file_path, "rb") as f:
                compressed = f.read()
            from ms_ovba_compression.ms_ovba import MsOvba
            decompressed = MsOvba().decompress(compressed)
            return DirStream.is_valid(decompressed)
        except Exception:
            return False
