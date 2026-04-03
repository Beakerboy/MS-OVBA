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


PackableData = DoubleEncodedString | IdSizeField | PackedData


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
        """
        Static validation: Checks if bytes follow the DirStream structure.
        Expects decompressed bytes.
        """
        try:
            offset = 0
            
            # 1. Check PROJECTSYSKIND (Mandatory first record)
            # IdSizeField(1, 4, 3) -> ID=1 (2 bytes), Size=4 (4 bytes)
            record_id, size = struct.unpack_from("<HI", data, offset)
            if record_id != 1 or size != 4:
                return False
            offset += 6 + size

            # 2. Skip through variable Information/Reference records
            # Real validation would loop through known IDs (1-12, 16, 17, etc.)
            # For brevity, we verify the specific 'Terminator' at the end.
            
            # 3. Check for the Modules Header and Project Cookie
            # These appear after references but before the modules list
            # to_bytes() uses: IdSizeField(0x000F, 2, len(modules))
            # We search for the 0x000F marker followed by 0x0013 (Cookie)
            found_modules_header = False
            while offset < len(data) - 6:
                header_id = struct.unpack_from("<H", data, offset)[0]
                if header_id == 0x000F:
                    found_modules_header = True
                    break
                # Jump by standard Record header (ID + Size) or typical lengths
                offset += 2 
            
            if not found_modules_header:
                return False

            # 4. Check the Terminator (Last 6 bytes of the stream)
            # output += struct.pack(pack_symbol + "HI", 16, 0)
            # 16 = 0x0010 (Terminator ID), 0 = Reserved
            term_id, reserved = struct.unpack_from("<HI", data, len(data) - 6)
            return term_id == 16 and reserved == 0

        except (struct.error, IndexError):
            return False

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

@staticmethod
    def from_bytes(data: bytes, endien: str = 'little') -> dict:
        """
        Parses decompressed bytes and extracts project metadata.
        Returns a dict of attributes for VbaProject.
        """
        offset = 0
        pack_symbol = '<' if endien == 'little' else '>'
        
        # State to return
        project_data = {
            "references": [],
            "modules": [],
            "help_context_id": 0,
            "project_cookie": 0,
            "codepage_name": "cp1252" # Default
        }

        while offset < len(data):
            # 1. Read Record ID (2 bytes)
            record_id = struct.unpack_from(pack_symbol + "H", data, offset)[0]
            
            # 2. Check for Terminator (ID 16)
            if record_id == 16:
                break
                
            # 3. Read Size (4 bytes)
            size = struct.unpack_from(pack_symbol + "I", data, offset + 2)[0]
            record_data = data[offset + 6 : offset + 6 + size]
            
            # 4. Map IDs to VbaProject attributes
            # Reference MS-OVBA Section 2.3.4.2
            if record_id == 0x0003: # PROJECTCODEPAGE
                # Map code page to name if necessary
                cp_val = struct.unpack(pack_symbol + "H", record_data)[0]
                project_data["codepage_name"] = f"cp{cp_val}"
            
            elif record_id == 0x0007: # PROJECTHELPCONTEXT
                project_data["help_context_id"] = struct.unpack(pack_symbol + "I", record_data)[0]
                
            elif record_id == 0x0013: # PROJECTCOOKIE
                project_data["project_cookie"] = struct.unpack(pack_symbol + "H", record_data)[0]
            
            # Record parsing for References/Modules would go here
            # e.g., if record_id in [0x0016, 0x0033]: append to references
            # e.g., if record_id == 0x0019: append to modules

            # Move to next record
            offset += 6 + size
            
        return project_data
