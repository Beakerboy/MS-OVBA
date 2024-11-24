import binascii
import ms_ovba_crypto
from vbaproject_compiler.vbaProject import VbaProject
from typing import TypeVar


T = TypeVar('T', bound='Project')


class Project:
    """
    The Project data view for the vbaProject
    """
    def __init__(self: T, project: VbaProject) -> None:
        self.project = project
        # Attributes

        # A list of attributes and values
        self.attributes = {}

        # The HostExtenderInfo string
        guid = "{3832D640-CF90-11CF-8E43-00A0C911005A}"
        self.hostExtenderInfo = "&H00000001=" + guid + ";VBE;&H00000000"

    def add_attribute(self: T, name: str, value: str) -> None:
        self.attributes[name] = value

    def to_bytes(self: T) -> bytes:
        project = self.project
        codepage_name = project.get_codepage_name()
        # Use \x0D0A line endings...however python encodes that.
        eol = b'\x0D\x0A'
        project_id = project.get_project_id()
        id = bytearray(project_id, codepage_name)
        result = b'ID="' + id + b'"' + eol
        modules = project.modules
        for module in modules:
            result += bytes(module.to_project_module_string(), codepage_name)
            result += eol
        result += b'Name="VBAProject"' + eol
        for key in self.attributes:
            result += self._attr(key, self.attributes[key])
        cmg = ms_ovba_crypto.encrypt(
                                     project_id,
                                     project.get_protection_state()
                                    )
        dpb = ms_ovba_crypto.encrypt(project_id, project.get_password())
        gc = ms_ovba_crypto.encrypt(project_id, project.get_visibility_state())
        result += (bytes('CMG="', codepage_name)
                   + binascii.hexlify(cmg).upper()
                   + b'\x22\x0D\x0A')
        result += (bytes('DPB="', codepage_name)
                   + binascii.hexlify(dpb).upper()
                   + b'\x22\x0D\x0A')
        result += (bytes('GC="', codepage_name)
                   + binascii.hexlify(gc).upper()
                   + b'\x22\x0D\x0A')
        result += eol
        result += b'[Host Extender Info]' + eol
        result += bytes(self.hostExtenderInfo, codepage_name)
        result += eol + eol
        result += b'[Workspace]' + eol
        for module in modules:
            separator = ", "
            result += bytes(module.modName.value, codepage_name) + b'='
            joined = separator.join(map(str, module.workspace))
            result += bytes(joined, codepage_name)
            result += eol
        return result

    def write_file(self: T) -> None:
        bin_f = open("project.bin", "wb")
        bin_f.write(self.to_bytes())
        bin_f.close()

    def _attr(self: T, name: str, value: str) -> str:
        codepage_name = self.project.get_codepage_name()
        eol = b'\x0D\x0A'
        b_name = bytes(name, codepage_name)
        b_value = bytes(value, codepage_name)
        return b_name + b'="' + b_value + b'"' + eol
